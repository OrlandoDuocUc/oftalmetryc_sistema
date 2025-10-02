from app.domain.models.sale import Sale
from app.domain.models.products import Product
from app.infraestructure.repositories.sql_sale_repository import SQLSaleRepository
from app.infraestructure.repositories.sql_product_repository import SQLProductRepository
from app.infraestructure.utils.db_session import get_db_session, close_db_session
from app.infraestructure.utils.date_utils import get_chile_date, get_day_start_end_chile, format_datetime_chile
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta, date

class SaleService:
    def __init__(self):
        # Los repositorios se crearán con sesiones cuando sea necesario
        pass

    def _get_repositories(self):
        """Obtiene una sesión de base de datos y crea los repositorios"""
        db_session = get_db_session()
        sale_repository = SQLSaleRepository(db_session)
        product_repository = SQLProductRepository(db_session)
        return db_session, sale_repository, product_repository

    def register_sale(self, producto_id, usuario_id, cantidad, total, cliente_id=None):
        # RF-05, RF-08: Registrar venta
        db_session, sale_repository, product_repository = self._get_repositories()
        try:
            product = product_repository.get_by_id(producto_id)
            if not product or product.stock < cantidad:
                return None  # Stock insuficiente o producto no existe
            
            sale = Sale(
                producto_id=producto_id, 
                usuario_id=usuario_id, 
                cantidad=cantidad, 
                total=total, 
                cliente_id=cliente_id  # Puede ser None
            )
            saved_sale = sale_repository.save(sale)
            if saved_sale:
                # RF-02, RF-07: Actualizar stock automáticamente
                product.stock -= cantidad
                product_repository.save(product)
                
                # Devolver solo el ID de la venta
                return saved_sale.venta_id
            return None
        finally:
            close_db_session(db_session)

    def get_sale(self, venta_id):
        db_session, sale_repository, _ = self._get_repositories()
        try:
            return sale_repository.get_by_id(venta_id)
        finally:
            close_db_session(db_session)

    def get_all_sales(self):
        db_session, sale_repository, _ = self._get_repositories()
        try:
            return sale_repository.get_all()
        finally:
            close_db_session(db_session)

    def get_all_sales_with_details(self):
        """Obtiene todas las ventas con información completa de productos y clientes"""
        db_session, sale_repository, _ = self._get_repositories()
        try:
            from app.domain.models.cliente import Cliente
            
            # Obtener ventas con joins para productos y clientes
            sales = db_session.query(Sale).join(Product, Sale.producto_id == Product.producto_id).all()
            
            # Crear lista con información completa
            sales_with_details = []
            for sale in sales:
                # Obtener información del producto
                product = db_session.query(Product).filter_by(producto_id=sale.producto_id).first()
                
                # Obtener información del cliente si existe
                cliente_nombre = "Sin cliente"
                if sale.cliente_id is not None:
                    cliente = db_session.query(Cliente).filter_by(cliente_id=sale.cliente_id).first()
                    if cliente:
                        # Extraer los datos del cliente antes de que se cierre la sesión
                        cliente_nombre = f"{cliente.nombres} {cliente.ap_pat}"
                
                sales_with_details.append({
                    'venta_id': sale.venta_id,
                    'producto_nombre': product.nombre if product else 'Producto no encontrado',
                    'cantidad': sale.cantidad,
                    'total': sale.total,
                    'cliente': cliente_nombre,
                    'fecha': format_datetime_chile(sale.fecha)
                })
            
            return sales_with_details
        finally:
            close_db_session(db_session)

    def get_sales_by_user(self, usuario_id):
        db_session, sale_repository, _ = self._get_repositories()
        try:
            return sale_repository.get_by_user(usuario_id)
        finally:
            close_db_session(db_session)

    def delete_sale(self, venta_id):
        db_session, sale_repository, _ = self._get_repositories()
        try:
            return sale_repository.delete(venta_id)
        finally:
            close_db_session(db_session)

    def get_sales_by_date(self, fecha):
        """Obtiene todas las ventas de una fecha específica en zona horaria de Chile"""
        db_session, sale_repository, _ = self._get_repositories()
        try:
            # Convertir fecha a datetime para comparar
            if isinstance(fecha, str):
                fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
            
            # Obtener inicio y fin del día en zona horaria de Chile
            start_of_day, end_of_day = get_day_start_end_chile(fecha)
            
            # Obtener ventas del día
            sales = db_session.query(Sale).filter(
                Sale.fecha >= start_of_day,
                Sale.fecha < end_of_day
            ).all()
            
            return sales
        finally:
            close_db_session(db_session)

    def get_dashboard_stats(self):
        """Obtiene estadísticas para el dashboard usando zona horaria de Chile"""
        db_session, sale_repository, _ = self._get_repositories()
        try:
            from app.domain.models.products import Product
            
            # Obtener productos en stock
            productos = db_session.query(Product).all()
            productos_en_stock = 0
            productos_stock_bajo = []
            
            for p in productos:
                stock = getattr(p, 'stock', None)
                if stock is not None and stock > 0:
                    productos_en_stock += 1
                    if stock < 10:
                        productos_stock_bajo.append({
                            'nombre': getattr(p, 'nombre', 'Sin nombre'),
                            'stock': stock
                        })
            
            # Obtener ventas del día actual en zona horaria de Chile
            hoy_chile = get_chile_date()
            start_of_day, end_of_day = get_day_start_end_chile(hoy_chile)
            
            ventas_hoy = db_session.query(Sale).filter(
                Sale.fecha >= start_of_day,
                Sale.fecha < end_of_day
            ).all()
            
            total_ventas_hoy = sum(float(getattr(v, 'total', 0)) for v in ventas_hoy if getattr(v, 'total', None) is not None)
            
            # Obtener ventas recientes
            ventas_recientes = db_session.query(Sale).order_by(Sale.fecha.desc()).limit(5).all()
            
            return {
                'productos_en_stock': productos_en_stock,
                'total_ventas_hoy': total_ventas_hoy,
                'productos_stock_bajo': productos_stock_bajo,
                'ventas_recientes': ventas_recientes
            }
            
        finally:
            close_db_session(db_session) 