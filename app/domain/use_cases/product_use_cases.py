from app.domain.models.products import Product
from app.infraestructure.repositories.sql_product_repository import SQLProductRepository
from app.infraestructure.utils.db import SessionLocal
from app.infraestructure.utils.exceptions import ProductCreationError
from sqlalchemy.exc import SQLAlchemyError

class ProductUseCases:
    def __init__(self):
        # El servicio ya no recibe un repositorio, lo gestiona internamente.
        pass

    def _execute_with_session(self, operation):
        """Maneja la creación y cierre de sesión para cualquier operación."""
        with SessionLocal() as db_session:
            try:
                repo = SQLProductRepository(db_session)
                result = operation(repo)
                return result
            except SQLAlchemyError as e:
                db_session.rollback()
                # Puedes loggear el error aquí si quieres
                raise e

    def list_products(self):
        """Devuelve todos los productos activos."""
        def operation(repo):
            return repo.get_all(include_deleted=False)
        return self._execute_with_session(operation)

    def get_product(self, product_id):
        """Devuelve un producto por su ID."""
        def operation(repo):
            return repo.get_by_id(product_id)
        return self._execute_with_session(operation)

    def create_product(self, data):
        """Crea un nuevo producto."""
        def operation(repo):
            # Validaciones de negocio
            if not data.get('nombre') or data.get('precio_unitario', 0) <= 0 or data.get('stock', -1) < 0:
                raise ValueError("Nombre, precio positivo y stock no negativo son requeridos.")
            
            product = Product(
                nombre=data['nombre'],
                descripcion=data.get('descripcion', ''),
                precio_unitario=data['precio_unitario'],
                stock=data['stock'],
                categoria=data.get('categoria'),
                marca=data.get('marca'),
                sku=data.get('sku'),
                estado=True
            )
            return repo.save(product)
        return self._execute_with_session(operation)

    def update_product(self, product_id, data):
        """Actualiza un producto existente."""
        def operation(repo):
            product = repo.get_by_id(product_id)
            if not product:
                return None
            
            # Actualiza solo los campos proporcionados en 'data'
            for key, value in data.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            
            return repo.save(product)
        return self._execute_with_session(operation)

    def list_deleted_products(self):
        """Devuelve todos los productos eliminados lógicamente."""
        def operation(repo):
            return repo.get_all(include_deleted=True, only_deleted=True)
        return self._execute_with_session(operation)

    def restore_product(self, product_id):
        """Restaura un producto eliminado lógicamente."""
        def operation(repo):
            return repo.restore(product_id)
        return self._execute_with_session(operation)

    def delete_product(self, product_id):
        """Elimina (lógica o físicamente) un producto por su ID."""
        def operation(repo):
            return repo.delete(product_id)
        return self._execute_with_session(operation)
