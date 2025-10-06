from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship  # <-- PASO 1: Importar 'relationship'
from app.infraestructure.utils.tables import Base
from datetime import datetime

class Rol(Base):
    __tablename__ = 'roles'

    rol_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=True)
    estado = Column(Boolean, default=True, nullable=True)

    # --- PASO 2: AÑADIR LA RELACIÓN INVERSA ---
    # Esto permite que en el futuro puedas hacer 'rol.usuarios' para ver todos los usuarios de un rol.
    usuarios = relationship("User", back_populates="rol")

    def __repr__(self):
        return f"<Rol(nombre={self.nombre}, descripcion={self.descripcion}, estado={self.estado})>"
