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