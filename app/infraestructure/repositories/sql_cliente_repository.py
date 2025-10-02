from app.domain.models.cliente import Cliente
from app.infraestructure.utils.db import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

class SQLClienteRepository:
    def __init__(self, db_session=None):
        self.db_session = db_session or SessionLocal()

    def get_by_id(self, cliente_id):
        return self.db_session.query(Cliente).filter_by(cliente_id=cliente_id).first()

    def get_all(self):
        return self.db_session.query(Cliente).all()

    def save(self, cliente):
        try:
            self.db_session.add(cliente)
            self.db_session.commit()
            return cliente
        except SQLAlchemyError:
            self.db_session.rollback()
            return None

    def delete(self, cliente_id):
        cliente = self.get_by_id(cliente_id)
        if cliente:
            self.db_session.delete(cliente)
            self.db_session.commit()
            return True
        return False 