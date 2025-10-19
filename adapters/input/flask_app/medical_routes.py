# adapters/input/flask_app/medical_routes.py
# ============================================================================
# Blueprint de VISTAS (HTML) y endpoints API del mÃ³dulo mÃ©dico.
# - Vistas: dashboard, historial, nueva ficha, detalle consulta, certificado.
# - API: proxys y endpoints mÃ­nimos para exÃ¡menes oftalmolÃ³gicos.
# - EXTENSIONES: /api/personas, /api/clientes/<id>, POST /api/pacientes-medicos flexible
# ============================================================================

from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, abort, current_app
from adapters.input.flask_app.controllers.paciente_controller import PacienteMedicoController
from adapters.input.flask_app.controllers.ficha_clinica_controller_nuevo import FichaClinicaController

from app.infraestructure.utils.db import SessionLocal
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from datetime import datetime

# Modelos nÃºcleo
from app.domain.models.consulta_medica import FichaClinica
from app.domain.models.paciente import PacienteMedico
from app.domain.models.cliente import Cliente
from app.domain.models.user import User

# Modelos de exÃ¡menes (alineados con tu BD)
from app.domain.models.biomicroscopia import Biomicroscopia
from app.domain.models.examenes_medicos import (
    FondoOjo,
    PresionIntraocular,
    CampoVisual,
    DiagnosticoMedico,
    Tratamiento,
    ReflejosPupilares,
    ParametrosClinicos,
)
from app.domain.use_cases.services.biomicroscopia_service import BiomicroscopiaService

from jinja2 import TemplateNotFound

# ----------------------------------------------------------------------------
# Helpers de render
# ----------------------------------------------------------------------------
def _render_view(prefer, fallback=None, **context):
    if prefer:
        try:
            return render_template(prefer, **context)
        except TemplateNotFound:
            pass
    if fallback:
        return render_template(fallback, **context)
    return render_template(prefer, **context)

# Blueprint
medical_bp = Blueprint('medical', __name__)

# Controladores existentes
paciente_medico_controller = PacienteMedicoController()
ficha_clinica_controller = FichaClinicaController()

# ----------------------------------------------------------------------------
# AutenticaciÃ³n mÃ­nima
# ----------------------------------------------------------------------------
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('user_html.login'))
        return f(*args, **kwargs)
    return decorated_function

# ----------------------------------------------------------------------------
# Serializadores simples
# ----------------------------------------------------------------------------
def _serialize_cliente(c: Cliente):
    if not c:
        return None
    return {
        'cliente_id': c.cliente_id,
        'nombres': c.nombres,
        'ap_pat': c.ap_pat,
        'ap_mat': c.ap_mat,
        'rut': c.rut,
        'email': c.email,
        'telefono': c.telefono,
        'direccion': c.direccion,
        'fecha_nacimiento': c.fecha_nacimiento.isoformat() if getattr(c, 'fecha_nacimiento', None) else None,
        'estado': c.estado
    }

def _serialize_paciente(p: PacienteMedico, c: Cliente):
    return {
        'type': 'paciente',
        'paciente_medico_id': p.paciente_medico_id,
        'cliente_id': c.cliente_id if c else None,
        'numero_ficha': p.numero_ficha,
        'antecedentes_medicos': p.antecedentes_medicos,
        'antecedentes_oculares': p.antecedentes_oculares,
        'alergias': p.alergias,
        'medicamentos_actuales': p.medicamentos_actuales,
        'contacto_emergencia': p.contacto_emergencia,
        'telefono_emergencia': p.telefono_emergencia,
        'fecha_registro': p.fecha_registro.isoformat() if getattr(p, 'fecha_registro', None) else None,
        'estado': p.estado,
        'cliente': _serialize_cliente(c)
    }

# ============================================================================
# VISTAS (HTML)
# ============================================================================
@medical_bp.route('/pacientes-medicos')
@login_required
def pacientes():
    return _render_view('medical/pacientes_nuevo.html', 'pacientes_nuevo.html')

@medical_bp.route('/pacientes/nuevo')
@login_required
def nuevo_paciente():
    # Soporta ?cliente_id=<id> para prefill
    return _render_view('medical/nuevo_paciente_form.html', 'nuevo_paciente_form.html')

@medical_bp.route('/pacientes/<int:paciente_id>')
@login_required
def ver_paciente(paciente_id):
    return _render_view('medical/detalle_paciente.html', 'detalle_paciente.html', paciente_id=paciente_id)

@medical_bp.route('/pacientes/<int:paciente_id>/editar')
@login_required
def editar_paciente(paciente_id):
    return _render_view('medical/editar_paciente.html', 'editar_paciente.html', paciente_id=paciente_id)

@medical_bp.route('/pacientes-medicos/<int:paciente_id>/editar')
@login_required
def editar_paciente_medico(paciente_id):
    return _render_view('medical/editar_paciente.html', 'editar_paciente.html', paciente_id=paciente_id)

@medical_bp.route('/pacientes-medicos/<int:paciente_id>/historial')
@login_required
def historial_paciente(paciente_id):
    # El template consume /api/pacientes-medicos/<id>/consultas y pinta la lista
    return _render_view('medical/historial_paciente.html', 'historial_paciente.html', paciente_id=paciente_id)

@medical_bp.route('/consultas-nuevo')
@login_required
def consultas():
    # El template consume /api/fichas-clinicas
    return _render_view('medical/consultas_nuevo.html', 'consultas_nuevo.html')

@medical_bp.route('/consultas/nueva')
@login_required
def nueva_consulta():
    return redirect(url_for('medical.ficha_clinica'))

@medical_bp.route('/consultas/<int:consulta_id>')
@login_required
def ver_consulta(consulta_id):
    # El template hace fetch a /api/fichas-clinicas/<id>
    return _render_view('medical/detalle_consulta.html', 'detalle_consulta.html', consulta_id=consulta_id)

@medical_bp.route('/consultas/<int:consulta_id>/editar')
@login_required
def editar_consulta(consulta_id):
    return _render_view('medical/editar_consulta.html', 'editar_consulta.html', consulta_id=consulta_id)

# --- RUTA LEGACY DE EXAMEN OFTALMOLÓGICO (INHABILITADA) ---
# Conservamos la función como referencia histórica, pero sin exponerla.
# @medical_bp.route('/consultas/<int:consulta_id>/examen')
# @login_required
# def examen_oftalmologico(consulta_id):
#     return _render_view('medical/examen_oftalmologico_nuevo.html', 'examen_oftalmologico_nuevo.html', consulta_id=consulta_id)

@medical_bp.route('/dashboard-medico')
@login_required
def dashboard_medico():
    return _render_view('medical/dashboard_medico_final.html', 'dashboard_medico_final.html')

# --- Endpoints con nombre explÃ­cito (para url_for desde el dashboard)
@medical_bp.route('/ficha-clinica-nuevo', endpoint='ficha_clinica')
@login_required
def ficha_clinica_view():
    return _render_view('medical/ficha_clinica_nuevo.html', 'ficha_clinica_nuevo.html')

# @medical_bp.route('/examen-oftalmologico-nuevo', endpoint='examen_oftalmologico_nuevo')
# @login_required
# def examen_oftalmologico_nuevo_view():
#     """Ruta deshabilitada: se mantiene como comentario para referencia."""
#     return _render_view('medical/examen_oftalmologico_nuevo.html', 'examen_oftalmologico_nuevo.html')


@medical_bp.route('/biomicroscopia-nuevo', endpoint='biomicroscopia_nuevo')
@login_required
def biomicroscopia_nuevo_view():
    consulta_id = request.args.get('consulta_id', type=int)
    paciente_id = request.args.get('paciente_id')
    context = {}
    if consulta_id:
        context['consulta_id'] = consulta_id
    if paciente_id:
        context['paciente_id'] = paciente_id
    return _render_view('medical/biomicroscopia_nuevo.html', 'biomicroscopia_nuevo.html', **context)

# ============================================================================
# CERTIFICADO (con datos opcionales si existen)
# ============================================================================
def _formatear_fecha_es(dt):
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    try:
        return f"{dt.day} de {meses[dt.month - 1]} del {dt.year}"
    except Exception:
        return dt.strftime("%d/%m/%Y")

def _calcular_edad(fecha_nacimiento, en_fecha):
    if not fecha_nacimiento:
        return None
    try:
        years = en_fecha.year - fecha_nacimiento.year
        if (en_fecha.month, en_fecha.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
            years -= 1
        return years
    except Exception:
        return None

def _compactar_textos_campos(obj, campos):
    if not obj:
        return None
    valores = []
    for nombre in campos:
        val = getattr(obj, nombre, None)
        if val:
            valores.append(str(val).strip())
    return ", ".join(valores) if valores else None

@medical_bp.route('/consultas/<int:consulta_id>/certificado')
@login_required
def certificado_consulta(consulta_id):
    db = SessionLocal()
    try:
        consulta = (
            db.query(FichaClinica)
              .options(
                  joinedload(FichaClinica.paciente_medico).joinedload(PacienteMedico.cliente),
                  joinedload(FichaClinica.usuario)
              )
              .filter(FichaClinica.ficha_id == consulta_id)
              .first()
        )
        if not consulta:
            abort(404, description="Ficha clÃ­nica no encontrada")

        paciente = consulta.paciente_medico
        cliente = paciente.cliente if paciente else None
        usuario = consulta.usuario

        edad = _calcular_edad(getattr(cliente, "fecha_nacimiento", None), consulta.fecha_consulta)
        fecha_consulta_str = _formatear_fecha_es(consulta.fecha_consulta)

        # BiomicroscopÃ­a (resumen)
        biomicroscopia_texto = None
        bio = db.query(Biomicroscopia).filter_by(ficha_id=consulta_id).first()
        if bio:
            od = _compactar_textos_campos(bio, [
                "parpados_od", "conjuntiva_od", "cornea_od", "camara_anterior_od", "iris_od", "cristalino_od"
            ])
            oi = _compactar_textos_campos(bio, [
                "parpados_oi", "conjuntiva_oi", "cornea_oi", "camara_anterior_oi", "iris_oi", "cristalino_oi"
            ])
            obs = getattr(bio, "observaciones_generales", None)
            partes = []
            if od: partes.append(f"OD: {od}")
            if oi: partes.append(f"OI: {oi}")
            if obs: partes.append(obs)
            biomicroscopia_texto = ". ".join(partes) if partes else None

        # Fondo de ojo (resumen)
        fondo_ojo_texto = None
        fo = db.query(FondoOjo).filter_by(ficha_id=consulta_id).first()
        if fo:
            od = _compactar_textos_campos(fo, ["disco_optico_od", "macula_od", "vasos_od", "retina_periferica_od"])
            oi = _compactar_textos_campos(fo, ["disco_optico_oi", "macula_oi", "vasos_oi", "retina_periferica_oi"])
            obs = getattr(fo, "observaciones", None)
            partes = []
            if od: partes.append(f"OD: {od}")
            if oi: partes.append(f"OI: {oi}")
            if obs: partes.append(obs)
            fondo_ojo_texto = ". ".join(partes) if partes else None

        # DiagnÃ³stico (principal/secundario)
        diagnostico_texto = None
        dx = (
            db.query(DiagnosticoMedico)
              .filter_by(ficha_id=consulta_id)
              .order_by(DiagnosticoMedico.fecha_diagnostico.desc())
              .first()
        )
        if dx:
            principal = (dx.diagnostico_principal or "").strip()
            cie_p = f"({dx.cie_10_principal})" if dx.cie_10_principal else ""
            secundarios = []
            if dx.diagnosticos_secundarios:
                secundarios.append(dx.diagnosticos_secundarios.strip())
            if dx.cie_10_secundarios:
                secundarios.append(f"({dx.cie_10_secundarios.strip()})")
            secundarios_txt = ", ".join([s for s in secundarios if s])
            partes = []
            if principal:
                partes.append(f"{principal} {cie_p}".strip())
            if secundarios_txt:
                partes.append(secundarios_txt)
            diagnostico_texto = ", ".join([p for p in partes if p])

        # Tratamiento (viÃ±etas)
        tratamiento_items = []
        tx = (
            db.query(Tratamiento)
              .filter_by(ficha_id=consulta_id)
              .order_by(Tratamiento.fecha_tratamiento.desc())
              .first()
        )
        if tx:
            posibles = [
                getattr(tx, "medicamentos", None),
                getattr(tx, "tratamiento_no_farmacologico", None),
                getattr(tx, "recomendaciones", None),
                getattr(tx, "plan_seguimiento", None),
            ]
            for bloque in posibles:
                if bloque:
                    for linea in str(bloque).splitlines():
                        l = linea.strip().lstrip("âœ“").strip()
                        if l:
                            tratamiento_items.append(l)

        # Firma
        medico_nombre = None
        if usuario:
            partes_nombre = [getattr(usuario, "nombre", None), getattr(usuario, "ap_pat", None)]
            medico_nombre = " ".join([p for p in partes_nombre if p])

        footer_info = {
            "direccion": "CALLE GARCÃA AVILES 318 entre Av. 9 de OCTUBRE Y VELEZ",
            "telefonos": "Telf: 0980632277 / 0998436958 / 0985394814",
            "ciudad": "Guayaquil",
        }

        return _render_view(
            'medical/certificado.html', 'certificado.html',
            consulta=consulta,
            paciente=paciente,
            cliente=cliente,
            edad=edad,
            fecha_consulta_str=fecha_consulta_str,
            biomicroscopia_texto=biomicroscopia_texto,
            fondo_ojo_texto=fondo_ojo_texto,
            diagnostico_texto=diagnostico_texto,
            tratamiento_items=tratamiento_items,
            medico_nombre=medico_nombre,
            footer_info=footer_info
        )
    finally:
        db.close()

# ============================================================================
# API - PERSONAS (PACIENTES + CLIENTES)
# ============================================================================
@medical_bp.route('/api/personas', methods=['GET'])
@login_required
def api_get_personas():
    """
    Devuelve una lista unificada de:
    - Pacientes con su cliente embebido  -> type='paciente'
    - Clientes sin ficha mÃ©dica          -> type='cliente'
    Filtros:
      q       : texto (nombre o rut)
      estado  : true/false (aplica al estado del registro correspondiente)
    """
    q = (request.args.get('q') or '').strip()
    estado = request.args.get('estado')
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))

    db = SessionLocal()
    try:
        items = []

        # 1) Pacientes (join Cliente)
        pq = (
            db.query(PacienteMedico, Cliente)
              .join(Cliente, PacienteMedico.cliente_id == Cliente.cliente_id)
        )
        if q:
            like = f"%{q}%"
            pq = pq.filter(or_(Cliente.nombres.ilike(like),
                               Cliente.ap_pat.ilike(like),
                               Cliente.ap_mat.ilike(like),
                               Cliente.rut.ilike(like)))
        if estado in ('true', 'false'):
            val = (estado == 'true')
            pq = pq.filter(PacienteMedico.estado == val)
        pacientes = pq.all()

        paciente_cliente_ids = set()
        for p, c in pacientes:
            items.append(_serialize_paciente(p, c))
            paciente_cliente_ids.add(c.cliente_id)

        # 2) Clientes sin ficha
        cq = db.query(Cliente).filter(~Cliente.cliente_id.in_(paciente_cliente_ids))
        if q:
            like = f"%{q}%"
            cq = cq.filter(or_(Cliente.nombres.ilike(like),
                               Cliente.ap_pat.ilike(like),
                               Cliente.ap_mat.ilike(like),
                               Cliente.rut.ilike(like)))
        if estado in ('true', 'false'):
            val = (estado == 'true')
            cq = cq.filter(Cliente.estado == val)

        clientes = cq.order_by(Cliente.nombres.asc()).offset(offset).limit(limit).all()

        for c in clientes:
            items.append({
                'type': 'cliente',
                'cliente_id': c.cliente_id,
                'estado': c.estado,
                'cliente': _serialize_cliente(c)
            })

        # Para pacientes tambiÃ©n respetamos paginaciÃ³n bÃ¡sica (opcional):
        # AquÃ­ mantenemos items completos; si deseas paginar de verdad, unifica en SQL con UNION.

        return jsonify({'success': True, 'data': items, 'meta': {'count': len(items)}})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

# ============================================================================
# API - CLIENTES (para prefill y detalle simple)
# ============================================================================
@medical_bp.route('/api/clientes/<int:cliente_id>', methods=['GET'])
@login_required
def api_get_cliente(cliente_id):
    db = SessionLocal()
    try:
        c = db.query(Cliente).filter(Cliente.cliente_id == cliente_id).first()
        if not c:
            return jsonify({'success': False, 'message': 'Cliente no encontrado'}), 404
        return jsonify({'success': True, 'data': _serialize_cliente(c)})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

# ============================================================================
# API - PACIENTES MÃ‰DICOS (existentes + POST flexible)
# ============================================================================
@medical_bp.route('/api/pacientes-medicos', methods=['GET'])
@login_required
def api_get_pacientes_medicos():
    return paciente_medico_controller.get_all_pacientes_medicos()

@medical_bp.route('/api/pacientes-medicos/search', methods=['GET'])
@login_required
def api_search_pacientes_medicos():
    return paciente_medico_controller.search_pacientes_medicos()

@medical_bp.route('/api/pacientes-medicos', methods=['POST'])
@login_required
def api_create_paciente_medico():
    """
    POST flexible:
    a) { cliente_id, paciente_medico: {...} }     -> usa cliente existente
    b) { cliente: {...}, paciente_medico: {...} } -> crea cliente + paciente
    c) (fallback) delega al controlador existente si no coincide con (a) o (b)
    """
    payload = request.get_json(silent=True) or {}
    db = SessionLocal()
    try:
        # Caso (a) / (b)
        if ('cliente_id' in payload) or ('cliente' in payload):
            # Resolver cliente
            cliente_obj = None
            if 'cliente_id' in payload and payload['cliente_id']:
                cliente_obj = db.query(Cliente).filter(Cliente.cliente_id == int(payload['cliente_id'])).first()
                if not cliente_obj:
                    return jsonify({'success': False, 'message': 'Cliente no encontrado'}), 404
            else:
                # Crear o reutilizar por RUC/CÃ©dula
                cdata = payload.get('cliente') or {}
                rut = (cdata.get('rut') or '').strip()
                if not rut:
                    return jsonify({'success': False, 'message': 'El campo rut (CÃ©dula/RUC) es requerido en cliente'}), 400
                existente = db.query(Cliente).filter(Cliente.rut == rut).first()
                if existente:
                    cliente_obj = existente
                else:
                    cliente_obj = Cliente(
                        nombres=cdata.get('nombres') or '',
                        ap_pat=cdata.get('ap_pat') or '',
                        ap_mat=cdata.get('ap_mat'),
                        rut=rut,
                        email=cdata.get('email'),
                        telefono=cdata.get('telefono'),
                        direccion=cdata.get('direccion'),
                        fecha_nacimiento=cdata.get('fecha_nacimiento'),
                        estado=True
                    )
                    db.add(cliente_obj)
                    db.flush()

            # Verifica que no exista ya un PacienteMedico para este cliente
            ya_pm = db.query(PacienteMedico).filter(PacienteMedico.cliente_id == cliente_obj.cliente_id).first()
            if ya_pm:
                return jsonify({'success': False, 'message': 'El cliente ya posee ficha de Paciente'}), 409

            pmdata = payload.get('paciente_medico') or {}
            numero_ficha = pmdata.get('numero_ficha') or f"FM-{datetime.now().strftime('%Y%m')}-{int(datetime.now().timestamp()*1000)}"

            paciente = PacienteMedico(
                cliente_id=cliente_obj.cliente_id,
                numero_ficha=numero_ficha,
                antecedentes_medicos=pmdata.get('antecedentes_medicos'),
                antecedentes_oculares=pmdata.get('antecedentes_oculares'),
                alergias=pmdata.get('alergias'),
                medicamentos_actuales=pmdata.get('medicamentos_actuales'),
                contacto_emergencia=pmdata.get('contacto_emergencia'),
                telefono_emergencia=pmdata.get('telefono_emergencia'),
                estado=pmdata.get('estado', True)
            )
            db.add(paciente)
            db.commit()

            return jsonify({'success': True, 'data': _serialize_paciente(paciente, cliente_obj)}), 201

        # Caso (c) fallback a controlador existente (compatibilidad)
        return paciente_medico_controller.create_paciente_medico()

    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        db.close()

