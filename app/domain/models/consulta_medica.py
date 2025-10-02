from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.infraestructure.utils.tables import Base
from datetime import datetime

class ConsultaMedica(Base):
    __tablename__ = 'consultas_medicas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False)
    fecha_consulta = Column(DateTime, default=func.now(), nullable=False)
    medico = Column(String(100))
    motivo_consulta = Column(Text)
    anamnesis = Column(Text)
    antecedentes_personales = Column(Text)
    antecedentes_familiares = Column(Text)
    medicamentos_actuales = Column(Text)
    alergias = Column(Text)
    diagnostico = Column(Text)
    plan_tratamiento = Column(Text)
    observaciones_generales = Column(Text)
    proxima_cita = Column(Date)
    estado = Column(String(20), default='activa')  # activa, completada, cancelada
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relaciones
    paciente = relationship("Paciente", foreign_keys=[paciente_id])

    def __repr__(self):
        return f"<ConsultaMedica(id={self.id}, paciente_id={self.paciente_id}, fecha={self.fecha_consulta}, estado={self.estado})>"

    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'fecha_consulta': self.fecha_consulta.isoformat() if self.fecha_consulta else None,
            'medico': self.medico,
            'motivo_consulta': self.motivo_consulta,
            'anamnesis': self.anamnesis,
            'antecedentes_personales': self.antecedentes_personales,
            'antecedentes_familiares': self.antecedentes_familiares,
            'medicamentos_actuales': self.medicamentos_actuales,
            'alergias': self.alergias,
            'diagnostico': self.diagnostico,
            'plan_tratamiento': self.plan_tratamiento,
            'observaciones_generales': self.observaciones_generales,
            'proxima_cita': self.proxima_cita.isoformat() if self.proxima_cita else None,
            'estado': self.estado,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }