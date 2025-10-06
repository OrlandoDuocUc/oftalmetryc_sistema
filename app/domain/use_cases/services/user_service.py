from app.domain.models.user import User
from app.domain.models.rol import Rol
from app.infraestructure.repositories.sql_user_repository import SQLUserRepository
from werkzeug.security import generate_password_hash, check_password_hash
from app.infraestructure.utils.db import SessionLocal

class UserService:
    def __init__(self):
        """
        El servicio se inicializa con una única instancia del repositorio.
        Este repositorio será reutilizado por todos los métodos del servicio.
        """
        self.user_repository = SQLUserRepository()

    def register_user(self, nombre, ap_pat, ap_mat, username, email, password, rol='vendedor'):
        """
        Registra un nuevo usuario.
        La contraseña se hashea antes de guardarla.
        """
        password_hash = generate_password_hash(password)
        
        # Se necesita una sesión local solo para esta operación específica de buscar el rol.
        db_session = SessionLocal()
        try:
            rol_obj = db_session.query(Rol).filter(Rol.nombre.ilike(rol)).first()
            if not rol_obj:
                raise ValueError(f"Rol '{rol}' no encontrado en la base de datos")
            
            user = User(
                nombre=nombre, 
                ap_pat=ap_pat, 
                ap_mat=ap_mat, 
                username=username, 
                email=email, 
                password=password_hash, 
                rol_id=rol_obj.rol_id
            )
            
            # Se usa la instancia única del repositorio para guardar el usuario.
            return self.user_repository.save(user)
        finally:
            db_session.close()

    def authenticate(self, usuario, password):
        """
        Autentica a un usuario por su nombre de usuario y contraseña.
        Devuelve el objeto User si es exitoso, 'inactivo' si el usuario está inactivo, o None si falla.
        """
        user = self.user_repository.get_by_username(usuario)
        
        if not user or not hasattr(user, 'password') or not user.password:
            return None

        if check_password_hash(user.password, password):
            if getattr(user, 'estado', False) is True:
                return user
            else:
                return 'inactivo'
        return None

    def get_user(self, user_id):
        """
        Obtiene un usuario por su ID.
        """
        return self.user_repository.get_by_id(user_id)

    def get_all_users(self):
        """
        Obtiene todos los usuarios de la base de datos.
        """
        return self.user_repository.get_all()

    def update_user(self, user_id, **kwargs):
        """
        Actualiza los datos de un usuario.
        Si se pasa 'password', se hashea automáticamente.
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if key == 'password':
                setattr(user, 'password', generate_password_hash(value))
            elif hasattr(user, key):
                setattr(user, key, value)
        
        return self.user_repository.save(user)

    def delete_user(self, user_id):
        """
        Realiza un borrado lógico o físico de un usuario.
        """
        return self.user_repository.delete(user_id)
