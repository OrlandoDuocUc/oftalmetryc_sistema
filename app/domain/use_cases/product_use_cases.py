from app.domain.models.products import Product
from app.infraestructure.repositories.sql_product_repository import SQLProductRepository
from app.infraestructure.utils.db import SessionLocal
from app.infraestructure.utils.exceptions import ProductCreationError
from sqlalchemy.exc import SQLAlchemyError

class ProductUseCases:
    def __init__(self, product_repo):
        self.product_repo = product_repo

    def list_products(self):
        """Returns all products."""
        products = self.product_repo.get_all()
        # Filtrar solo productos activos y asegurar que stock sea int
        productos_activos = []
        for p in products:
            if str(p.estado).lower() in ['a', 'activo']:
                p.stock = int(p.stock)
                productos_activos.append(p)
        return productos_activos

    def get_product(self, product_id):
        """Returns a product by its ID."""
        product = self.product_repo.get_by_id(product_id)
        return self._to_domain(product) if product else None

    def create_product(self, data):
        """Creates a new product and saves it to the repository."""
        try:
            # Data validation
            required_fields = ['nombre', 'descripcion', 'precio_unitario', 'stock']
            if not all(key in data for key in required_fields):
                raise ValueError(f"Missing required fields: {', '.join([key for key in required_fields if key not in data])}")

            # Validating that fields are not empty or invalid
            if not data['nombre'] or not data['descripcion']:
                raise ValueError("Product name and description cannot be empty.")
            
            if data['precio_unitario'] <= 0:
                raise ValueError("Price must be greater than zero.")
            
            if data['stock'] < 0:
                raise ValueError("Stock cannot be negative.")

            # Create product instance
            product = Product(
                nombre=data['nombre'],
                descripcion=data['descripcion'],
                precio_unitario=data['precio_unitario'],
                stock=data['stock'],
                estado=data.get('estado', 'A')  # Default to 'A' if not provided
            )
            print(f"Creating product with data: {data}")

            # Save to the repository (assuming product_repo is an object with save method)
            saved = self.product_repo.save(product)
            
            if not saved:
                raise ProductCreationError("Failed to create product")

            return self._to_domain(saved)

        except ValueError as ve:
            raise ProductCreationError(f"Validation error: {ve}") from ve
        except SQLAlchemyError as e:
            raise ProductCreationError(f"Database error creating product: {e}") from e
        except Exception as e:
            raise ProductCreationError(f"Error creating product: {e}") from e


    def update_product(self, product_id, data):
        """Updates an existing product."""
        existing = self.product_repo.get_by_id(product_id)
        if not existing:
            return None

        # Update fields
        updated = Product(
            producto_id=existing.producto_id,
            nombre=data.get("nombre", existing.nombre),
            descripcion=data.get("descripcion", existing.descripcion),
            precio_unitario=data.get("precio_unitario", existing.precio_unitario),
            stock=data.get("stock", existing.stock)
        )

        # Save updated product
        saved = self.product_repo.save(updated)
        return self._to_domain(saved)

    def list_deleted_products(self):
        """Devuelve todos los productos eliminados lógicamente."""
        products = self.product_repo.get_deleted()
        return [self._to_domain(p) for p in products]

    def restore_product(self, product_id):
        """Restaura un producto eliminado lógicamente."""
        return self.product_repo.restore(product_id)

    def delete_product(self, product_id):
        """Elimina lógicamente un producto por su ID."""
        return self.product_repo.delete(product_id)

    def _to_domain(self, product_model):
        """Convierte un modelo SQLAlchemy en un objeto de dominio."""
        return Product(
            producto_id=product_model.producto_id,
            nombre=product_model.nombre,
            descripcion=product_model.descripcion,
            precio_unitario=product_model.precio_unitario,
            stock=product_model.stock,
            estado=getattr(product_model, 'estado', 'activo')
        )
