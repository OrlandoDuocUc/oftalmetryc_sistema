from sqlalchemy import Column, BigInteger, String, DateTime, CHAR, Text
from app.infraestructure.utils.tables import Base
from datetime import datetime

class Rol(Base):
    __tablename__ = 'rol'

    rol_id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=True)
    estado = Column(CHAR(1), default='A', nullable=False)  # A=Activo, I=Inactivo

    def __repr__(self):
        return f"<Rol(nombre={self.nombre}, descripcion={self.descripcion}, estado={self.estado})>" 