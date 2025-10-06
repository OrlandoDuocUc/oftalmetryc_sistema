from flask import Blueprint
from adapters.input.flask_app.controllers.proveedor_controller import ProveedorController

# Crear blueprint para proveedores
proveedor_bp = Blueprint('proveedores', __name__)

# Instanciar controlador
proveedor_controller = ProveedorController()

# Rutas principales
@proveedor_bp.route('/proveedores')
def lista_proveedores():
    """Página principal de proveedores"""
    return proveedor_controller.listar_proveedores()

@proveedor_bp.route('/proveedores/crear', methods=['GET', 'POST'])
def crear_proveedor():
    """Crear nuevo proveedor"""
    return proveedor_controller.crear_proveedor()

@proveedor_bp.route('/proveedores/<int:proveedor_id>/editar', methods=['GET', 'POST'])
def editar_proveedor(proveedor_id):
    """Editar proveedor existente"""
    return proveedor_controller.editar_proveedor(proveedor_id)

@proveedor_bp.route('/proveedores/<int:proveedor_id>/ver')
def ver_proveedor(proveedor_id):
    """Ver detalles de proveedor"""
    return proveedor_controller.ver_proveedor(proveedor_id)

@proveedor_bp.route('/proveedores/<int:proveedor_id>/eliminar', methods=['DELETE'])
def eliminar_proveedor(proveedor_id):
    """Eliminar proveedor"""
    return proveedor_controller.eliminar_proveedor(proveedor_id)

# APIs para búsqueda y datos
@proveedor_bp.route('/api/proveedores/buscar')
def buscar_proveedores():
    """API para buscar proveedores"""
    return proveedor_controller.buscar_proveedores()

@proveedor_bp.route('/api/proveedores/<int:proveedor_id>')
def obtener_proveedor(proveedor_id):
    """API para obtener datos de un proveedor"""
    return proveedor_controller.obtener_proveedor_api(proveedor_id)