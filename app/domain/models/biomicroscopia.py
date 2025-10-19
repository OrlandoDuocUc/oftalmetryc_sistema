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
    pupila_desc_od = Column(Text)
    pestanas_od = Column(Text)
    conjuntiva_bulbar_od = Column(Text)
    conjuntiva_tarsal_od = Column(Text)
    orbita_od = Column(Text)
    pliegue_semilunar_od = Column(Text)
    caruncula_od = Column(Text)
    conductos_lagrimales_od = Column(Text)
    parpado_superior_od = Column(Text)
    parpado_inferior_od = Column(Text)

    # OJO IZQUIERDO
    parpados_oi = Column(Text)
    conjuntiva_oi = Column(Text)
    cornea_oi = Column(Text)
    camara_anterior_oi = Column(Text)
    iris_oi = Column(Text)
    pupila_oi_mm = Column(String(10))
    pupila_oi_reaccion = Column(String(20))
    cristalino_oi = Column(Text)
    pupila_desc_oi = Column(Text)
    pestanas_oi = Column(Text)
    conjuntiva_bulbar_oi = Column(Text)
    conjuntiva_tarsal_oi = Column(Text)
    orbita_oi = Column(Text)
    pliegue_semilunar_oi = Column(Text)
    caruncula_oi = Column(Text)
    conductos_lagrimales_oi = Column(Text)
    parpado_superior_oi = Column(Text)
    parpado_inferior_oi = Column(Text)

    observaciones_generales = Column(Text)
    otros_detalles = Column(Text)
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
            'pupila_desc_od': self.pupila_desc_od,
            'pestanas_od': self.pestanas_od,
            'conjuntiva_bulbar_od': self.conjuntiva_bulbar_od,
            'conjuntiva_tarsal_od': self.conjuntiva_tarsal_od,
            'orbita_od': self.orbita_od,
            'pliegue_semilunar_od': self.pliegue_semilunar_od,
            'caruncula_od': self.caruncula_od,
            'conductos_lagrimales_od': self.conductos_lagrimales_od,
            'parpado_superior_od': self.parpado_superior_od,
            'parpado_inferior_od': self.parpado_inferior_od,
            'parpados_oi': self.parpados_oi,
            'conjuntiva_oi': self.conjuntiva_oi,
            'cornea_oi': self.cornea_oi,
            'camara_anterior_oi': self.camara_anterior_oi,
            'iris_oi': self.iris_oi,
            'pupila_oi_mm': self.pupila_oi_mm,
            'pupila_oi_reaccion': self.pupila_oi_reaccion,
            'cristalino_oi': self.cristalino_oi,
            'pupila_desc_oi': self.pupila_desc_oi,
            'pestanas_oi': self.pestanas_oi,
            'conjuntiva_bulbar_oi': self.conjuntiva_bulbar_oi,
            'conjuntiva_tarsal_oi': self.conjuntiva_tarsal_oi,
            'orbita_oi': self.orbita_oi,
            'pliegue_semilunar_oi': self.pliegue_semilunar_oi,
            'caruncula_oi': self.caruncula_oi,
            'conductos_lagrimales_oi': self.conductos_lagrimales_oi,
            'parpado_superior_oi': self.parpado_superior_oi,
            'parpado_inferior_oi': self.parpado_inferior_oi,
            'observaciones_generales': self.observaciones_generales,
            'otros_detalles': self.otros_detalles,
            'fecha_examen': self.fecha_examen.isoformat() if self.fecha_examen else None
        }
