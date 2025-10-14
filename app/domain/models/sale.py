# app/domain/models/sale.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.infraestructure.utils.tables import Base
from datetime import datetime

class Sale(Base):
    __tablename__ = 'ventas'

    venta_id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.cliente_id'), nullable=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'), nullable=True)  # vendedor
    fecha_venta = Column(DateTime, default=datetime.utcnow, nullable=True)
    total = Column(Numeric, nullable=False)
    descuento = Column(Numeric, nullable=True)
    metodo_pago = Column(String(50), nullable=True)
    observaciones = Column(Text, nullable=True)
    estado = Column(String(20), nullable=True)

    # Relaciones (EAGER por defecto para evitar DetachedInstanceError en templates)
    detalles = relationship(
        "SaleDetail",
        back_populates="venta",
        cascade="all, delete-orphan",
        lazy="selectin"          # carga la colección en un SELECT IN, apto para templates
    )

    # Nombres de clases REALES en tu app: Cliente y User
    cliente = relationship("Cliente", backref="ventas", lazy="joined")
    usuario = relationship("User", backref="ventas", lazy="joined")

    @property
    def fecha(self):
        return self.fecha_venta

    def __repr__(self):
        return (
            f"<Sale(venta_id={self.venta_id}, cliente_id={self.cliente_id}, "
            f"total={self.total}, fecha_venta={self.fecha_venta})>"
        )


class SaleDetail(Base):
    __tablename__ = 'detalle_ventas'

    detalle_id = Column(Integer, primary_key=True, autoincrement=True)
    venta_id = Column(Integer, ForeignKey('ventas.venta_id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.producto_id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric, nullable=False)
    subtotal = Column(Numeric, nullable=False)

    # Relaciones
    venta = relationship("Sale", back_populates="detalles")
    # Clase real de productos en tu app es Product (no "Producto")
    producto = relationship("Product", lazy="joined")

    def __repr__(self):
        return (
            f"<SaleDetail(detalle_id={self.detalle_id}, venta_id={self.venta_id}, "
            f"producto_id={self.producto_id}, cantidad={self.cantidad})>"
        )
