from flask import jsonify, Blueprint, render_template, redirect, url_for, request, session, flash
from app.domain.use_cases.services.user_service import UserService

user_html = Blueprint('user_html', __name__)
user_service = UserService()

def get_user_controller(user_service):
    def handler(user_id):
        user = user_service.get_user(int(user_id))
        if user:
            return jsonify({"id": user.id, "name": user.name, "email": user.email})
        return jsonify({"error": "User not found"}), 404
    return handler

@user_html.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        user = user_service.authenticate(usuario, password)
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

@user_html.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user_html.login'))

@user_html.route('/usuarios')
def usuarios():
    # Verificar si hay sesión activa y si es administrador
    user_id = session.get('user_id')
    rol = session.get('rol')
    if not user_id or rol != 'Administrador':
        return redirect(url_for('user_html.login'))
    try:
        users = user_service.get_all_users()
        return render_template('usuarios.html', users=users)
    except Exception as e:
        print(f"Error al cargar usuarios: {e}")
        flash('Ocurrió un error al cargar los usuarios. Intente más tarde.', 'danger')
        return render_template('usuarios.html', users=[])

@user_html.route('/usuarios/toggle/<int:usuario_id>', methods=['POST'])
def toggle_estado_usuario(usuario_id):
    if 'user_id' not in session or 'rol' not in session or session['rol'] != 'Administrador':
        return redirect(url_for('user_html.login'))
    try:
        nuevo_estado = request.args.get('estado')
        if nuevo_estado in ['A', 'I']:
            user_service.update_user(usuario_id, estado=nuevo_estado)
    except Exception as e:
        print(f"Error al cambiar estado de usuario: {e}")
        flash('Ocurrió un error al cambiar el estado del usuario. Intente más tarde.', 'danger')
    return redirect(url_for('user_html.usuarios'))

@user_html.route('/usuarios/edit/<int:usuario_id>', methods=['POST'])
def editar_usuario(usuario_id):
    if 'user_id' not in session or 'rol' not in session or session['rol'] != 'Administrador':
        return redirect(url_for('user_html.login'))
    try:
        data = request.form.to_dict()
        campos_permitidos = ['nombre', 'ap_pat', 'ap_mat', 'username', 'email']
        data = {k: v for k, v in data.items() if k in campos_permitidos}
        user_service.update_user(usuario_id, **data)
    except Exception as e:
        print(f"Error al editar usuario: {e}")
        flash('Ocurrió un error al editar el usuario. Intente más tarde.', 'danger')
    return redirect(url_for('user_html.usuarios'))

@user_html.route('/usuarios/delete/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    if 'user_id' not in session or 'rol' not in session or session['rol'] != 'Administrador':
        return redirect(url_for('user_html.login'))
    try:
        exito = user_service.delete_user(usuario_id)
        if not exito:
            flash('No se puede eliminar el usuario porque tiene ventas asociadas.', 'danger')
    except Exception as e:
        print('Error al eliminar usuario:', str(e))
        flash('Ocurrió un error al eliminar usuario. Intente más tarde.', 'danger')
    return redirect(url_for('user_html.usuarios'))
