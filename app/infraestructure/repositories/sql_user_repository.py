from app.domain.models.user import User
from app.infraestructure.utils.db import SessionLocal
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from typing import Optional

class SQLUserRepository:
    def __init__(self, db_session: Optional[Session] = None):
        self.db_session = db_session

    def _get_session(self):
        """Obtiene la sesión actual o crea una nueva si es necesario"""
        if not self.db_session:
            self.db_session = SessionLocal()
        return self.db_session

    def get_by_id(self, user_id):
        session = self._get_session()
        return session.query(User).filter_by(usuario_id=user_id).first()

    def get_by_username(self, username):
        session = self._get_session()
        return session.query(User).filter_by(username=username).first()

    def get_all(self):
        session = self._get_session()
        return session.query(User).all()

    def save(self, user):
        session = self._get_session()
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error saving user: {e}")
            return None
        finally:
            if not self.db_session:  # Solo cerrar si creamos la sesión aquí
                session.close()

    def delete(self, user_id):
        session = self._get_session()
        user = self.get_by_id(user_id)
        if user:
            try:
                session.delete(user)
                session.commit()
                return True  # Eliminación física
            except IntegrityError:
                session.rollback()
                setattr(user, 'estado', False)
                session.commit()
                return False  # Eliminación lógica
        return False

    def restore(self, user_id):
        session = self._get_session()
        user = self.get_by_id(user_id)
        if user and getattr(user, 'estado', None) == 'I':
            setattr(user, 'estado', 'A')
            session.commit()
            return True
        return False

    def close_session(self):
        """Cierra la sesión si existe"""
        if self.db_session:
            self.db_session.close()
            self.db_session = None 