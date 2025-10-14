# sale_service.py
from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

from app.domain.models.sale import Sale, SaleDetail
from app.domain.models.cliente import Cliente
from app.infraestructure.repositories.sql_sale_repository import SQLSaleRepository
from app.infraestructure.repositories.sql_product_repository import SQLProductRepository
from app.infraestructure.utils.db import SessionLocal


def q2(value) -> Decimal:
    """Redondeo financiero a 2 decimales."""
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class SaleService:
    def _execute_with_session(self, operation):
        with SessionLocal() as db_session:
            try:
                sale_repo = SQLSaleRepository(db_session)
                product_repo = SQLProductRepository(db_session)
                result = operation(db_session, sale_repo, product_repo)
                return result
            except Exception as e:
                db_session.rollback()
                print(f"Error en la operación del servicio de ventas: {e}")
                raise e

    def register_sale_from_cart(
        self,
        cart_items,
        usuario_id,
        cliente_data=None,
        metodo_pago=None,
        observaciones=None,
        descuento=0,
    ):
        """
        Crea (opcional) el Cliente, registra una Venta y sus Detalles,
        descuenta stock con bloqueo de fila y hace UN SOLO commit al final.

        Seguridad:
        - No confiamos en subtotales del frontend: tomamos precio desde BD.
        - Bloqueo FOR UPDATE por producto.
        - CHECK (stock >= 0) actúa de red mínima si hay carreras.
        """
        cliente_data = cliente_data or {}

        def operation(db, sale_repo, product_repo):
            cliente_id = None

            # 1) Crear/usar cliente si se proporcionó RUC/Cédula (campo 'rut' en backend)
            rut = (cliente_data.get("rut") or "").strip()
            if rut:
                existing = db.query(Cliente).filter(Cliente.rut == rut).first()
                if existing:
                    cliente_id = existing.cliente_id
                else:
                    nuevo = Cliente(
                        rut=rut,
                        nombres=cliente_data.get("nombres") or "",
                        ap_pat=cliente_data.get("ap_pat") or "",
                        ap_mat=cliente_data.get("ap_mat") or "",
                        telefono=cliente_data.get("telefono"),
                        email=cliente_data.get("email"),
                        direccion=cliente_data.get("direccion"),
                        estado=True,
                    )
                    db.add(nuevo)
                    db.flush()
                    cliente_id = nuevo.cliente_id

            # 2) Crear la venta con total provisional 0 (necesitamos venta_id para los detalles)
            venta = Sale(
                cliente_id=cliente_id,
                usuario_id=usuario_id,
                total=Decimal("0.00"),
                descuento=q2(descuento or 0),
                metodo_pago=metodo_pago,
                observaciones=observaciones,
                estado="completada",
            )
            db.add(venta)
            db.flush()  # obtener venta.venta_id

            # 3) Crear detalles + descontar stock con bloqueo; calcular TOTAL REAL desde BD
            total_real = Decimal("0.00")

            for it in cart_items:
                producto_id = int(it["producto_id"])
                cantidad = int(it.get("cantidad", 0) or 0)
                if cantidad <= 0:
                    continue

                # Bloquea la fila del producto (FOR UPDATE) para evitar overselling
                prod = product_repo.get_by_id(producto_id, for_update=True)
                if not prod:
                    raise ValueError(f"Producto ID {producto_id} no existe.")

                stock_actual = int(prod.stock or 0)
                if stock_actual < cantidad:
                    raise ValueError(f"Stock insuficiente para el producto {getattr(prod, 'nombre', 'N/D')}.")

                # Precio desde BD (no confiamos en el cliente)
                precio = q2(prod.precio_unitario or 0)
                subtotal = q2(precio * cantidad)

                detalle = SaleDetail(
                    venta_id=venta.venta_id,
                    producto_id=prod.producto_id,
                    cantidad=cantidad,
                    precio_unitario=precio,
                    subtotal=subtotal,
                )
                db.add(detalle)

                # Descontar stock (sin commit, solo flush dentro de la misma transacción)
                prod.stock = stock_actual - cantidad
                # Como el objeto ya está en la sesión, basta con flushear;
                # usamos el repo por consistencia (no comitea).
                product_repo.save(prod, commit=False)

                total_real += subtotal

            # Aplicar descuento al total (si corresponde)
            venta.total = q2(total_real)

            try:
                # 4) Un solo commit para toda la operación
                db.commit()
            except IntegrityError as ie:
                db.rollback()
                # Si el CHECK (stock >= 0) u otra condición salta por carrera
                raise ValueError("No se pudo completar la venta por cambios concurrentes en stock. Intenta nuevamente.") from ie

            return venta.venta_id

        return self._execute_with_session(operation)

    def get_sale_details_for_receipt(self, venta_id):
        """
        Devuelve la venta con relaciones cargadas (eager) para evitar DetachedInstanceError
        al renderizar en templates fuera del contexto de sesión.
        """
        def operation(db, sale_repo, product_repo):
            venta = (
                db.query(Sale)
                .options(
                    joinedload(Sale.usuario),
                    joinedload(Sale.cliente),
                    joinedload(Sale.detalles).joinedload(SaleDetail.producto),
                )
                .filter(Sale.venta_id == venta_id)
                .first()
            )
            return venta

        return self._execute_with_session(operation)

    def get_all_sales_with_details(self):
        def operation(db, sale_repo, product_repo):
            ventas = (
                db.query(Sale)
                .options(
                    joinedload(Sale.usuario),
                    joinedload(Sale.cliente),
                    joinedload(Sale.detalles).joinedload(SaleDetail.producto),
                )
                .order_by(Sale.fecha_venta.desc())
                .all()
            )
            return ventas

        return self._execute_with_session(operation)
