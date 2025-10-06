from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text
from app.infraestructure.utils.tables import Base
from datetime import datetime

class Sale(Base):
    __tablename__ = 'ventas'

    venta_id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.cliente_id'), nullable=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'), nullable=True)  # Vendedor
    fecha_venta = Column(DateTime, default=datetime.utcnow, nullable=True)
    total = Column(Numeric, nullable=False)
    descuento = Column(Numeric, nullable=True)
    metodo_pago = Column(String(50), nullable=True)
    observaciones = Column(Text, nullable=True)
    estado = Column(String(20), nullable=True)

    # Alias para compatibilidad con código existente
    @property
    def fecha(self):
        return self.fecha_venta
    estado = Column(String(20), nullable=True)

    def __repr__(self):
        return f"<Sale(venta_id={self.venta_id}, cliente_id={self.cliente_id}, total={self.total}, fecha_venta={self.fecha_venta})>"

class SaleDetail(Base):
    __tablename__ = 'detalle_ventas'

    detalle_id = Column(Integer, primary_key=True, autoincrement=True)
    venta_id = Column(Integer, ForeignKey('ventas.venta_id'), nullable=True)
    producto_id = Column(Integer, ForeignKey('productos.producto_id'), nullable=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric, nullable=False)
    subtotal = Column(Numeric, nullable=False)

    def __repr__(self):
        return f"<SaleDetail(detalle_id={self.detalle_id}, venta_id={self.venta_id}, producto_id={self.producto_id}, cantidad={self.cantidad})>" 