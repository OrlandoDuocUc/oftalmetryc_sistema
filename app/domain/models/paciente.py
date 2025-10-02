from sqlalchemy import Column, Integer, String, Date, Text, DateTime, func
from app.infraestructure.utils.tables import Base
from datetime import datetime

class Paciente(Base):
    __tablename__ = 'pacientes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rut = Column(String(12), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date)
    telefono = Column(String(20))
    email = Column(String(100))
    direccion = Column(Text)
    ocupacion = Column(String(100))
    contacto_emergencia = Column(String(100))
    telefono_emergencia = Column(String(20))
    observaciones = Column(Text)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Paciente(rut={self.rut}, nombre={self.nombre}, apellido={self.apellido})>"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'rut': self.rut,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'nombre_completo': self.nombre_completo,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'ocupacion': self.ocupacion,
            'contacto_emergencia': self.contacto_emergencia,
            'telefono_emergencia': self.telefono_emergencia,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }