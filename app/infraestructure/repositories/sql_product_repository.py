from app.domain.models.products import Product
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

class SQLProductRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all(self, include_deleted=False, only_deleted=False):
        """Obtiene productos usando SQLAlchemy ORM para más eficiencia."""
        query = self.db.query(Product)
        if only_deleted:
            return query.filter(Product.estado == False).all()
        if not include_deleted:
            return query.filter(Product.estado == True).all()
        return query.all()

    def get_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.producto_id == product_id).first()

    def save(self, product: Product):
        """Guarda un producto, ya sea creando uno nuevo o actualizando uno existente."""
        try:
            # Si el objeto ya tiene una sesión, se actualizará; si es nuevo, se añadirá.
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
            return product
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, product_id: int):
        """Intenta eliminar físicamente. Si falla, hace una eliminación lógica."""
        product = self.get_by_id(product_id)
        if product:
            try:
                # Intento de eliminación física
                self.db.delete(product)
                self.db.commit()
                return True
            except Exception:
                # Fallback a eliminación lógica si hay dependencias (ej. ventas)
                self.db.rollback()
                product.estado = False
                self.db.commit()
                return False
        return None

    def restore(self, product_id: int):
        """Restaura un producto que fue eliminado lógicamente."""
        product = self.get_by_id(product_id)
        if product and product.estado == False:
            product.estado = True
            self.db.commit()
            return True
        return False

    def update_stock(self, product_id: int, new_stock: int):
        """Actualiza solo el stock de un producto."""
        product = self.get_by_id(product_id)
        if product:
            product.stock = new_stock
            self.db.commit()
            return True
        return False
