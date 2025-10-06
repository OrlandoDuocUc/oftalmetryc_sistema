from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.domain.use_cases.services.user_service import UserService

# Creación del Blueprint para las rutas de usuario
user_html = Blueprint('user_html', __name__, template_folder='templates')

# Instancia del servicio que contiene toda la lógica de negocio
user_service = UserService()

@user_html.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya inició sesión, redirigir al dashboard
    if 'user_id' in session:
        if session.get('rol') == 'Administrador':
            return redirect(url_for('product_html.dashboard'))
        else:
            return redirect(url_for('routes.registrar_venta'))
            
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = user_service.authenticate(username, password)
        
        if user == 'inactivo':
            flash('Tu cuenta está inactiva. Por favor, contacta al administrador.', 'danger')
            return render_template('login.html')
        
        if user:
            # Guardar información esencial en la sesión
            session['user_id'] = user.usuario_id
            session['username'] = user.username
            session['rol'] = user.rol.nombre
            
            flash('Inicio de sesión exitoso.', 'success')
            
            # Redirigir según el rol
            if user.rol.nombre == 'Administrador':
                return redirect(url_for('product_html.dashboard'))
            else:
                return redirect(url_for('routes.registrar_venta'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            return render_template('login.html')
    
    return render_template('login.html')

@user_html.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('user_html.login'))

@user_html.route('/usuarios')
def usuarios():
    # Proteger la ruta: solo para administradores
    if 'user_id' not in session or session.get('rol') != 'Administrador':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('user_html.login'))
        
    try:
        users = user_service.get_all_users()
        return render_template('usuarios.html', users=users)
    except Exception as e:
        print(f"Error al cargar usuarios: {e}")
        flash('Ocurrió un error al cargar los usuarios.', 'danger')
        return render_template('usuarios.html', users=[])

@user_html.route('/usuarios/toggle/<int:usuario_id>', methods=['POST'])
def toggle_estado_usuario(usuario_id):
    if session.get('rol') != 'Administrador':
        return redirect(url_for('user_html.login'))
    
    try:
        user = user_service.get_user(usuario_id)
        if user:
            # Cambia el estado al opuesto del actual
            nuevo_estado = not user.estado
            user_service.update_user(usuario_id, estado=nuevo_estado)
            flash(f'Estado del usuario {user.username} actualizado.', 'success')
    except Exception as e:
        flash('Error al cambiar el estado del usuario.', 'danger')
        
    return redirect(url_for('user_html.usuarios'))

@user_html.route('/usuarios/edit/<int:usuario_id>', methods=['POST'])
def editar_usuario(usuario_id):
    if session.get('rol') != 'Administrador':
        return redirect(url_for('user_html.login'))
        
    try:
        data = {
            'nombre': request.form['nombre'],
            'ap_pat': request.form['ap_pat'],
            'ap_mat': request.form['ap_mat'],
            'username': request.form['username'],
            'email': request.form['email']
        }
        user_service.update_user(usuario_id, **data)
        flash('Usuario actualizado correctamente.', 'success')
    except Exception as e:
        flash('Error al editar el usuario.', 'danger')
        
    return redirect(url_for('user_html.usuarios'))

@user_html.route('/usuarios/delete/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    if session.get('rol') != 'Administrador':
        return redirect(url_for('user_html.login'))
        
    try:
        # El servicio ahora intenta la eliminación lógica si la física falla
        exito = user_service.delete_user(usuario_id)
        if exito:
            flash('Usuario eliminado físicamente.', 'success')
        else:
            flash('No se pudo eliminar físicamente (puede tener ventas asociadas). El usuario ha sido desactivado.', 'warning')
    except Exception as e:
        flash('Error al intentar eliminar/desactivar el usuario.', 'danger')
        
    return redirect(url_for('user_html.usuarios'))

# ============================================================================
# RUTAS PARA RECUPERACIÓN DE CONTRASEÑA (VISUALIZACIÓN INICIAL)
# ============================================================================

@user_html.route('/reset-password', methods=['GET', 'POST'])
def request_reset():
    """
    Paso 1 del reseteo: Muestra el formulario para que el usuario
    ingrese su correo electrónico.
    """
    # La lógica POST se implementará más adelante.
    return render_template('request_reset.html')


@user_html.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Paso 2 del reseteo: El usuario llega aquí desde el enlace en su correo.
    Muestra el formulario para ingresar la nueva contraseña.
    """
    # La lógica para validar el token y actualizar la contraseña se implementará más adelante.
    return render_template('reset_password.html')

