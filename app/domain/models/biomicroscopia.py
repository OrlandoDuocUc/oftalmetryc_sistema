from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.infraestructure.utils.tables import Base

class Biomicroscopia(Base):
    __tablename__ = 'biomicroscopia'

    biomicroscopia_id = Column(Integer, primary_key=True, autoincrement=True)
    ficha_id = Column(Integer, ForeignKey('fichas_clinicas.ficha_id', ondelete='CASCADE'), nullable=False)
    
    # OJO DERECHO
    parpados_od = Column(Text)
    conjuntiva_od = Column(Text)
    cornea_od = Column(Text)
    camara_anterior_od = Column(Text)
    iris_od = Column(Text)
    pupila_od_mm = Column(String(10))
    pupila_od_reaccion = Column(String(20))
    cristalino_od = Column(Text)
    
    # OJO IZQUIERDO
    parpados_oi = Column(Text)
    conjuntiva_oi = Column(Text)
    cornea_oi = Column(Text)
    camara_anterior_oi = Column(Text)
    iris_oi = Column(Text)
    pupila_oi_mm = Column(String(10))
    pupila_oi_reaccion = Column(String(20))
    cristalino_oi = Column(Text)
    
    observaciones_generales = Column(Text)
    fecha_examen = Column(DateTime, default=func.now(), nullable=False)

    # Relación
    ficha = relationship("FichaClinica", foreign_keys=[ficha_id])

    def __repr__(self):
        return f"<Biomicroscopia(id={self.biomicroscopia_id}, ficha_id={self.ficha_id})>"

    def to_dict(self):
        return {
            'biomicroscopia_id': self.biomicroscopia_id,
            'ficha_id': self.ficha_id,
            'parpados_od': self.parpados_od,
            'conjuntiva_od': self.conjuntiva_od,
            'cornea_od': self.cornea_od,
            'camara_anterior_od': self.camara_anterior_od,
            'iris_od': self.iris_od,
            'pupila_od_mm': self.pupila_od_mm,
            'pupila_od_reaccion': self.pupila_od_reaccion,
            'cristalino_od': self.cristalino_od,
            'parpados_oi': self.parpados_oi,
            'conjuntiva_oi': self.conjuntiva_oi,
            'cornea_oi': self.cornea_oi,
            'camara_anterior_oi': self.camara_anterior_oi,
            'iris_oi': self.iris_oi,
            'pupila_oi_mm': self.pupila_oi_mm,
            'pupila_oi_reaccion': self.pupila_oi_reaccion,
            'cristalino_oi': self.cristalino_oi,
            'observaciones_generales': self.observaciones_generales,
            'fecha_examen': self.fecha_examen.isoformat() if self.fecha_examen else None
        }
