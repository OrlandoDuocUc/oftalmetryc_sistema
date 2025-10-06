from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Date
from sqlalchemy.orm import relationship
from app.infraestructure.utils.tables import Base
from datetime import datetime

class Cliente(Base):
    __tablename__ = 'clientes'

    cliente_id = Column(Integer, primary_key=True, autoincrement=True)
    nombres = Column(String(100), nullable=False)
    ap_pat = Column(String(100), nullable=False)
    ap_mat = Column(String(100), nullable=True)
    rut = Column(String(20), nullable=False)
    email = Column(String(120), nullable=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(Text, nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=True)
    estado = Column(Boolean, default=True, nullable=True)

    # Relación con paciente médico
    paciente_medico = relationship("PacienteMedico", back_populates="cliente", uselist=False)

    def __repr__(self):
        return f"<Cliente(nombres={self.nombres}, ap_pat={self.ap_pat}, estado={self.estado})>" 