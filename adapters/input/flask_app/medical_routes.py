from flask import Blueprint, render_template, session, redirect, url_for
from adapters.input.flask_app.controllers.paciente_controller import PacienteController
from adapters.input.flask_app.controllers.consulta_medica_controller import ConsultaMedicaController

# Crear el blueprint
medical_bp = Blueprint('medical', __name__)

# Inicializar controladores
paciente_controller = PacienteController()
consulta_controller = ConsultaMedicaController()

def login_required(f):
    """Decorador para verificar autenticación"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# RUTAS DE VISTAS (HTML)
# ============================================================================

@medical_bp.route('/pacientes')
@login_required
def pacientes():
    """Vista principal de pacientes"""
    return render_template('medical/pacientes.html')

@medical_bp.route('/pacientes/nuevo')
@login_required
def nuevo_paciente():
    """Vista para crear nuevo paciente"""
    return render_template('medical/nuevo_paciente.html')

@medical_bp.route('/pacientes/<int:paciente_id>')
@login_required
def ver_paciente(paciente_id):
    """Vista detalle de paciente"""
    return render_template('medical/detalle_paciente.html', paciente_id=paciente_id)

@medical_bp.route('/pacientes/<int:paciente_id>/editar')
@login_required
def editar_paciente(paciente_id):
    """Vista para editar paciente"""
    return render_template('medical/editar_paciente.html', paciente_id=paciente_id)

@medical_bp.route('/consultas')
@login_required
def consultas():
    """Vista principal de consultas"""
    return render_template('medical/consultas.html')

@medical_bp.route('/consultas/nueva')
@login_required
def nueva_consulta():
    """Vista para nueva consulta"""
    return render_template('medical/nueva_consulta.html')

@medical_bp.route('/consultas/<int:consulta_id>')
@login_required
def ver_consulta(consulta_id):
    """Vista detalle de consulta"""
    return render_template('medical/detalle_consulta.html', consulta_id=consulta_id)

@medical_bp.route('/consultas/<int:consulta_id>/examen')
@login_required
def examen_oftalmologico(consulta_id):
    """Vista para realizar examen oftalmológico completo"""
    return render_template('medical/examen_oftalmologico.html', consulta_id=consulta_id)

@medical_bp.route('/dashboard-medico')
@login_required
def dashboard_medico():
    """Dashboard médico"""
    return render_template('medical/dashboard_medico.html')

# ============================================================================
# RUTAS API - PACIENTES
# ============================================================================

@medical_bp.route('/api/pacientes', methods=['GET'])
@login_required
def api_get_pacientes():
    """API: Obtener todos los pacientes"""
    return paciente_controller.get_all_pacientes()

@medical_bp.route('/api/pacientes/search', methods=['GET'])
@login_required
def api_search_pacientes():
    """API: Buscar pacientes"""
    return paciente_controller.search_pacientes()

@medical_bp.route('/api/pacientes', methods=['POST'])
@login_required
def api_create_paciente():
    """API: Crear paciente"""
    return paciente_controller.create_paciente()

@medical_bp.route('/api/pacientes/<int:paciente_id>', methods=['GET'])
@login_required
def api_get_paciente(paciente_id):
    """API: Obtener paciente por ID"""
    return paciente_controller.get_paciente_by_id(paciente_id)

@medical_bp.route('/api/pacientes/<int:paciente_id>', methods=['PUT'])
@login_required
def api_update_paciente(paciente_id):
    """API: Actualizar paciente"""
    return paciente_controller.update_paciente(paciente_id)

@medical_bp.route('/api/pacientes/<int:paciente_id>', methods=['DELETE'])
@login_required
def api_delete_paciente(paciente_id):
    """API: Eliminar paciente"""
    return paciente_controller.delete_paciente(paciente_id)

# ============================================================================
# RUTAS API - CONSULTAS
# ============================================================================

@medical_bp.route('/api/consultas', methods=['GET'])
@login_required
def api_get_consultas():
    """API: Obtener todas las consultas"""
    return consulta_controller.get_all_consultas()

@medical_bp.route('/api/consultas', methods=['POST'])
@login_required
def api_create_consulta():
    """API: Crear consulta"""
    return consulta_controller.create_consulta()

@medical_bp.route('/api/consultas/<int:consulta_id>', methods=['GET'])
@login_required
def api_get_consulta(consulta_id):
    """API: Obtener consulta por ID"""
    return consulta_controller.get_consulta_by_id(consulta_id)

@medical_bp.route('/api/consultas/<int:consulta_id>', methods=['PUT'])
@login_required
def api_update_consulta(consulta_id):
    """API: Actualizar consulta"""
    return consulta_controller.update_consulta(consulta_id)

@medical_bp.route('/api/consultas/<int:consulta_id>', methods=['DELETE'])
@login_required
def api_delete_consulta(consulta_id):
    """API: Eliminar consulta"""
    return consulta_controller.delete_consulta(consulta_id)

@medical_bp.route('/api/pacientes/<int:paciente_id>/consultas', methods=['GET'])
@login_required
def api_get_consultas_paciente(paciente_id):
    """API: Obtener consultas de un paciente"""
    return consulta_controller.get_consultas_by_paciente(paciente_id)

@medical_bp.route('/api/consultas/hoy', methods=['GET'])
@login_required
def api_get_consultas_hoy():
    """API: Obtener consultas de hoy"""
    return consulta_controller.get_consultas_hoy()

@medical_bp.route('/api/diagnosticos', methods=['GET'])
@login_required
def api_get_diagnosticos():
    """API: Obtener diagnósticos"""
    return consulta_controller.get_diagnosticos()

# ============================================================================
# RUTAS FICHA CLÍNICA DIGITAL - INTEGRADAS
# ============================================================================

@medical_bp.route('/ficha-clinica')
@login_required
def ficha_clinica():
    """Página principal de ficha clínica digital"""
    return render_template('medical/ficha_clinica.html')

@medical_bp.route('/api/ficha-clinica/buscar-pacientes', methods=['POST'])
@login_required
def api_buscar_pacientes_ficha():
    """API: Buscar pacientes para ficha clínica"""
    from flask import request, jsonify
    from app.infraestructure.utils.db_session import get_db_session
    from app.domain.models.paciente import Paciente
    
    try:
        data = request.get_json()
        ci = data.get('ci', '').strip()
        nombre = data.get('nombre', '').strip()
        
        if not ci and not nombre:
            return jsonify({'error': 'Debe proporcionar CI o nombre para buscar'}), 400
        
        db_session = get_db_session()
        query = db_session.query(Paciente)
        
        if ci:
            # Buscar por CI exacto
            paciente = query.filter(Paciente.ci == ci).first()
        else:
            # Buscar por nombre (contiene)
            nombre_busqueda = f"%{nombre}%"
            pacientes = query.filter(
                (Paciente.nombres.ilike(nombre_busqueda)) |
                (Paciente.apellidos.ilike(nombre_busqueda))
            ).limit(10).all()
            
            if pacientes:
                paciente = pacientes[0]
            else:
                paciente = None
        
        if paciente:
            return jsonify({
                'found': True,
                'paciente': {
                    'id': paciente.id,
                    'ci': paciente.ci,
                    'nombres': paciente.nombres,
                    'apellidos': paciente.apellidos,
                    'edad': paciente.edad,
                    'genero': paciente.genero,
                    'telefono': paciente.telefono,
                    'email': paciente.email
                }
            })
        else:
            return jsonify({
                'found': False,
                'message': 'Paciente no encontrado'
            })
            
    except Exception as e:
        return jsonify({'error': f'Error en la búsqueda: {str(e)}'}), 500
    finally:
        if 'db_session' in locals():
            db_session.close()

@medical_bp.route('/api/ficha-clinica/guardar', methods=['POST'])
@login_required
def api_guardar_ficha():
    """API: Guardar datos de ficha clínica"""
    from flask import request, jsonify
    from app.infraestructure.utils.db_session import get_db_session
    from app.domain.models.examen_basico import ExamenBasico
    from app.infraestructure.utils.models import ConsultaMedica
    from datetime import datetime
    
    try:
        data = request.get_json()
        paciente_id = data.get('paciente_id')
        
        if not paciente_id:
            return jsonify({'error': 'ID de paciente requerido'}), 400
        
        db_session = get_db_session()
        
        # Crear nueva consulta médica
        nueva_consulta = ConsultaMedica(
            paciente_id=paciente_id,
            fecha_consulta=datetime.now(),
            motivo_consulta=data.get('motivo_consulta', ''),
            diagnostico=data.get('diagnostico', ''),
            observaciones=data.get('observaciones', ''),
            estado='Completada'
        )
        
        db_session.add(nueva_consulta)
        db_session.flush()  # Para obtener el ID
        
        # Crear examen básico asociado
        examen = ExamenBasico(consulta_id=nueva_consulta.id)
        
        # Campos de examen a actualizar
        campos_examen = [
            'av_distancia_od', 'av_distancia_oi', 'av_distancia_ao',
            'av_proximidad_od', 'av_proximidad_oi', 'av_proximidad_ao',
            'pin_hole_od', 'pin_hole_oi', 'dominancia_ocular',
            'autorefractor_od_esfera', 'autorefractor_od_cilindro', 'autorefractor_od_eje',
            'autorefractor_oi_esfera', 'autorefractor_oi_cilindro', 'autorefractor_oi_eje',
            'rx_final_od_esfera', 'rx_final_od_cilindro', 'rx_final_od_eje', 'rx_final_od_adicion',
            'rx_final_oi_esfera', 'rx_final_oi_cilindro', 'rx_final_oi_eje', 'rx_final_oi_adicion',
            'lc_od_poder', 'lc_od_curva_base', 'lc_od_diametro', 'lc_od_material',
            'lc_oi_poder', 'lc_oi_curva_base', 'lc_oi_diametro', 'lc_oi_material',
            'pio_od', 'pio_oi', 'pio_metodo', 'pio_hora',
            'test_ishihara', 'test_hirschberg', 'cover_test', 'luces_worth',
            'observaciones', 'diagnostico', 'recomendaciones'
        ]
        
        # Actualizar campos del examen
        for campo in campos_examen:
            if campo in data:
                setattr(examen, campo, data[campo])
        
        db_session.add(examen)
        db_session.commit()
        
        return jsonify({
            'success': True,
            'consulta_id': nueva_consulta.id,
            'message': 'Ficha clínica guardada exitosamente'
        })
        
    except Exception as e:
        if 'db_session' in locals():
            db_session.rollback()
        return jsonify({'error': f'Error al guardar ficha: {str(e)}'}), 500
    finally:
        if 'db_session' in locals():
            db_session.close()