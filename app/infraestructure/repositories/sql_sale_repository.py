from app.domain.models.sale import Sale
from app.domain.models.products import Product
from app.domain.models.user import User
from app.domain.models.cliente import Cliente
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError

class SQLSaleRepository:
    def __init__(self, db_session: Session):
        # El repositorio siempre recibe una sesión activa.
        self.db = db_session

    def get_by_id(self, venta_id: int):
        # Carga la venta y la información relacionada (producto, cliente, usuario) de una vez.
        return self.db.query(Sale).options(
            joinedload(Sale.producto),
            joinedload(Sale.cliente),
            joinedload(Sale.usuario)
        ).filter(Sale.venta_id == venta_id).first()

    def get_all_with_details(self):
        # Obtiene todas las ventas, precargando los datos relacionados para evitar múltiples consultas.
        return self.db.query(Sale).options(
            joinedload(Sale.producto),
            joinedload(Sale.cliente),
            joinedload(Sale.usuario)
        ).order_by(Sale.fecha_venta.desc()).all()

    def get_by_user(self, usuario_id: int):
        return self.db.query(Sale).filter(Sale.usuario_id == usuario_id).all()

    def save(self, sale: Sale):
        try:
            self.db.add(sale)
            self.db.commit()
            self.db.refresh(sale)
            return sale
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete(self, venta_id: int):
        sale = self.get_by_id(venta_id)
        if sale:
            self.db.delete(sale)
            self.db.commit()
            return True
        return False

