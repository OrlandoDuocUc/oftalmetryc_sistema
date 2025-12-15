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
                db_session.commit()  # asegura que insert/update no se deshaga
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
        """Crea un nuevo producto con la nueva estructura de campos."""
        def operation(repo):
            from datetime import datetime
            
            # Validaciones de negocio
            if not data.get('nombre'):
                raise ValueError("El nombre del producto es requerido.")
            if data.get('costo_unitario', 0) <= 0:
                raise ValueError("El costo unitario debe ser mayor a 0.")
            if data.get('cantidad', -1) < 0:
                raise ValueError("La cantidad no puede ser negativa.")
            
            # Crear producto con todos los nuevos campos
            product = Product(
                fecha=data.get('fecha', datetime.now().date()),
                nombre=data['nombre'],
                distribuidor=data.get('distribuidor'),
                marca=data.get('marca'),
                material=data.get('material'),
                tipo_armazon=data.get('tipo_armazon'),
                codigo=data.get('codigo'),
                diametro_1=data.get('diametro_1'),
                diametro_2=data.get('diametro_2'),
                color=data.get('color'),
                cantidad=data.get('cantidad', 0),
                costo_unitario=data['costo_unitario'],
                costo_total=data.get('costo_total'),
                costo_venta_1=data.get('costo_venta_1'),
                costo_venta_2=data.get('costo_venta_2'),
                descripcion=data.get('descripcion'),
                estado=True
            )
            # No hacer commit aquí, lo hace _execute_with_session
            return repo.save(product, commit=False)
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
