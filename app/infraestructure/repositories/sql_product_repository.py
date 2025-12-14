from sqlalchemy.orm import Session
from app.domain.models.products import Product


class SQLProductRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    # ---------- Lectura ----------
    def get_all(self, include_deleted: bool = False, only_deleted: bool = False):
        """
        Obtiene productos usando ORM. No hace commit (solo lectura).
        """
        query = self.db.query(Product)
        if only_deleted:
            return query.filter(Product.estado.is_(False)).all()
        if not include_deleted:
            return query.filter(Product.estado.is_(True)).all()
        return query.all()

    def get_by_id(self, product_id: int, for_update: bool = False):
        """
        Obtiene un producto por ID. Si for_update=True, bloquea la fila (SELECT ... FOR UPDATE).
        Útil para operaciones de stock en transacciones concurrentes.
        """
        q = self.db.query(Product).filter(Product.producto_id == product_id)
        if for_update:
            q = q.with_for_update()  # requiere transacción activa (BEGIN implícito)
        return q.first()

    # ---------- Escritura ----------
    def save(self, product: Product, *, commit: bool = False):
        """
        Guarda un producto (insert/update). Por defecto NO hace commit para
        permitir transacciones atómicas a nivel de servicio.
        - commit=False -> solo flush/refresh (deja el commit al servicio)
        - commit=True  -> commit inmediato (para usos fuera de la venta)
        """
        try:
            self.db.add(product)
            self.db.flush()
            self.db.refresh(product)
            if commit:
                self.db.commit()
            return product
        except Exception as e:
            self.db.rollback()
            print(f"Error al guardar producto: {e}")
            raise

    def delete(self, product_id: int, *, commit: bool = True):
        """
        Intenta eliminación física. Si falla (FK, etc.), hace soft-delete.
        commit=True por compatibilidad en usos administrativos.
        """
        product = self.get_by_id(product_id, for_update=True)
        if not product:
            return None

        try:
            self.db.delete(product)
            if commit:
                self.db.commit()
            else:
                self.db.flush()
            return True
        except Exception:
            # Soft delete en caso de restricciones
            self.db.rollback()
            product = self.get_by_id(product_id, for_update=True)
            if not product:
                return None
            product.estado = False
            if commit:
                self.db.commit()
            else:
                self.db.flush()
            return False

    def restore(self, product_id: int, *, commit: bool = True):
        product = self.get_by_id(product_id, for_update=True)
        if product and product.estado is False:
            product.estado = True
            if commit:
                self.db.commit()
            else:
                self.db.flush()
            return True
        return False

    def update_stock(self, product_id: int, new_stock: int, *, commit: bool = False):
        """
        Actualiza stock/cantidad a un valor específico. Usa FOR UPDATE.
        Respeta el CHECK de DB (cantidad >= 0).
        Por defecto NO hace commit para integrarse a transacciones atómicas.
        """
        product = self.get_by_id(product_id, for_update=True)
        if not product:
            return False
        product.cantidad = new_stock  # Usa el nuevo campo cantidad
        if commit:
            self.db.commit()
        else:
            self.db.flush()
        return True

    # ---------- Ayudantes de stock seguros ----------
    def decrement_stock(self, product_id: int, quantity: int, *, commit: bool = False):
        """
        Resta 'quantity' del stock/cantidad con bloqueo de fila (FOR UPDATE).
        No hace commit por defecto para permitir una venta atómica.
        Lanza ValueError si no hay stock suficiente.
        """
        if quantity <= 0:
            return self.get_by_id(product_id)  # no-op

        product = self.get_by_id(product_id, for_update=True)
        if not product:
            raise ValueError(f"Producto ID {product_id} no existe.")

        current = product.cantidad or 0  # Usa el nuevo campo cantidad
        if current < quantity:
            raise ValueError(f"Stock insuficiente para el producto {product.nombre}.")

        product.cantidad = current - quantity  # Usa el nuevo campo cantidad

        self.db.flush()
        if commit:
            self.db.commit()

        return product
