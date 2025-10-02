from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask_restx import Api
from .user_routes import ns_users
from .product_routes import ns_products
from .sale_routes import ns_sales
from .medical_routes import medical_bp
from app.domain.use_cases.services.user_service import UserService
from app.domain.use_cases.services.sale_service import SaleService
from app.domain.use_cases.services.cliente_service import ClienteService
from app.infraestructure.repositories.sql_product_repository import SQLProductRepository
from app.infraestructure.utils.db import SessionLocal
from app.infraestructure.utils.db_session import get_db_session, close_db_session
from app.domain.models.products import Product
from app.domain.models.sale import Sale
from app.domain.models.cliente import Cliente
from app.domain.models.user import User
from datetime import datetime, date, timedelta
from app.infraestructure.utils.date_utils import get_chile_date, get_day_start_end_chile, format_datetime_chile
import json

bp = Blueprint('routes', __name__, template_folder='templates')

# Servicios - Crear nuevas instancias cada vez para evitar problemas de caché
def get_user_service():
    return UserService()

def get_product_service():
    db_session = SessionLocal()
    product_repo = SQLProductRepository(db_session)
    return product_repo

def get_sale_service():
    return SaleService()

def get_cliente_service():
    return ClienteService()

# Función para verificar sesión activa
def require_login():
    if 'user_id' not in session:
        flash('Debe iniciar sesión para acceder a esta página.', 'danger')
        return redirect(url_for('routes.login'))
    return None

# Función para verificar si es administrador
def require_admin():
    login_check = require_login()
    if login_check:
        return login_check
    if session.get('rol') != 'Administrador':
        flash('Acceso denegado. Se requieren permisos de administrador.', 'danger')
        return redirect(url_for('routes.login'))
    return None

# Función para verificar si es vendedor
def require_vendor():
    login_check = require_login()
    if login_check:
        return login_check
    if session.get('rol') not in ['Administrador', 'Vendedor']:
        flash('Acceso denegado. Se requieren permisos de vendedor.', 'danger')
        return redirect(url_for('routes.login'))
    return None

# Rutas web para HTML y formularios funcionales
@bp.route('/')
def index():
    # Si hay sesión activa, redirigir según el rol
    if 'user_id' in session and 'rol' in session:
        if session['rol'] == 'Administrador':
            return redirect(url_for('product_html.dashboard'))
        else:
            return redirect(url_for('routes.registrar_venta'))
    
    # Si no hay sesión, redirigir al login
    return redirect(url_for('user_html.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        user = get_user_service().authenticate(usuario, password)
        if user == 'inactivo':
            return render_template('login.html', error='Usuario inactivo o eliminado. No puede iniciar sesión.')
        if user:
            session['user_id'] = getattr(user, 'usuario_id', None)
            # Obtener el nombre del rol desde la relación o consulta
            rol_nombre = None
            if hasattr(user, 'rol') and hasattr(user.rol, 'nombre'):
                rol_nombre = user.rol.nombre
            else:
                # Consulta directa si no hay relación
                from app.domain.models.rol import Rol
                from app.infraestructure.utils.db import SessionLocal
                db_session = SessionLocal()
                try:
                    rol_obj = db_session.query(Rol).filter(Rol.rol_id == getattr(user, 'rol_id', None)).first()
                    rol_nombre = getattr(rol_obj, 'nombre', 'Vendedor') if rol_obj else 'Vendedor'
                finally:
                    db_session.close()
            session['rol'] = rol_nombre
            # Redirigir según el rol
            if rol_nombre == 'Administrador':
                return redirect(url_for('product_html.dashboard'))
            else:
                return redirect(url_for('routes.registrar_venta'))
        return render_template('login.html', error='Credenciales inválidas')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user_html.login'))

@bp.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    # Solo administradores pueden acceder
    admin_check = require_admin()
    if admin_check:
        return admin_check
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        ap_pat = request.form['ap_pat']
        ap_mat = request.form['ap_mat']
        usuario = request.form['usuario']
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']
        
        user_service = get_user_service()
        result = user_service.register_user(nombre, ap_pat, ap_mat, usuario, email, password, rol)
        
        if result:
            flash('Usuario registrado exitosamente', 'success')
        else:
            flash('Error al registrar usuario', 'error')
        
        return redirect(url_for('routes.usuarios'))
    
    users = get_user_service().get_all_users()
    return render_template('usuarios.html', users=users)

@bp.route('/productos', methods=['GET', 'POST'])
def productos():
    # Solo administradores pueden acceder
    admin_check = require_admin()
    if admin_check:
        return admin_check
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio_unitario = float(request.form['precio_unitario'])
        stock = int(request.form['stock'])
        
        # Crear producto usando el repositorio directamente
        db_session = SessionLocal()
        try:
            from app.domain.models.products import Product
            from app.infraestructure.utils.date_utils import get_chile_datetime_naive
            
            nuevo_producto = Product(
                nombre=nombre,
                descripcion=descripcion,
                precio_unitario=precio_unitario,
                stock=stock,
                estado='A',
                fecha_creacion=get_chile_datetime_naive()
            )
            
            product_repo = SQLProductRepository(db_session)
            result = product_repo.save(nuevo_producto)
            
            if result:
                flash('Producto registrado exitosamente', 'success')
            else:
                flash('Error al registrar producto', 'error')
                
        finally:
            db_session.close()
        
        return redirect(url_for('routes.productos'))
    
    # Obtener productos usando el repositorio directamente
    db_session = SessionLocal()
    try:
        product_repo = SQLProductRepository(db_session)
        products = product_repo.get_all()
    finally:
        db_session.close()
    
    return render_template('productos.html', products=products)

@bp.route('/registrar-venta', methods=['GET', 'POST'])
def registrar_venta():
    # Verificar sesión activa
    login_check = require_login()
    if login_check:
        return login_check
    
    # Permitir acceso a administradores y vendedores
    if session.get('rol') not in ['Administrador', 'Vendedor']:
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('routes.login'))
    
    if request.method == 'POST':
        # Este método POST ya no se usa directamente, se maneja con AJAX
        pass
    
    # Obtener productos usando el repositorio directamente
    db_session = SessionLocal()
    try:
        product_repo = SQLProductRepository(db_session)
        productos = product_repo.get_all()
    finally:
        db_session.close()
    
    return render_template('registrar_venta.html', products=productos)

@bp.route('/historial-ventas')
def historial_ventas():
    # Verificar sesión activa
    login_check = require_login()
    if login_check:
        return login_check
    
    # Permitir acceso a administradores y vendedores
    if session.get('rol') not in ['Administrador', 'Vendedor']:
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('routes.login'))
    
    ventas = get_sale_service().get_all_sales_with_details()
    return render_template('historial_ventas.html', ventas=ventas)

