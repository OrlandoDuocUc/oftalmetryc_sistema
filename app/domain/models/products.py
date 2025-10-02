from sqlalchemy import Column, BigInteger, String, DateTime, CHAR, Integer, Float
from app.infraestructure.utils.tables import Base
from datetime import datetime

class Product(Base):
    __tablename__ = 'producto'

    producto_id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    stock = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=True)
    estado = Column(String(20), default='activo')  # 'activo' o 'eliminado'

    def __repr__(self):
        return f"<Product(nombre={self.nombre}, stock={self.stock}, estado={self.estado})>"
