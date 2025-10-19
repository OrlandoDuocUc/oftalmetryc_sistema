# adapters/input/flask_app/controllers/ficha_clinica_controller_nuevo.py
from flask import request, jsonify
from app.infraestructure.utils.db import SessionLocal
from app.domain.models.consulta_medica import FichaClinica
from app.domain.models.paciente import PacienteMedico
from app.domain.models.biomicroscopia import Biomicroscopia
from app.domain.models.examenes_medicos import (
    FondoOjo,
    ReflejosPupilares,
    ParametrosClinicos,
    DiagnosticoMedico,
    Tratamiento,
)
from sqlalchemy.orm import joinedload
from datetime import datetime

class FichaClinicaController:
    """
    Controlador para gestionar fichas clínicas según estructura SQL real
    """

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Helpers de resumen para exámenes asociados
    # ------------------------------------------------------------------
    @staticmethod
    def _join_values(*values):
        return ", ".join([str(v).strip() for v in values if v and str(v).strip()])

    def _resumen_biomicroscopia(self, bio: Biomicroscopia) -> str:
        od = self._join_values(
            bio.cornea_od,
            bio.cristalino_od,
            bio.pupila_desc_od,
            bio.conjuntiva_bulbar_od,
            bio.parpado_superior_od,
        )
        oi = self._join_values(
            bio.cornea_oi,
            bio.cristalino_oi,
            bio.pupila_desc_oi,
            bio.conjuntiva_bulbar_oi,
            bio.parpado_superior_oi,
        )
        partes = []
        if od:
            partes.append(f"OD: {od}")
        if oi:
            partes.append(f"OI: {oi}")
        if bio.otros_detalles:
            partes.append(bio.otros_detalles)
        elif bio.observaciones_generales:
            partes.append(bio.observaciones_generales)
        return ". ".join(partes)

    def _resumen_fondo_ojo(self, fo: FondoOjo) -> str:
        od = self._join_values(
            fo.disco_optico_od,
            fo.macula_od,
            fo.vasos_od,
            fo.retina_periferica_od,
            fo.excavacion_od,
            fo.color_od,
        )
        oi = self._join_values(
            fo.disco_optico_oi,
            fo.macula_oi,
            fo.vasos_oi,
            fo.retina_periferica_oi,
            fo.excavacion_oi,
            fo.color_oi,
        )
        partes = []
        if od:
            partes.append(f"OD: {od}")
        if oi:
            partes.append(f"OI: {oi}")
        if fo.otros_detalles:
            partes.append(fo.otros_detalles)
        elif fo.observaciones:
            partes.append(fo.observaciones)
        return ". ".join(partes)

    def _resumen_parametros(self, parametros: ParametrosClinicos) -> str:
        presion = self._join_values(
            parametros.presion_sistolica and f"PAS {parametros.presion_sistolica}",
            parametros.presion_diastolica and f"PAD {parametros.presion_diastolica}",
        )
        extras = self._join_values(
            parametros.saturacion_o2 and f"SatO2 {parametros.saturacion_o2}",
            parametros.glucosa and f"Glu {parametros.glucosa}",
            parametros.trigliceridos and f"Trig {parametros.trigliceridos}",
            parametros.ttp and f"TTP {parametros.ttp}",
            parametros.atp and f"ATP {parametros.atp}",
            parametros.colesterol and f"Col {parametros.colesterol}",
        )
        return self._join_values(presion, extras)

    # ---------------------------------------------------------------------
    # LISTAR TODAS
    # ---------------------------------------------------------------------
    def get_all_fichas_clinicas(self):
        """Obtiene todas las fichas clínicas"""
        try:
            session = SessionLocal()
            try:
                fichas = (
                    session.query(FichaClinica)
                    .options(
                        joinedload(FichaClinica.paciente_medico).joinedload(PacienteMedico.cliente),
                        joinedload(FichaClinica.usuario),
                    )
                    .order_by(FichaClinica.fecha_consulta.desc())
                    .all()
                )

                result = []
                for ficha in fichas:
                    data = ficha.to_dict()

                    # Paciente médico y cliente
                    if ficha.paciente_medico:
                        data["paciente_medico"] = {
                            "paciente_medico_id": ficha.paciente_medico.paciente_medico_id,
                            "numero_ficha": ficha.paciente_medico.numero_ficha,
                        }
                        if ficha.paciente_medico.cliente:
                            data["cliente"] = {
                                "nombres": ficha.paciente_medico.cliente.nombres,
                                "ap_pat": ficha.paciente_medico.cliente.ap_pat,
                                "ap_mat": ficha.paciente_medico.cliente.ap_mat,
                                "rut": ficha.paciente_medico.cliente.rut,
                            }

                    # Usuario (médico)
                    if ficha.usuario:
                        data["usuario"] = {
                            "usuario_id": ficha.usuario.usuario_id,
                            "nombre": ficha.usuario.nombre,
                            "username": ficha.usuario.username,
                        }

                    bio = (
                        session.query(Biomicroscopia)
                        .filter(Biomicroscopia.ficha_id == ficha.ficha_id)
                        .order_by(Biomicroscopia.fecha_examen.desc())
                        .first()
                    )
                    if bio:
                        data["biomicroscopia"] = {
                            "biomicroscopia_id": bio.biomicroscopia_id,
                            "fecha_examen": bio.fecha_examen.isoformat() if bio.fecha_examen else None,
                            "resumen": self._resumen_biomicroscopia(bio),
                        }

                    reflejos = (
                        session.query(ReflejosPupilares)
                        .filter(ReflejosPupilares.ficha_id == ficha.ficha_id)
                        .order_by(ReflejosPupilares.fecha_registro.desc())
                        .first()
                    )
                    if reflejos:
                        data["reflejos_pupilares"] = reflejos.to_dict()

                    fondo = (
                        session.query(FondoOjo)
                        .filter(FondoOjo.ficha_id == ficha.ficha_id)
                        .order_by(FondoOjo.fecha_examen.desc())
                        .first()
                    )
                    if fondo:
                        resumen_fondo = self._resumen_fondo_ojo(fondo)
                        info_fondo = fondo.to_dict()
                        info_fondo["resumen"] = resumen_fondo
                        data["fondo_ojo_extendido"] = info_fondo

                    parametros = (
                        session.query(ParametrosClinicos)
                        .filter(ParametrosClinicos.ficha_id == ficha.ficha_id)
                        .order_by(ParametrosClinicos.fecha_registro.desc())
                        .first()
                    )
                    if parametros:
                        info_param = parametros.to_dict()
                        info_param["resumen"] = self._resumen_parametros(parametros)
                        data["parametros_clinicos"] = info_param

                    diagnostico = (
                        session.query(DiagnosticoMedico)
                        .filter(DiagnosticoMedico.ficha_id == ficha.ficha_id)
                        .order_by(DiagnosticoMedico.fecha_diagnostico.desc())
                        .first()
                    )
                    if diagnostico:
                        data["diagnostico"] = diagnostico.to_dict()

                    tratamiento = (
                        session.query(Tratamiento)
                        .filter(Tratamiento.ficha_id == ficha.ficha_id)
                        .order_by(Tratamiento.fecha_tratamiento.desc())
                        .first()
                    )
                    if tratamiento:
                        data["tratamiento"] = tratamiento.to_dict()

                    result.append(data)

                return jsonify({"success": True, "data": result, "total": len(result)})
            finally:
                session.close()
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    # ---------------------------------------------------------------------
    # OBTENER POR ID
    # ---------------------------------------------------------------------
    def get_ficha_clinica_by_id(self, ficha_id):
        """Obtiene una ficha clínica por ID (respuesta normalizada con 'data')"""
        try:
            session = SessionLocal()
            try:
                ficha = (
                    session.query(FichaClinica)
                    .options(
                        joinedload(FichaClinica.paciente_medico).joinedload(PacienteMedico.cliente),
                        joinedload(FichaClinica.usuario),
                    )
                    .filter(FichaClinica.ficha_id == ficha_id)
                    .first()
                )

                if not ficha:
                    return jsonify({"success": False, "error": "Ficha clínica no encontrada"}), 404

                data = ficha.to_dict()

                # Paciente médico y cliente
                if ficha.paciente_medico:
                    data["paciente_medico"] = {
                        "paciente_medico_id": ficha.paciente_medico.paciente_medico_id,
                        "numero_ficha": ficha.paciente_medico.numero_ficha,
                    }
                    if ficha.paciente_medico.cliente:
                        data["cliente"] = {
                            "nombres": ficha.paciente_medico.cliente.nombres,
                            "ap_pat": ficha.paciente_medico.cliente.ap_pat,
                            "ap_mat": ficha.paciente_medico.cliente.ap_mat,
                            "rut": ficha.paciente_medico.cliente.rut,
                        }

                # Usuario (médico)
                if ficha.usuario:
                    data["usuario"] = {
                        "usuario_id": ficha.usuario.usuario_id,
                        "nombre": ficha.usuario.nombre,
                        "username": ficha.usuario.username,
                    }

                return jsonify({"success": True, "data": data})
            finally:
                session.close()
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    # ---------------------------------------------------------------------
    # CREAR
    # ---------------------------------------------------------------------
    def create_ficha_clinica(self):
        """Crea una nueva ficha clínica"""
        try:
            data = request.get_json()
            session = SessionLocal()
            try:
                # Validaciones básicas
                if not data.get("paciente_medico_id"):
                    return jsonify({"success": False, "error": "ID del paciente médico es obligatorio"}), 400

                if not data.get("numero_consulta"):
                    return jsonify({"success": False, "error": "Número de consulta es obligatorio"}), 400

                # Parse fecha_consulta (ISO con o sin zona)
                fc = data.get("fecha_consulta")
                if fc:
                    try:
                        fecha_consulta = datetime.fromisoformat(fc.replace("Z", "+00:00"))
                    except Exception:
                        fecha_consulta = datetime.now()
                else:
                    fecha_consulta = datetime.now()

                # Crear nueva ficha clínica
                nueva_ficha = FichaClinica(
                    paciente_medico_id=data.get("paciente_medico_id"),
                    usuario_id=data.get("usuario_id", 1),  # Default admin user
                    numero_consulta=data.get("numero_consulta"),
                    fecha_consulta=fecha_consulta,
                    motivo_consulta=data.get("motivo_consulta"),
                    historia_actual=data.get("historia_actual"),
                    # Agudeza Visual
                    av_od_sc=data.get("av_od_sc"),
                    av_od_cc=data.get("av_od_cc"),
                    av_od_ph=data.get("av_od_ph"),
                    av_od_cerca=data.get("av_od_cerca"),
                    av_oi_sc=data.get("av_oi_sc"),
                    av_oi_cc=data.get("av_oi_cc"),
                    av_oi_ph=data.get("av_oi_ph"),
                    av_oi_cerca=data.get("av_oi_cerca"),
                    # Refracción
                    esfera_od=data.get("esfera_od"),
                    cilindro_od=data.get("cilindro_od"),
                    eje_od=data.get("eje_od"),
                    adicion_od=data.get("adicion_od"),
                    esfera_oi=data.get("esfera_oi"),
                    cilindro_oi=data.get("cilindro_oi"),
                    eje_oi=data.get("eje_oi"),
                    adicion_oi=data.get("adicion_oi"),
                    # Datos generales
                    distancia_pupilar=data.get("distancia_pupilar"),
                    tipo_lente=data.get("tipo_lente"),
                    estado=data.get("estado", "en_proceso"),
                )

                session.add(nueva_ficha)
                session.commit()
                session.refresh(nueva_ficha)

                return jsonify(
                    {"success": True, "data": nueva_ficha.to_dict(), "message": "Ficha clínica creada exitosamente"}
                ), 201
            finally:
                session.close()
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    # ---------------------------------------------------------------------
    # ACTUALIZAR
    # ---------------------------------------------------------------------
    def update_ficha_clinica(self, ficha_id):
        """Actualiza una ficha clínica existente"""
        try:
            data = request.get_json()
            session = SessionLocal()
            try:
                ficha = session.query(FichaClinica).filter(FichaClinica.ficha_id == ficha_id).first()

                if not ficha:
                    return jsonify({"success": False, "error": "Ficha clínica no encontrada"}), 404

                # Actualizar campos (salvo PK)
                for key, value in data.items():
                    if key == "ficha_id":
                        continue
                    if hasattr(ficha, key):
                        # parse suave para fecha_consulta
                        if key == "fecha_consulta" and isinstance(value, str):
                            try:
                                value = datetime.fromisoformat(value.replace("Z", "+00:00"))
                            except Exception:
                                pass
                        setattr(ficha, key, value)

                session.commit()
                session.refresh(ficha)

                return jsonify({"success": True, "data": ficha.to_dict(), "message": "Ficha clínica actualizada exitosamente"})
            finally:
                session.close()
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    # ---------------------------------------------------------------------
    # LISTAR POR PACIENTE (para historial_paciente.html)  **DEVUELVE ARRAY**
    # ---------------------------------------------------------------------
    def get_consultas_by_paciente(self, paciente_medico_id):
        """
        Obtiene todas las consultas/fichas clínicas de un paciente específico.
        IMPORTANTE: Devuelve un ARRAY plano para ser compatible con historial_paciente.html
        """
        try:
            session = SessionLocal()
            try:
                q = (
                    session.query(FichaClinica)
                    .options(
                        joinedload(FichaClinica.paciente_medico).joinedload(PacienteMedico.cliente),
                        joinedload(FichaClinica.usuario),
                    )
                    .order_by(FichaClinica.fecha_consulta.desc())
                )

                # Usa el nombre de FK correcto
                if hasattr(FichaClinica, "paciente_medico_id"):
                    q = q.filter(FichaClinica.paciente_medico_id == paciente_medico_id)
                elif hasattr(FichaClinica, "paciente_id"):
                    q = q.filter(FichaClinica.paciente_id == paciente_medico_id)
                else:
                    # Si no existe ninguna, retornamos vacío
                    return jsonify([])

                fichas = q.all()

                result = []
                for f in fichas:
                    item = {
                        "ficha_id": getattr(f, "ficha_id", getattr(f, "id", None)),
                        "numero_consulta": getattr(f, "numero_consulta", None),
                        "fecha_consulta": f.fecha_consulta.isoformat() if getattr(f, "fecha_consulta", None) else None,
                        "motivo_consulta": getattr(f, "motivo_consulta", None),
                        "estado": getattr(f, "estado", "en_proceso"),
                    }
                    result.append(item)

                # Devuelve ARRAY (no wrapped) para el front actual
                return jsonify(result)
            finally:
                session.close()
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
