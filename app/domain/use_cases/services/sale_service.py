from app.domain.models.sale import Sale
from app.domain.models.cliente import Cliente
from app.infraestructure.repositories.sql_sale_repository import SQLSaleRepository
from app.infraestructure.repositories.sql_product_repository import SQLProductRepository
from app.infraestructure.utils.db import SessionLocal
from app.infraestructure.utils.date_utils import get_chile_date, get_day_start_end_chile
from sqlalchemy.exc import SQLAlchemyError

class SaleService:
    def _execute_with_session(self, operation):
        """Maneja la creación y cierre de sesión para cualquier operación."""
        with SessionLocal() as db_session:
            try:
                # Pasa la sesión a los repositorios
                sale_repo = SQLSaleRepository(db_session)
                product_repo = SQLProductRepository(db_session)
                # Ejecuta la operación
                result = operation(sale_repo, product_repo)
                return result
            except Exception as e:
                db_session.rollback()
                print(f"Error en la operación del servicio de ventas: {e}")
                raise e

    def register_sale_from_cart(self, cart_items, usuario_id, cliente_data):
        """Registra una venta completa a partir del carrito y los datos del cliente."""
        def operation(sale_repo, product_repo):
            cliente_id = None
            # 1. Crear o encontrar al cliente
            if cliente_data.get('nombres') and cliente_data.get('ap_pat'):
                # Idealmente, esto debería estar en un ClienteService
                cliente = Cliente(**cliente_data)
                sale_repo.db.add(cliente)
                sale_repo.db.flush() # Para obtener el ID del cliente antes del commit
                cliente_id = cliente.cliente_id

            ventas_creadas_ids = []
            # 2. Registrar cada item del carrito como una venta
            for item in cart_items:
                product = product_repo.get_by_id(item['producto_id'])
                if not product or product.stock < item['cantidad']:
                    raise ValueError(f"Stock insuficiente para el producto {item['nombre']}.")

                sale = Sale(
                    producto_id=item['producto_id'],
                    usuario_id=usuario_id,
                    cantidad=item['cantidad'],
                    total=item['subtotal'],
                    cliente_id=cliente_id
                )
                saved_sale = sale_repo.save(sale)
                ventas_creadas_ids.append(saved_sale.venta_id)

                # 3. Actualizar el stock del producto
                product.stock -= item['cantidad']
                product_repo.save(product)
            
            # Si todo salió bien, el 'with' de la sesión hará commit.
            return ventas_creadas_ids[0] if ventas_creadas_ids else None

        return self._execute_with_session(operation)

    def get_sale_details_for_receipt(self, venta_id):
        """Obtiene todos los detalles necesarios para generar una boleta."""
        def operation(sale_repo, product_repo):
            return sale_repo.get_by_id(venta_id)
        return self._execute_with_session(operation)

    def get_all_sales_with_details(self):
        """Obtiene el historial de todas las ventas con sus detalles."""
        def operation(sale_repo, product_repo):
            return sale_repo.get_all_with_details()
        return self._execute_with_session(operation)

    def get_dashboard_stats(self):
        """Obtiene las estadísticas para el dashboard principal."""
        def operation(sale_repo, product_repo):
            all_products = product_repo.get_all(include_deleted=False)
            
            total_stock = sum(p.stock for p in all_products if p.stock)
            productos_stock_bajo = [p for p in all_products if p.stock is not None and p.stock <= 10]
            
            hoy_chile = get_chile_date()
            start_of_day, end_of_day = get_day_start_end_chile(hoy_chile)
            ventas_hoy = sale_repo.db.query(Sale).filter(Sale.fecha_venta >= start_of_day, Sale.fecha_venta < end_of_day).all()
            total_ventas_hoy = sum(float(v.total) for v in ventas_hoy if v.total is not None)
            
            ventas_recientes = sale_repo.get_all_with_details()[:5]
            
            return {
                'total_stock': total_stock,
                'productos_stock_bajo': productos_stock_bajo,
                'total_ventas_hoy': total_ventas_hoy,
                'ventas_recientes': ventas_recientes
            }
        return self._execute_with_session(operation)

