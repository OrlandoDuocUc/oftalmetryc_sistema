from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.infraestructure.utils.tables import Base

class Diagnostico(Base):
    """
    Diagnóstico por ficha clínica (tabla 'diagnosticos').
    """
    __tablename__ = 'diagnosticos'

    diagnostico_id = Column(Integer, primary_key=True, autoincrement=True)
    ficha_id = Column(Integer, ForeignKey('fichas_clinicas.ficha_id', ondelete='CASCADE'), nullable=False)

    diagnostico_principal = Column(Text, nullable=False)
    diagnosticos_secundarios = Column(Text)
    cie_10_principal = Column(String(10))
    cie_10_secundarios = Column(Text)
    severidad = Column(String(20))
    observaciones = Column(Text)
    fecha_diagnostico = Column(DateTime, default=func.now(), nullable=False)

    ficha = relationship("FichaClinica", foreign_keys=[ficha_id])

    def __repr__(self):
        return f"<Diagnostico(id={self.diagnostico_id}, ficha_id={self.ficha_id})>"

    def to_dict(self):
        return {
            'diagnostico_id': self.diagnostico_id,
            'ficha_id': self.ficha_id,
            'diagnostico_principal': self.diagnostico_principal,
            'diagnosticos_secundarios': self.diagnosticos_secundarios,
            'cie_10_principal': self.cie_10_principal,
            'cie_10_secundarios': self.cie_10_secundarios,
            'severidad': self.severidad,
            'observaciones': self.observaciones,
            'fecha_diagnostico': self.fecha_diagnostico.isoformat() if self.fecha_diagnostico else None
        }
