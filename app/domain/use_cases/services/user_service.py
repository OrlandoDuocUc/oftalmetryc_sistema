from app.domain.models.user import User
from app.domain.models.rol import Rol
from app.infraestructure.repositories.sql_user_repository import SQLUserRepository
from werkzeug.security import generate_password_hash, check_password_hash
from app.infraestructure.utils.db import SessionLocal

class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or SQLUserRepository()

    def register_user(self, nombre, ap_pat, ap_mat, usuario, email, password, rol='vendedor'):
        password_hash = generate_password_hash(password)
        db_session = SessionLocal()
        try:
            rol_obj = db_session.query(Rol).filter(Rol.nombre.ilike(rol)).first()
            if not rol_obj:
                raise ValueError(f"Rol '{rol}' no encontrado en la base de datos")
            user = User(nombre=nombre, ap_pat=ap_pat, ap_mat=ap_mat, username=usuario, email=email, password=password_hash, rol_id=rol_obj.rol_id)
            user_repo = SQLUserRepository(db_session)
            return user_repo.save(user)
        finally:
            db_session.close()

    def authenticate(self, usuario, password):
        db_session = SessionLocal()
        try:
            user_repo = SQLUserRepository(db_session)
            user = user_repo.get_by_username(usuario)
            if user and check_password_hash(getattr(user, 'password', ''), password):
                if getattr(user, 'estado', '') == 'A':
                    return user
                else:
                    return 'inactivo'
            return None
        finally:
            db_session.close()

    def get_user(self, user_id):
        db_session = SessionLocal()
        try:
            user_repo = SQLUserRepository(db_session)
            return user_repo.get_by_id(user_id)
        finally:
            db_session.close()

    def get_all_users(self):
        db_session = SessionLocal()
        try:
            user_repo = SQLUserRepository(db_session)
            return user_repo.get_all()
        finally:
            db_session.close()

    def update_user(self, user_id, **kwargs):
        db_session = SessionLocal()
        try:
            user_repo = SQLUserRepository(db_session)
            user = user_repo.get_by_id(user_id)
            if not user:
                return None
            for key, value in kwargs.items():
                if key == 'password':
                    setattr(user, 'password', generate_password_hash(value))
                elif hasattr(user, key):
                    setattr(user, key, value)
            return user_repo.save(user)
        finally:
            db_session.close()

    def delete_user(self, user_id):
        db_session = SessionLocal()
        try:
            user_repo = SQLUserRepository(db_session)
            return user_repo.delete(user_id)
        finally:
            db_session.close()
