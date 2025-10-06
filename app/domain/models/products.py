from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Numeric
from app.infraestructure.utils.tables import Base
from datetime import datetime

class Product(Base):
    __tablename__ = 'productos'

    producto_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    stock = Column(Integer, nullable=True)
    precio_unitario = Column(Numeric, nullable=False)
    categoria = Column(String(100), nullable=True)
    marca = Column(String(100), nullable=True)
    sku = Column(String(50), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=True)
    estado = Column(Boolean, default=True, nullable=True)

    def __repr__(self):
        return f"<Product(nombre={self.nombre}, stock={self.stock}, estado={self.estado})>"