@bp.route('/dashboard')
def dashboard():
    # Verificar sesión activa
    login_check = require_login()
    if login_check:
        return login_check
    
    # Permitir acceso a administradores y vendedores
    if session.get('rol') not in ['Administrador', 'Vendedor']:
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('routes.login'))
    
    # Obtener datos reales del dashboard
    try:
        db_session = get_db_session()
        try:
            # Obtener productos en stock (stock > 0)
            productos_en_stock = db_session.query(Product).filter(Product.stock > 0).count()
            
            # Obtener ventas del día actual en zona horaria de Chile
            hoy_chile = get_chile_date()
            start_of_day, end_of_day = get_day_start_end_chile(hoy_chile)
            
            ventas_hoy = db_session.query(Sale).filter(
                Sale.fecha >= start_of_day,
                Sale.fecha < end_of_day
            ).all()
            
            # Calcular total de ventas del día
            total_ventas_hoy = sum(float(getattr(venta, 'total', 0)) for venta in ventas_hoy if getattr(venta, 'total', None) is not None)
            
            # Obtener ventas recientes con detalles completos
            ventas_recientes = db_session.query(Sale).order_by(Sale.fecha.desc()).limit(10).all()
            
            # Crear lista con información completa de ventas recientes
            ventas_con_detalles = []
            for venta in ventas_recientes:
                # Obtener información del producto
                producto = db_session.query(Product).filter_by(producto_id=venta.producto_id).first()
                
                # Obtener información del cliente
                cliente_nombre = "Sin cliente"
                if venta.cliente_id is not None:
                    cliente = db_session.query(Cliente).filter_by(cliente_id=venta.cliente_id).first()
                    if cliente:
                        cliente_nombre = f"{cliente.nombres} {cliente.ap_pat}"
                
                ventas_con_detalles.append({
                    'venta_id': venta.venta_id,
                    'producto_nombre': producto.nombre if producto else 'Producto no encontrado',
                    'cantidad': venta.cantidad,
                    'total': venta.total,
                    'cliente': cliente_nombre,
                    'fecha': format_datetime_chile(venta.fecha)
                })
            
            return render_template('dashboard.html', 
                                 productos_en_stock=productos_en_stock,
                                 total_ventas_hoy=total_ventas_hoy,
                                 ventas_recientes=ventas_con_detalles)
        
        finally:
            close_db_session(db_session)
    
    except Exception as e:
        # En caso de error, mostrar valores por defecto
        return render_template('dashboard.html', 
                             productos_en_stock=0,
                             total_ventas_hoy=0,
                             ventas_recientes=[])

