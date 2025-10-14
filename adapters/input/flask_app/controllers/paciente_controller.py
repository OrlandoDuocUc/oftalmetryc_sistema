# -*- coding: utf-8 -*-
"""
Controller de Pacientes Médicos
- Crea/actualiza Cliente por rut (cédula/RUC EC) y asocia PacienteMedico.
- Evita duplicados por cliente_id.
- Genera numero_ficha único si no viene del front.
- Devuelve JSON consistente para el front actual.
"""

from flask import request, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from datetime import datetime
import random
import re

from app.infraestructure.utils.db import SessionLocal
from app.domain.models.cliente import Cliente
from app.domain.models.paciente import PacienteMedico


class PacienteMedicoController:
    # ---------------------------- Utilidades ----------------------------

    def _validar_identificacion_ec(self, valor: str) -> bool:
        """
        Acepta:
          - Cédula: 10 dígitos con verificador (módulo 10).
          - RUC persona natural: 13 dígitos, base cédula válida + '001'.
        Para empresa privada/pública el RUC es más complejo; de momento
        limitamos a natural (cobertura habitual en clínica).
        """
        if not valor:
            return False
        s = re.sub(r"\D+", "", valor)
        if len(s) == 10:
            return self._validar_cedula_ec(s)
        if len(s) == 13 and s.endswith("001"):
            base = s[:10]
            return self._validar_cedula_ec(base)
        # Permitir otros 13 dígitos como fallback suave (evita bloquear flujo),
        # pero es mejor exigir formato correcto. Descomenta la línea siguiente
        # si quieres endurecer:
        # return False
        return False

    def _validar_cedula_ec(self, ci: str) -> bool:
        if not re.fullmatch(r"\d{10}", ci):
            return False
        provincia = int(ci[:2])
        if provincia < 1 or provincia > 24:
            return False
        coef = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        suma = 0
        for i in range(9):
            prod = int(ci[i]) * coef[i]
            if prod >= 10:
                prod -= 9
            suma += prod
        decena = ((suma + 9) // 10) * 10
        digito = (decena - suma) % 10
        return digito == int(ci[9])

    def _normalizar_rut(self, valor: str) -> str:
        return re.sub(r"\D+", "", valor or "").strip()

    def _generar_numero_ficha(self, db) -> str:
        """
        Genera un número de ficha único estilo FM-YYYYMM-<ticks>-NNN.
        Verifica colisión en BD por si hay varias creaciones simultáneas.
        """
        for _ in range(5):
            ahora = datetime.utcnow()
            pref = f"FM-{ahora.year}{str(ahora.month).zfill(2)}-{int(ahora.timestamp() * 1000)}-{random.randint(100,999)}"
            existe = (
                db.query(PacienteMedico)
                  .filter(PacienteMedico.numero_ficha == pref)
                  .first()
            )
            if not existe:
                return pref
        # Último recurso (prácticamente imposible colisionar 5 veces)
        return f"FM-{int(datetime.utcnow().timestamp()*1000)}-{random.randint(1000,9999)}"

    def _cliente_to_dict(self, c: Cliente) -> dict:
        if not c:
            return {}
        return {
            "cliente_id": c.cliente_id,
            "nombres": c.nombres,
            "ap_pat": c.ap_pat,
            "ap_mat": c.ap_mat,
            "rut": c.rut,
            "email": c.email,
            "telefono": c.telefono,
            "direccion": c.direccion,
            "fecha_nacimiento": c.fecha_nacimiento.isoformat() if getattr(c, "fecha_nacimiento", None) else None,
            "estado": c.estado,
        }

    def _paciente_to_dict(self, p: PacienteMedico, include_cliente=True) -> dict:
        if not p:
            return {}
        data = {
            "paciente_medico_id": p.paciente_medico_id,
            "cliente_id": p.cliente_id,
            "numero_ficha": p.numero_ficha,
            "antecedentes_medicos": p.antecedentes_medicos,
            "antecedentes_oculares": p.antecedentes_oculares,
            "alergias": p.alergias,
            "medicamentos_actuales": p.medicamentos_actuales,
            "contacto_emergencia": p.contacto_emergencia,
            "telefono_emergencia": p.telefono_emergencia,
            "fecha_registro": p.fecha_registro.isoformat() if getattr(p, "fecha_registro", None) else None,
            "estado": p.estado,
        }
        if include_cliente:
            # joinedload nos permite acceder sin DetachedInstanceError
            try:
                data["cliente"] = self._cliente_to_dict(getattr(p, "cliente", None))
            except Exception:
                data["cliente"] = None
        return data

    # ---------------------------- Endpoints ----------------------------

    def get_all_pacientes_medicos(self):
        db = SessionLocal()
        try:
            pacientes = (
                db.query(PacienteMedico)
                  .options(joinedload(PacienteMedico.cliente))
                  .order_by(PacienteMedico.paciente_medico_id.desc())
                  .all()
            )
            data = [self._paciente_to_dict(p) for p in pacientes]
            return jsonify({"success": True, "data": data})
        except Exception as e:
            db.rollback()
            return jsonify({"success": False, "message": f"Error al listar pacientes: {str(e)}"}), 500
        finally:
            db.close()

    def get_paciente_medico_by_id(self, paciente_medico_id: int):
        db = SessionLocal()
        try:
            p = (
                db.query(PacienteMedico)
                  .options(joinedload(PacienteMedico.cliente))
                  .filter(PacienteMedico.paciente_medico_id == paciente_medico_id)
                  .first()
            )
            if not p:
                return jsonify({"success": False, "message": "Paciente no encontrado"}), 404
            return jsonify({"success": True, "data": self._paciente_to_dict(p)})
        except Exception as e:
            db.rollback()
            return jsonify({"success": False, "message": f"Error al obtener paciente: {str(e)}"}), 500
        finally:
            db.close()

    def search_pacientes_medicos(self):
        """
        GET /api/pacientes-medicos/search?q=texto
        Busca por nombre/apellido/rut con ilike. Responde igual que get_all.
        """
        q = (request.args.get("q") or "").strip().lower()
        db = SessionLocal()
        try:
            query = (
                db.query(PacienteMedico)
                  .join(Cliente, Cliente.cliente_id == PacienteMedico.cliente_id)
                  .options(joinedload(PacienteMedico.cliente))
            )
            if q:
                like = f"%{q}%"
                query = query.filter(
                    (func.lower(Cliente.nombres).ilike(like)) |
                    (func.lower(Cliente.ap_pat).ilike(like)) |
                    (func.lower(Cliente.ap_mat).ilike(like)) |
                    (func.lower(Cliente.rut).ilike(like))
                )
            pacientes = query.order_by(PacienteMedico.paciente_medico_id.desc()).all()
            data = [self._paciente_to_dict(p) for p in pacientes]
            return jsonify({"success": True, "data": data})
        except Exception as e:
            db.rollback()
            return jsonify({"success": False, "message": f"Error de búsqueda: {str(e)}"}), 500
        finally:
            db.close()

    def create_paciente_medico(self):
        """
        POST /api/pacientes-medicos
        body: {
          "cliente": {...},            # nombres, ap_pat, ap_mat?, rut, email?, telefono?, direccion?, fecha_nacimiento?
          "paciente_medico": {...}     # numero_ficha?, antecedentes_*, alergias, medicamentos_actuales, contacto_emergencia, telefono_emergencia, estado?
        }
        """
        payload = request.get_json(silent=True) or {}
        cli_in = payload.get("cliente") or {}
        pac_in = payload.get("paciente_medico") or {}

        db = SessionLocal()
        try:
            # ---------- 1) Validación básica en servidor ----------
            rut_raw = cli_in.get("rut", "")
            rut_norm = self._normalizar_rut(rut_raw)
            if not self._validar_identificacion_ec(rut_norm):
                return jsonify({"success": False, "message": "Cédula/RUC inválido para Ecuador."}), 400

            nombres = (cli_in.get("nombres") or "").strip()
            ap_pat = (cli_in.get("ap_pat") or "").strip()
            if not nombres or not ap_pat:
                return jsonify({"success": False, "message": "Nombres y Apellido Paterno son obligatorios."}), 400

            # ---------- 2) UPSERT Cliente por rut ----------
            cliente = db.query(Cliente).filter(Cliente.rut == rut_norm).first()
            if cliente:
                # Actualiza campos si vinieron
                cliente.nombres = nombres or cliente.nombres
                cliente.ap_pat = ap_pat or cliente.ap_pat
                if cli_in.get("ap_mat") is not None:
                    cliente.ap_mat = (cli_in.get("ap_mat") or "").strip() or None
                if cli_in.get("email") is not None:
                    cliente.email = (cli_in.get("email") or "").strip() or None
                if cli_in.get("telefono") is not None:
                    cliente.telefono = (cli_in.get("telefono") or "").strip() or None
                if cli_in.get("direccion") is not None:
                    cliente.direccion = (cli_in.get("direccion") or "").strip() or None
                if cli_in.get("fecha_nacimiento"):
                    try:
                        cliente.fecha_nacimiento = datetime.fromisoformat(cli_in["fecha_nacimiento"]).date()
                    except Exception:
                        pass
                if cli_in.get("estado") is not None:
                    cliente.estado = bool(cli_in.get("estado"))
                db.flush()
            else:
                cliente = Cliente(
                    rut=rut_norm,
                    nombres=nombres,
                    ap_pat=ap_pat,
                    ap_mat=(cli_in.get("ap_mat") or "").strip() or None,
                    email=(cli_in.get("email") or "").strip() or None,
                    telefono=(cli_in.get("telefono") or "").strip() or None,
                    direccion=(cli_in.get("direccion") or "").strip() or None,
                    estado=True,
                )
                db.add(cliente)
                db.flush()  # para obtener cliente_id

            # ---------- 3) Evitar duplicado de PacienteMedico por cliente ----------
            existente = (
                db.query(PacienteMedico)
                  .filter(PacienteMedico.cliente_id == cliente.cliente_id)
                  .first()
            )
            if existente:
                # Ya es paciente. Devolver 200 con datos (idempotente)
                data = self._paciente_to_dict(existente, include_cliente=True)
                return jsonify({"success": True, "message": "El cliente ya es paciente.", "data": data})

            # ---------- 4) Crear PacienteMedico ----------
            numero_ficha = (pac_in.get("numero_ficha") or "").strip()
            if not numero_ficha:
                numero_ficha = self._generar_numero_ficha(db)
            else:
                # Verifica unicidad si viene desde el front
                colision = (
                    db.query(PacienteMedico)
                      .filter(PacienteMedico.numero_ficha == numero_ficha)
                      .first()
                )
                if colision:
                    numero_ficha = self._generar_numero_ficha(db)

            paciente = PacienteMedico(
                cliente_id=cliente.cliente_id,
                numero_ficha=numero_ficha,
                antecedentes_medicos=(pac_in.get("antecedentes_medicos") or "").strip() or None,
                antecedentes_oculares=(pac_in.get("antecedentes_oculares") or "").strip() or None,
                alergias=(pac_in.get("alergias") or "").strip() or None,
                medicamentos_actuales=(pac_in.get("medicamentos_actuales") or "").strip() or None,
                contacto_emergencia=(pac_in.get("contacto_emergencia") or "").strip() or None,
                telefono_emergencia=(pac_in.get("telefono_emergencia") or "").strip() or None,
                estado=bool(pac_in.get("estado", True)),
            )
            db.add(paciente)
            db.flush()   # obtener PK y fecha_registro si hay default en servidor
            db.commit()  # ---------- COMMIT ÚNICO ----------

            # Recargar con joinedload para respuesta consistente y evitar DetachedInstanceError
            paciente_refrescado = (
                db.query(PacienteMedico)
                  .options(joinedload(PacienteMedico.cliente))
                  .filter(PacienteMedico.paciente_medico_id == paciente.paciente_medico_id)
                  .first()
            )

            return jsonify({
                "success": True,
                "message": "Paciente creado correctamente.",
                "data": self._paciente_to_dict(paciente_refrescado, include_cliente=True)
            }), 201

        except Exception as e:
            db.rollback()
            return jsonify({"success": False, "message": f"Error al crear paciente: {str(e)}"}), 500
        finally:
            db.close()