@medical_bp.route('/api/pacientes-medicos/<int:paciente_medico_id>', methods=['GET'])
@login_required
def api_get_paciente_medico(paciente_medico_id):
    return paciente_medico_controller.get_paciente_medico_by_id(paciente_medico_id)

@medical_bp.route('/api/pacientes-medicos/<int:paciente_medico_id>/consultas', methods=['GET'])
@login_required
def api_get_consultas_paciente(paciente_medico_id):
    """
    Devuelve las fichas clÃ­nicas del paciente (por paciente_medico_id).
    Fallback si por error se entrega un cliente_id.
    """
    db = SessionLocal()
    try:
        # 1) Intento directo por paciente_medico_id
        fichas = (
            db.query(FichaClinica)
              .filter(FichaClinica.paciente_medico_id == paciente_medico_id)
              .order_by(FichaClinica.fecha_consulta.desc())
              .all()
        )

        # 2) Fallback: si no hay fichas, considerar que llegÃ³ cliente_id
        if not fichas:
            pm = (
                db.query(PacienteMedico)
                  .filter(PacienteMedico.cliente_id == paciente_medico_id)
                  .first()
            )
            if pm:
                fichas = (
                    db.query(FichaClinica)
                      .filter(FichaClinica.paciente_medico_id == pm.paciente_medico_id)
                      .order_by(FichaClinica.fecha_consulta.desc())
                      .all()
                )

        items = []
        for f in fichas:
            items.append({
                'ficha_id': f.ficha_id,
                'numero_consulta': getattr(f, 'numero_consulta', None),
                'fecha_consulta': f.fecha_consulta.isoformat() if getattr(f, 'fecha_consulta', None) else None,
                'motivo_consulta': getattr(f, 'motivo_consulta', None),
                'estado': getattr(f, 'estado', None) or 'en_proceso',
            })

        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# ============================================================================
