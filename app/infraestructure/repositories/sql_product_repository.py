from app.domain.models.products import Product
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

class SQLProductRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all(self, include_deleted=False):
        # Usar consulta SQL directa para evitar cacheo
        if include_deleted:
            result = self.db.execute(text("SELECT * FROM producto"))
        else:
            result = self.db.execute(text("SELECT * FROM producto WHERE estado IN ('A', 'a', 'activo', 'ACTIVO')"))
        
        # Convertir resultados a objetos Product
        products = []
        for row in result:
            product = Product()
            product.producto_id = row.producto_id
            product.nombre = row.nombre
            product.descripcion = row.descripcion
            product.stock = row.stock
            product.precio_unitario = row.precio_unitario
            product.fecha_creacion = row.fecha_creacion
            product.estado = row.estado
            products.append(product)
        
        return products

    def get_by_id(self, product_id: int):
        return self.db.query(Product).filter_by(producto_id=product_id).first()

    def get_deleted(self):
        return self.db.query(Product).filter(Product.estado == 'eliminado').all()

    def save(self, product: Product):
        try:
            product_id = getattr(product, 'producto_id', None)
            if product_id is not None:
                # Update existing product
                existing = self.get_by_id(product_id)
                if existing:
                    existing.nombre = product.nombre
                    existing.descripcion = product.descripcion
                    existing.precio_unitario = product.precio_unitario
                    existing.stock = product.stock
                    # Ensure 'estado' is updated if provided, but 'fecha_creacion' should not be changed
                    if product.estado is not None:
                        existing.estado = product.estado
                    self.db.commit()
                    self.db.refresh(existing)
                    return existing
                else:
                    raise ValueError(f"Product with ID {product_id} does not exist.")
            else:
                # Create a new product
                new_product = Product(
                    nombre=product.nombre,
                    descripcion=product.descripcion,
                    precio_unitario=product.precio_unitario,
                    stock=product.stock,
                    estado=product.estado or 'A',  # Default to 'A' if estado is not provided
                    fecha_creacion=product.fecha_creacion or datetime.utcnow()  # Set current time if not provided
                )
                self.db.add(new_product)
                self.db.commit()
                self.db.refresh(new_product)
                return new_product

        except Exception as e:
            # Rollback in case of any error
            self.db.rollback()
            raise e  # Re-raise the exception to handle it at a higher level

    def delete(self, product_id: int):
        product = self.get_by_id(product_id)
        if product is not None:
            try:
                self.db.delete(product)
                self.db.commit()
                return True  # Eliminación física
            except Exception:
                self.db.rollback()
                setattr(product, 'estado', 'eliminado')
                self.db.commit()
                return False  # Eliminación lógica
        return False

    def restore(self, product_id: int):
        product = self.get_by_id(product_id)
        if product is not None and getattr(product, 'estado', None) == 'eliminado':
            setattr(product, 'estado', 'activo')
            self.db.commit()
            return True
        return False
