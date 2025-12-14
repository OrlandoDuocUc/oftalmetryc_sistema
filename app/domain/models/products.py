# app/domain/models/products.py
from sqlalchemy import Column, Integer, String, Date, Boolean, Text, Numeric, CheckConstraint
from app.infraestructure.utils.tables import Base
from datetime import date

class Product(Base):
    __tablename__ = 'productos'

    producto_id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, default=date.today, nullable=True)
    nombre = Column(String(200), nullable=False)
    distribuidor = Column(String(200), nullable=True)
    marca = Column(String(100), nullable=True)
    material = Column(String(100), nullable=True)
    tipo_armazon = Column(String(100), nullable=True)
    codigo = Column(String(50), nullable=True)
    diametro_1 = Column(String(50), nullable=True)
    diametro_2 = Column(String(50), nullable=True)
    color = Column(String(100), nullable=True)
    cantidad = Column(Integer, default=0, nullable=True)
    costo_unitario = Column(Numeric(10, 2), nullable=False)
    costo_total = Column(Numeric(10, 2), nullable=True)
    costo_venta_1 = Column(Numeric(10, 2), nullable=True)
    costo_venta_2 = Column(Numeric(10, 2), nullable=True)
    descripcion = Column(Text, nullable=True)
    estado = Column(Boolean, default=True, nullable=True)

    # Propiedades calculadas para compatibilidad con código antiguo
    @property
    def stock(self):
        """Alias para cantidad (compatibilidad)"""
        return self.cantidad
    
    @property
    def precio_unitario(self):
        """Alias para costo_venta_1 (compatibilidad)"""
        return self.costo_venta_1
    
    @property
    def sku(self):
        """Alias para codigo (compatibilidad)"""
        return self.codigo

    # Constraints para protección de datos
    __table_args__ = (
        CheckConstraint('cantidad >= 0', name='ck_productos_cantidad_non_negative'),
        CheckConstraint('costo_unitario >= 0', name='ck_productos_costo_unitario_positive'),
    )

    def __repr__(self):
        return f"<Product(nombre={self.nombre}, codigo={self.codigo}, cantidad={self.cantidad}, estado={self.estado})>"
