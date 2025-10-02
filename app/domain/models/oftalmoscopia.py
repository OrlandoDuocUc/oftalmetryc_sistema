from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, Boolean, Numeric
from sqlalchemy.orm import relationship
from app.infraestructure.utils.tables import Base

class Oftalmoscopia(Base):
    __tablename__ = 'oftalmoscopia'

    id = Column(Integer, primary_key=True, autoincrement=True)
    consulta_id = Column(Integer, ForeignKey('consultas_medicas.id', ondelete='CASCADE'), nullable=False)
    
    # Vítreo OD
    od_vitreo = Column(String(30))  # transparente, hialosis, hemorragia, opacidades
    od_vitreo_desprendimiento = Column(Boolean, default=False)
    
    # Vítreo OI
    oi_vitreo = Column(String(30))
    oi_vitreo_desprendimiento = Column(Boolean, default=False)
    
    # Papila Óptica OD
    od_papila_color = Column(String(20))  # normal, pálida, hiperémico
    od_papila_contornos = Column(String(20))  # nítidos, borrosos
    od_papila_excavacion = Column(Numeric(3,2))  # relación copa/disco 0.0-1.0
    od_papila_hemorragias = Column(Boolean, default=False)
    od_papila_edema = Column(Boolean, default=False)
    
    # Papila Óptica OI
    oi_papila_color = Column(String(20))
    oi_papila_contornos = Column(String(20))
    oi_papila_excavacion = Column(Numeric(3,2))
    oi_papila_hemorragias = Column(Boolean, default=False)
    oi_papila_edema = Column(Boolean, default=False)
    
    # Mácula OD
    od_macula_reflejo = Column(String(20))  # presente, ausente, alterado
    od_macula_pigmentacion = Column(String(20))  # normal, hiper/hipopigmentación
    od_macula_exudados = Column(Boolean, default=False)
    od_macula_hemorragias = Column(Boolean, default=False)
    od_macula_edema = Column(Boolean, default=False)
    od_macula_drusen = Column(Boolean, default=False)
    
    # Mácula OI
    oi_macula_reflejo = Column(String(20))
    oi_macula_pigmentacion = Column(String(20))
    oi_macula_exudados = Column(Boolean, default=False)
    oi_macula_hemorragias = Column(Boolean, default=False)
    oi_macula_edema = Column(Boolean, default=False)
    oi_macula_drusen = Column(Boolean, default=False)
    
    # Vasos Retinianos OD
    od_arterias = Column(String(30))  # calibre normal, estrechamiento, esclerosis
    od_venas = Column(String(30))  # calibre normal, dilatación, tortuosidad
    od_cruces_av = Column(String(30))  # normales, compresión, escotaduras
    od_hemorragias_retina = Column(Boolean, default=False)
    od_exudados_duros = Column(Boolean, default=False)
    od_exudados_blandos = Column(Boolean, default=False)
    
    # Vasos Retinianos OI
    oi_arterias = Column(String(30))
    oi_venas = Column(String(30))
    oi_cruces_av = Column(String(30))
    oi_hemorragias_retina = Column(Boolean, default=False)
    oi_exudados_duros = Column(Boolean, default=False)
    oi_exudados_blandos = Column(Boolean, default=False)
    
    # Periferia Retiniana OD
    od_periferia = Column(String(30))  # normal, degeneración, roturas
    od_desprendimiento = Column(Boolean, default=False)
    
    # Periferia Retiniana OI
    oi_periferia = Column(String(30))
    oi_desprendimiento = Column(Boolean, default=False)
    
    observaciones = Column(Text)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Relaciones
    consulta = relationship("ConsultaMedica", foreign_keys=[consulta_id])

    def __repr__(self):
        return f"<Oftalmoscopia(id={self.id}, consulta_id={self.consulta_id})>"

    def to_dict(self):
        return {
            'id': self.id,
            'consulta_id': self.consulta_id,
            # Vítreo
            'od_vitreo': self.od_vitreo,
            'od_vitreo_desprendimiento': self.od_vitreo_desprendimiento,
            'oi_vitreo': self.oi_vitreo,
            'oi_vitreo_desprendimiento': self.oi_vitreo_desprendimiento,
            # Papila Óptica
            'od_papila_color': self.od_papila_color,
            'od_papila_contornos': self.od_papila_contornos,
            'od_papila_excavacion': float(self.od_papila_excavacion) if self.od_papila_excavacion else None,
            'od_papila_hemorragias': self.od_papila_hemorragias,
            'od_papila_edema': self.od_papila_edema,
            'oi_papila_color': self.oi_papila_color,
            'oi_papila_contornos': self.oi_papila_contornos,
            'oi_papila_excavacion': float(self.oi_papila_excavacion) if self.oi_papila_excavacion else None,
            'oi_papila_hemorragias': self.oi_papila_hemorragias,
            'oi_papila_edema': self.oi_papila_edema,
            # Mácula
            'od_macula_reflejo': self.od_macula_reflejo,
            'od_macula_pigmentacion': self.od_macula_pigmentacion,
            'od_macula_exudados': self.od_macula_exudados,
            'od_macula_hemorragias': self.od_macula_hemorragias,
            'od_macula_edema': self.od_macula_edema,
            'od_macula_drusen': self.od_macula_drusen,
            'oi_macula_reflejo': self.oi_macula_reflejo,
            'oi_macula_pigmentacion': self.oi_macula_pigmentacion,
            'oi_macula_exudados': self.oi_macula_exudados,
            'oi_macula_hemorragias': self.oi_macula_hemorragias,
            'oi_macula_edema': self.oi_macula_edema,
            'oi_macula_drusen': self.oi_macula_drusen,
            # Vasos Retinianos
            'od_arterias': self.od_arterias,
            'od_venas': self.od_venas,
            'od_cruces_av': self.od_cruces_av,
            'od_hemorragias_retina': self.od_hemorragias_retina,
            'od_exudados_duros': self.od_exudados_duros,
            'od_exudados_blandos': self.od_exudados_blandos,
            'oi_arterias': self.oi_arterias,
            'oi_venas': self.oi_venas,
            'oi_cruces_av': self.oi_cruces_av,
            'oi_hemorragias_retina': self.oi_hemorragias_retina,
            'oi_exudados_duros': self.oi_exudados_duros,
            'oi_exudados_blandos': self.oi_exudados_blandos,
            # Periferia Retiniana
            'od_periferia': self.od_periferia,
            'od_desprendimiento': self.od_desprendimiento,
            'oi_periferia': self.oi_periferia,
            'oi_desprendimiento': self.oi_desprendimiento,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }