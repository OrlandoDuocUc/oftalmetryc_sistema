from sqlalchemy import Column, BigInteger, Integer, String, Numeric, DateTime, ForeignKey
from app.infraestructure.utils.tables import Base
from datetime import datetime

class Sale(Base):
    __tablename__ = 'venta'

    venta_id = Column(BigInteger, primary_key=True, autoincrement=True)
    producto_id = Column(BigInteger, ForeignKey('producto.producto_id'), nullable=False)
    usuario_id = Column(BigInteger, ForeignKey('usuario.usuario_id'), nullable=False)  # Vendedor
    cliente_id = Column(BigInteger, ForeignKey('cliente.cliente_id'), nullable=True)  # Cliente
    cantidad = Column(Integer, nullable=False)
    total = Column(Numeric, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Sale(producto_id={self.producto_id}, usuario_id={self.usuario_id}, cantidad={self.cantidad}, total={self.total}, fecha={self.fecha})>" 