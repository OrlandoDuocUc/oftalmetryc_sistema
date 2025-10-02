from app.domain.models.sale import Sale
from app.infraestructure.utils.db import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

class SQLSaleRepository:
    def __init__(self, db_session=None):
        self.db_session = db_session or SessionLocal()

    def get_by_id(self, venta_id):
        return self.db_session.query(Sale).filter_by(venta_id=venta_id).first()

    def get_all(self):
        return self.db_session.query(Sale).all()

    def get_by_user(self, usuario_id):
        return self.db_session.query(Sale).filter_by(usuario_id=usuario_id).all()

    def save(self, sale):
        try:
            self.db_session.add(sale)
            self.db_session.commit()
            return sale
        except SQLAlchemyError:
            self.db_session.rollback()
            return None

    def delete(self, venta_id):
        sale = self.get_by_id(venta_id)
        if sale:
            self.db_session.delete(sale)
            self.db_session.commit()
            return True
        return False 