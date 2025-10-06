from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship  # <-- PASO 1: Importar 'relationship'
from app.infraestructure.utils.tables import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'usuarios'

    usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    rol_id = Column(Integer, ForeignKey('roles.rol_id'), nullable=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    ap_pat = Column(String(100), nullable=False)
    ap_mat = Column(String(100), nullable=True)
    email = Column(String(120), unique=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=True)
    estado = Column(Boolean, default=True, nullable=True)

    # --- PASO 2: AÑADIR LA RELACIÓN ---
    # Esta línea crea el atributo 'user.rol' que faltaba.
    # 'back_populates' le dice cómo conectarse con el modelo Rol.
    rol = relationship("Rol", back_populates="usuarios")

    def __repr__(self):
        return f"<User(nombre={self.nombre}, username={self.username}, estado={self.estado})>"