@bp.route('/boleta/<int:venta_id>')
def boleta(venta_id):
    # Verificar sesión activa
    login_check = require_login()
    if login_check:
        return login_check
    
    # Permitir acceso a administradores y vendedores
    if session.get('rol') not in ['Administrador', 'Vendedor']:
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('routes.login'))
    
    try:
        # Obtener la venta con todos los datos necesarios
        db_session = get_db_session()
        try:
            # Obtener la venta principal
            venta_principal = db_session.query(Sale).filter_by(venta_id=venta_id).first()
            if not venta_principal:
                flash('Venta no encontrada', 'danger')
                return redirect(url_for('routes.registrar_venta'))
            
            # Obtener información del cliente
            cliente_info = None
            if venta_principal.cliente_id is not None:
                cliente = db_session.query(Cliente).filter_by(cliente_id=venta_principal.cliente_id).first()
                if cliente:
                    cliente_info = {
                        'nombre_completo': f"{cliente.nombres} {cliente.ap_pat} {cliente.ap_mat or ''}".strip(),
                        'telefono': cliente.telefono,
                        'email': cliente.email,
                        'direccion': cliente.direccion
                    }
            
            # Obtener información del vendedor
            vendedor_info = None
            if venta_principal.usuario_id is not None:
                vendedor = db_session.query(User).filter_by(usuario_id=venta_principal.usuario_id).first()
                if vendedor:
                    vendedor_info = {
                        'nombre_completo': f"{vendedor.nombre} {vendedor.ap_pat} {vendedor.ap_mat or ''}".strip()
                    }
            
            # Buscar todas las ventas relacionadas (mismo cliente, mismo vendedor, misma fecha)
            # Usar un margen de 5 minutos para agrupar ventas de la misma transacción
            
            ventas_relacionadas = db_session.query(Sale).filter(
                Sale.cliente_id == venta_principal.cliente_id,
                Sale.usuario_id == venta_principal.usuario_id,
                Sale.fecha >= venta_principal.fecha - timedelta(minutes=5),
                Sale.fecha <= venta_principal.fecha + timedelta(minutes=5)
            ).order_by(Sale.fecha).all()
            
            # Crear lista de productos de la venta
            productos_venta = []
            total_general = 0
            
            for venta in ventas_relacionadas:
                # Obtener información del producto
                producto = db_session.query(Product).filter_by(producto_id=venta.producto_id).first()
                if producto:
                    subtotal = float(getattr(venta, 'total', 0)) if getattr(venta, 'total', None) is not None else 0
                    total_general += subtotal
                    
                    productos_venta.append({
                        'nombre': getattr(producto, 'nombre', 'Sin nombre'),
                        'cantidad': getattr(venta, 'cantidad', 0),
                        'precio_unitario': float(getattr(producto, 'precio_unitario', 0)) if getattr(producto, 'precio_unitario', None) is not None else 0,
                        'subtotal': subtotal
                    })
            
            # Crear un diccionario con los datos de la venta principal
            venta_data = {
                'venta_id': venta_principal.venta_id,
                'producto_id': venta_principal.producto_id,
                'usuario_id': venta_principal.usuario_id,
                'cantidad': venta_principal.cantidad,
                'total': total_general,  # Total general de todas las ventas
                'cliente_id': venta_principal.cliente_id,
                'fecha': venta_principal.fecha
            }
            
            return render_template('boleta.html', 
                                 venta=venta_data,
                                 productos_venta=productos_venta,
                                 total_general=total_general,
                                 cliente_info=cliente_info,
                                 vendedor_info=vendedor_info)
        
        finally:
            close_db_session(db_session)
    
    except Exception as e:
        flash(f'Error al generar la boleta: {str(e)}', 'danger')
        return redirect(url_for('routes.registrar_venta'))