# API - FICHAS CLÃNICAS
# ============================================================================
@medical_bp.route('/api/fichas-clinicas', methods=['GET'])
@login_required
def api_get_fichas_clinicas():
    return ficha_clinica_controller.get_all_fichas_clinicas()

@medical_bp.route('/api/fichas-clinicas', methods=['POST'])
@login_required
def api_create_ficha_clinica():
    return ficha_clinica_controller.create_ficha_clinica()

@medical_bp.route('/api/fichas-clinicas/<int:ficha_id>', methods=['GET'])
@login_required
def api_get_ficha_clinica_by_id(ficha_id):
    return ficha_clinica_controller.get_ficha_clinica_by_id(ficha_id)

@medical_bp.route('/api/fichas-clinicas/<int:ficha_id>', methods=['PUT'])
@login_required
def api_update_ficha_clinica(ficha_id):
    return ficha_clinica_controller.update_ficha_clinica(ficha_id)

# ---------------------------------------------------------------------------
# API - RESUMEN DE EXÃMENES POR FICHA (para detalle / historial si se quiere)
# ---------------------------------------------------------------------------
@medical_bp.route('/api/fichas-clinicas/<int:ficha_id>/examenes', methods=['GET'])
@login_required
def api_get_examenes_por_ficha(ficha_id):
    db = SessionLocal()
    try:
        data = {'ficha_id': ficha_id, 'fondo_ojo': None, 'presion_intraocular': None}

        fo = (
            db.query(FondoOjo)
              .filter_by(ficha_id=ficha_id)
              .order_by(FondoOjo.fecha_examen.desc())
              .first()
        )
        if fo:
            data['fondo_ojo'] = {
                'od': ", ".join([x for x in [fo.disco_optico_od, fo.macula_od, fo.vasos_od, fo.retina_periferica_od] if x]),
                'oi': ", ".join([x for x in [fo.disco_optico_oi, fo.macula_oi, fo.vasos_oi, fo.retina_periferica_oi] if x]),
                'observaciones': fo.observaciones,
                'fecha_examen': fo.fecha_examen.isoformat() if fo.fecha_examen else None
            }

        pio = (
            db.query(PresionIntraocular)
              .filter_by(ficha_id=ficha_id)
              .order_by(PresionIntraocular.fecha_medicion.desc())
              .first()
        )
        if pio:
            data['presion_intraocular'] = {
                'pio_od': pio.pio_od,
                'pio_oi': pio.pio_oi,
                'metodo': pio.metodo_medicion,
                'hora': pio.hora_medicion.isoformat() if pio.hora_medicion else None,
                'observaciones': pio.observaciones,
                'fecha_medicion': pio.fecha_medicion.isoformat() if pio.fecha_medicion else None
            }

        return jsonify({'success': True, 'data': data})
    finally:
        db.close()

