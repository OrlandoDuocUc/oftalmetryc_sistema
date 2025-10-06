# app/domain/models/proveedor.py

from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, DateTime, func
# --- LÍNEA CORREGIDA ---
# Ahora importa 'Base' desde 'tables.py', igual que los demás modelos.
from app.infraestructure.utils.tables import Base

class Proveedor(Base):
    """
    Modelo de dominio para representar un proveedor
    """
    __tablename__ = 'proveedores'
    
    # Identificación única
    proveedor_id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_proveedor = Column(String(20), unique=True)
    
    # Información básica de la empresa
    razon_social = Column(String(255), nullable=False)
    nombre_comercial = Column(String(255), nullable=True)
    rut = Column(String(12), unique=True, nullable=False)
    
    # Información de contacto
    direccion = Column(Text, nullable=True)
    telefono = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    sitio_web = Column(String(255), nullable=True)
    
    # Información comercial
    categoria_productos = Column(Text, nullable=True)
    condiciones_pago = Column(String(50), nullable=False, default='Contado')
    plazo_pago_dias = Column(Integer, nullable=False, default=0)
    descuento_volumen = Column(DECIMAL(5, 2), nullable=False, default=0.00)
    
    # Representante comercial
    representante_nombre = Column(String(255), nullable=True)
    representante_telefono = Column(String(20), nullable=True)
    representante_email = Column(String(100), nullable=True)
    
    # Información adicional
    observaciones = Column(Text, nullable=True)
    
    # Control de estado y fechas
    estado = Column(Boolean, nullable=False, default=True)
    fecha_registro = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    fecha_actualizacion = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    
    def __repr__(self):
        return f"<Proveedor(id={self.proveedor_id}, razon_social='{self.razon_social}')>"