# Rutas para el carrito de compras
@bp.route('/agregar-al-carrito', methods=['POST'])
def agregar_al_carrito():
    """Agrega un producto al carrito de compras"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Debe iniciar sesión'})
    
    try:
        data = request.get_json()
        producto_id = data.get('producto_id')
        cantidad = data.get('cantidad')
        total = data.get('total')
        nombre = data.get('nombre')
        precio_unitario = data.get('precio_unitario')
        
        if not all([producto_id, cantidad, total, nombre, precio_unitario]):
            return jsonify({'success': False, 'message': 'Datos incompletos'})
        
        # Inicializar carrito si no existe
        if 'carrito' not in session:
            session['carrito'] = []
            session['total_carrito'] = 0
        
        # Verificar si el producto ya está en el carrito
        for item in session['carrito']:
            if item['producto_id'] == producto_id:
                return jsonify({'success': False, 'message': 'El producto ya está en el carrito'})
        
        # Agregar producto al carrito
        item_carrito = {
            'producto_id': producto_id,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio_unitario': precio_unitario,
            'subtotal': total
        }
        
        session['carrito'].append(item_carrito)
        session['total_carrito'] = sum(float(item['subtotal']) for item in session['carrito'])
        
        return jsonify({'success': True, 'message': 'Producto agregado al carrito'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@bp.route('/eliminar-del-carrito', methods=['POST'])
def eliminar_del_carrito():
    """Elimina un producto del carrito de compras"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Debe iniciar sesión'})
    
    try:
        data = request.get_json()
        producto_id = data.get('producto_id')
        
        if 'carrito' in session:
            # Eliminar el producto del carrito
            session['carrito'] = [item for item in session['carrito'] if item['producto_id'] != producto_id]
            
            # Recalcular total
            session['total_carrito'] = sum(float(item['subtotal']) for item in session['carrito'])
            
            # Si el carrito está vacío, limpiarlo
            if not session['carrito']:
                session.pop('carrito', None)
                session.pop('total_carrito', None)
        
        return jsonify({'success': True, 'message': 'Producto eliminado del carrito'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@bp.route('/limpiar-carrito', methods=['POST'])
def limpiar_carrito():
    """Limpia todo el carrito de compras"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Debe iniciar sesión'})
    
    try:
        session.pop('carrito', None)
        session.pop('total_carrito', None)
        return jsonify({'success': True, 'message': 'Carrito limpiado'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@bp.route('/finalizar-venta', methods=['POST'])
def finalizar_venta():
    """Finaliza la venta procesando todos los productos del carrito"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Debe iniciar sesión'})
    
    if 'carrito' not in session or not session['carrito']:
        return jsonify({'success': False, 'message': 'El carrito está vacío'})
    
    try:
        data = request.get_json()
        cliente_data = {
            'nombres': data.get('nombres', ''),
            'ap_pat': data.get('ap_pat', ''),
            'ap_mat': data.get('ap_mat', ''),
            'telefono': data.get('telefono', ''),
            'email': data.get('email', ''),
            'direccion': data.get('direccion', '')
        }
        
        # Crear cliente si se proporcionaron datos
        cliente_id = None
        if cliente_data['nombres'] and cliente_data['ap_pat']:
            cliente_service = get_cliente_service()
            cliente_id = cliente_service.create_cliente(**cliente_data)
            # Ahora create_cliente devuelve directamente el ID del cliente
        
        # Procesar cada producto del carrito
        sale_service = get_sale_service()
        ventas_creadas = []
        
        for item in session['carrito']:
            # Registrar la venta individual
            venta_id = sale_service.register_sale(
                producto_id=item['producto_id'],
                usuario_id=session['user_id'],
                cantidad=item['cantidad'],
                total=item['subtotal'],
                cliente_id=cliente_id
            )
            
            if venta_id:
                ventas_creadas.append(venta_id)
            else:
                # Si falla alguna venta, hacer rollback
                return jsonify({'success': False, 'message': f'Error al registrar venta del producto {item["nombre"]}'})
        
        # Limpiar carrito después de venta exitosa
        session.pop('carrito', None)
        session.pop('total_carrito', None)
        
        # Redirigir a la boleta de la primera venta (o dashboard)
        redirect_url = f'/boleta/{ventas_creadas[0]}' if ventas_creadas else '/'
        
        return jsonify({
            'success': True, 
            'message': f'Venta finalizada exitosamente. {len(ventas_creadas)} productos vendidos.',
            'redirect_url': redirect_url
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al finalizar la venta: {str(e)}'})

# API RESTX
api = Api(
    bp,
    version='1.0.0',
    openapi='3.0.0',
    title='Oftalmetryc API',
    description='API para la gestión de usuarios, productos y ventas en el sistema de Oftalmetryc.',
    default='General',
    default_label='Operaciones Generales',
    validate=True,
    swagger_ui_config={
        'docExpansion': 'list',
        'defaultModelsExpandDepth': -1,
        'filter': True,
        'displayRequestDuration': True,
        'deepLinking': True,
        'persistAuthorization': True
    }
)

api.add_namespace(ns_users, path='/users')
api.add_namespace(ns_products, path='/products')
api.add_namespace(ns_sales, path='/sales')

def register_routes(app):
    app.register_blueprint(bp)