# ---------------------------------------------------------------------------
# API - EXAMEN DE BIOMICROSCOPÍA COMPLETO
# ---------------------------------------------------------------------------
@medical_bp.route('/api/biomicroscopia/<int:ficha_id>')
@login_required
def api_get_biomicroscopia(ficha_id):
    service = BiomicroscopiaService()
    data = service.obtener_examen(ficha_id)
    return jsonify({'success': True, 'data': data})


@medical_bp.route('/api/biomicroscopia', methods=['POST'])
@login_required
def api_save_biomicroscopia():
    payload = request.get_json(silent=True) or {}
    ficha_id = payload.get('ficha_id')

    if ficha_id is None:
        return jsonify({'success': False, 'message': 'ficha_id es requerido'}), 400

    try:
        ficha_id = int(ficha_id)
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'ficha_id no es válido'}), 400

    service = BiomicroscopiaService()

    try:
        resultado = service.guardar_examen(ficha_id, payload)

        diagnostico_txt = (payload.get('diagnostico') or '').strip()
        tratamiento_txt = (payload.get('tratamiento') or '').strip()

        if diagnostico_txt or tratamiento_txt:
            db = SessionLocal()
            try:
                if diagnostico_txt:
                    diag = (
                        db.query(DiagnosticoMedico)
                        .filter(DiagnosticoMedico.ficha_id == ficha_id)
                        .order_by(DiagnosticoMedico.fecha_diagnostico.desc())
                        .first()
                    )
                    if not diag:
                        diag = DiagnosticoMedico(ficha_id=ficha_id)
                    diag.diagnostico_principal = diagnostico_txt
                    db.add(diag)

                if tratamiento_txt:
                    tx = (
                        db.query(Tratamiento)
                        .filter(Tratamiento.ficha_id == ficha_id)
                        .order_by(Tratamiento.fecha_tratamiento.desc())
                        .first()
                    )
                    if not tx:
                        tx = Tratamiento(ficha_id=ficha_id)
                    tx.medicamentos = tratamiento_txt
                    db.add(tx)

                db.commit()

                if diagnostico_txt:
                    resultado['diagnostico'] = diag.to_dict()
                if tratamiento_txt:
                    resultado['tratamiento'] = tx.to_dict()
            except Exception:
                db.rollback()
                raise
            finally:
                db.close()

        return jsonify({'success': True, 'data': resultado})
    except Exception as exc:
        current_app.logger.exception('Error guardando examen de biomicroscopía')
        return jsonify({'success': False, 'message': str(exc)}), 500

# ---------------------------------------------------------------------------
# API - GUARDAR EXAMEN OFTALMOLÃ“GICO (desde examen_oftalmologico_nuevo.html)
# Guarda en tablas existentes: presion_intraocular y fondo_ojo
# ---------------------------------------------------------------------------
@medical_bp.route('/api/examenes-oftalmologicos', methods=['POST'])
@login_required
def api_save_examen_oftalmologico():
    payload = request.get_json(silent=True) or {}

    # 1) Resolver ficha_id de forma flexible
    ficha_id = (
        payload.get('ficha_id')
        or payload.get('consulta_id')
        or payload.get('consultaId')
    )

    db = SessionLocal()
    try:
        if not ficha_id:
            # Fallback: si viene paciente_rut, buscar su Ãºltima ficha
            rut = (payload.get('paciente_rut') or "").strip()
            if rut:
                cli = db.query(Cliente).filter(Cliente.rut == rut).first()
                if cli:
                    pm = db.query(PacienteMedico).filter(PacienteMedico.cliente_id == cli.cliente_id).first()
                    if pm:
                        ficha = (
                            db.query(FichaClinica)
                              .filter(FichaClinica.paciente_medico_id == pm.paciente_medico_id)
                              .order_by(FichaClinica.fecha_consulta.desc())
                              .first()
                        )
                        if ficha:
                            ficha_id = ficha.ficha_id

        if not ficha_id:
            return jsonify({'success': False, 'message': 'ficha_id es requerido (o proporcione paciente_rut para resolverla)'}), 400

        # Verificar que la ficha exista
        ficha = db.query(FichaClinica).filter_by(ficha_id=ficha_id).first()
        if not ficha:
            return jsonify({'success': False, 'message': 'Ficha clÃ­nica no encontrada'}), 404

        guardados = {'fondo_ojo': False, 'presion_intraocular': False}

        # ---- FONDO DE OJO ----
        fondo_od = (payload.get('fondo_ojo_od') or "").strip()
        fondo_oi = (payload.get('fondo_ojo_oi') or "").strip()
        obs_agudeza = (payload.get('observaciones_agudeza') or "").strip()  # lo usamos como "observaciones" si llega

        if fondo_od or fondo_oi or obs_agudeza:
            fo = FondoOjo(
                ficha_id=ficha_id,
                disco_optico_od=None,
                macula_od=None,
                vasos_od=None,
                retina_periferica_od=fondo_od if fondo_od else None,
                disco_optico_oi=None,
                macula_oi=None,
                vasos_oi=None,
                retina_periferica_oi=fondo_oi if fondo_oi else None,
                observaciones=obs_agudeza if obs_agudeza else None
            )
            db.add(fo)
            guardados['fondo_ojo'] = True

        # ---- PIO ----
        pio_od = (payload.get('pio_od') or "").strip()
        pio_oi = (payload.get('pio_oi') or "").strip()
        metodo = (payload.get('metodo_tonometria') or "").strip()
        hora_txt = (payload.get('hora_medicion') or payload.get('horaMediacion') or "").strip()
        hora_val = None
        if hora_txt:
            try:
                hora_val = datetime.strptime(hora_txt, "%H:%M").time()
            except Exception:
                hora_val = None

        if pio_od or pio_oi or metodo or hora_val:
            pio = PresionIntraocular(
                ficha_id=ficha_id,
                pio_od=pio_od if pio_od else None,
                pio_oi=pio_oi if pio_oi else None,
                metodo_medicion=metodo if metodo else None,
                hora_medicion=hora_val,
                observaciones=None
            )
            db.add(pio)
            guardados['presion_intraocular'] = True

        db.commit()
        return jsonify({'success': True, 'message': 'Examen guardado', 'guardados': guardados})

    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': f'Error al guardar examen: {str(e)}'}), 500
    finally:
        db.close()

__all__ = ['medical_bp']

