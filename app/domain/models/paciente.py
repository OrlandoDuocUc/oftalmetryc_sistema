from sqlalchemy import Column, Integer, String, Date, Text, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.infraestructure.utils.tables import Base
from datetime import datetime

class PacienteMedico(Base):
    __tablename__ = 'pacientes_medicos'

    paciente_medico_id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.cliente_id'), nullable=True)
    numero_ficha = Column(String(20), unique=True, nullable=False)
    antecedentes_medicos = Column(Text)
    antecedentes_oculares = Column(Text)
    alergias = Column(Text)
    medicamentos_actuales = Column(Text)
    contacto_emergencia = Column(String(100))
    telefono_emergencia = Column(String(20))
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)
    estado = Column(Boolean, default=True)

    # Relación con cliente
    cliente = relationship("Cliente", back_populates="paciente_medico")

    def __repr__(self):
        return f"<PacienteMedico(id={self.paciente_medico_id}, numero_ficha={self.numero_ficha})>"

    def to_dict(self):
        return {
            'paciente_medico_id': self.paciente_medico_id,
            'cliente_id': self.cliente_id,
            'numero_ficha': self.numero_ficha,
            'antecedentes_medicos': self.antecedentes_medicos,
            'antecedentes_oculares': self.antecedentes_oculares,
            'alergias': self.alergias,
            'medicamentos_actuales': self.medicamentos_actuales,
            'contacto_emergencia': self.contacto_emergencia,
            'telefono_emergencia': self.telefono_emergencia,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'estado': self.estado
        }

# Alias para compatibilidad
Paciente = PacienteMedico