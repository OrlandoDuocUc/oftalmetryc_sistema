from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import relationship
from app.infraestructure.utils.tables import Base

class Biomicroscopia(Base):
    __tablename__ = 'biomicroscopia'

    id = Column(Integer, primary_key=True, autoincrement=True)
    consulta_id = Column(Integer, ForeignKey('consultas_medicas.id', ondelete='CASCADE'), nullable=False)
    
    # Párpados OD
    od_parpados_posicion = Column(String(20))  # normal, ptosis, retracción
    od_parpados_edema = Column(Boolean, default=False)
    od_parpados_lesiones = Column(Text)
    od_pestanas = Column(String(20))  # normales, triaquiasis, madarosis
    
    # Párpados OI
    oi_parpados_posicion = Column(String(20))
    oi_parpados_edema = Column(Boolean, default=False)
    oi_parpados_lesiones = Column(Text)
    oi_pestanas = Column(String(20))
    
    # Conjuntiva OD
    od_conjuntiva_bulbar = Column(String(30))  # normal, hiperemia, hemorragia
    od_conjuntiva_tarsal = Column(String(30))
    od_conjuntiva_secrecion = Column(String(30))  # ausente, mucosa, purulenta
    od_conjuntiva_foliculos = Column(Boolean, default=False)
    od_conjuntiva_papilas = Column(Boolean, default=False)
    
    # Conjuntiva OI
    oi_conjuntiva_bulbar = Column(String(30))
    oi_conjuntiva_tarsal = Column(String(30))
    oi_conjuntiva_secrecion = Column(String(30))
    oi_conjuntiva_foliculos = Column(Boolean, default=False)
    oi_conjuntiva_papilas = Column(Boolean, default=False)
    
    # Córnea OD
    od_cornea_transparencia = Column(String(20))  # transparente, opaca, leucoma
    od_cornea_superficie = Column(String(20))  # lisa, irregular, erosión
    od_cornea_epitelo = Column(String(20))  # intacto, defecto epitelial
    od_cornea_estroma = Column(String(30))  # transparente, cicatrices, infiltrados
    od_cornea_endotelio = Column(String(20))  # normal, precipitados, edema
    od_cornea_fluorenceina = Column(String(30))  # negativa, positiva (describir)
    
    # Córnea OI
    oi_cornea_transparencia = Column(String(20))
    oi_cornea_superficie = Column(String(20))
    oi_cornea_epitelo = Column(String(20))
    oi_cornea_estroma = Column(String(30))
    oi_cornea_endotelio = Column(String(20))
    oi_cornea_fluorenceina = Column(String(30))
    
    # Cámara Anterior OD
    od_camara_profundidad = Column(String(20))  # normal, superficial, profunda
    od_camara_contenido = Column(String(30))  # transparente, células, fibrina, sangre
    od_camara_tyndall = Column(String(10))  # grado 0-4
    
    # Cámara Anterior OI
    oi_camara_profundidad = Column(String(20))
    oi_camara_contenido = Column(String(30))
    oi_camara_tyndall = Column(String(10))
    
    # Iris OD
    od_iris_color = Column(String(20))
    od_iris_patron = Column(String(20))  # normal, atrofia, sinequias
    od_iris_lesiones = Column(Text)
    
    # Iris OI
    oi_iris_color = Column(String(20))
    oi_iris_patron = Column(String(20))
    oi_iris_lesiones = Column(Text)
    
    # Cristalino OD
    od_cristalino_transparencia = Column(String(30))  # transparente, catarata nuclear/cortical/subcapsular
    od_cristalino_posicion = Column(String(20))  # normal, subluxación, luxación
    od_cristalino_pseudofaquia = Column(Boolean, default=False)
    od_cristalino_lente_tipo = Column(String(30))  # si es pseudofáquico
    
    # Cristalino OI
    oi_cristalino_transparencia = Column(String(30))
    oi_cristalino_posicion = Column(String(20))
    oi_cristalino_pseudofaquia = Column(Boolean, default=False)
    oi_cristalino_lente_tipo = Column(String(30))
    
    observaciones = Column(Text)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Relaciones
    consulta = relationship("ConsultaMedica", foreign_keys=[consulta_id])

    def __repr__(self):
        return f"<Biomicroscopia(id={self.id}, consulta_id={self.consulta_id})>"

    def to_dict(self):
        return {
            'id': self.id,
            'consulta_id': self.consulta_id,
            # Párpados OD
            'od_parpados_posicion': self.od_parpados_posicion,
            'od_parpados_edema': self.od_parpados_edema,
            'od_parpados_lesiones': self.od_parpados_lesiones,
            'od_pestanas': self.od_pestanas,
            # Párpados OI
            'oi_parpados_posicion': self.oi_parpados_posicion,
            'oi_parpados_edema': self.oi_parpados_edema,
            'oi_parpados_lesiones': self.oi_parpados_lesiones,
            'oi_pestanas': self.oi_pestanas,
            # Conjuntiva OD
            'od_conjuntiva_bulbar': self.od_conjuntiva_bulbar,
            'od_conjuntiva_tarsal': self.od_conjuntiva_tarsal,
            'od_conjuntiva_secrecion': self.od_conjuntiva_secrecion,
            'od_conjuntiva_foliculos': self.od_conjuntiva_foliculos,
            'od_conjuntiva_papilas': self.od_conjuntiva_papilas,
            # Conjuntiva OI
            'oi_conjuntiva_bulbar': self.oi_conjuntiva_bulbar,
            'oi_conjuntiva_tarsal': self.oi_conjuntiva_tarsal,
            'oi_conjuntiva_secrecion': self.oi_conjuntiva_secrecion,
            'oi_conjuntiva_foliculos': self.oi_conjuntiva_foliculos,
            'oi_conjuntiva_papilas': self.oi_conjuntiva_papilas,
            # Córnea OD
            'od_cornea_transparencia': self.od_cornea_transparencia,
            'od_cornea_superficie': self.od_cornea_superficie,
            'od_cornea_epitelo': self.od_cornea_epitelo,
            'od_cornea_estroma': self.od_cornea_estroma,
            'od_cornea_endotelio': self.od_cornea_endotelio,
            'od_cornea_fluorenceina': self.od_cornea_fluorenceina,
            # Córnea OI
            'oi_cornea_transparencia': self.oi_cornea_transparencia,
            'oi_cornea_superficie': self.oi_cornea_superficie,
            'oi_cornea_epitelo': self.oi_cornea_epitelo,
            'oi_cornea_estroma': self.oi_cornea_estroma,
            'oi_cornea_endotelio': self.oi_cornea_endotelio,
            'oi_cornea_fluorenceina': self.oi_cornea_fluorenceina,
            # Cámara Anterior
            'od_camara_profundidad': self.od_camara_profundidad,
            'od_camara_contenido': self.od_camara_contenido,
            'od_camara_tyndall': self.od_camara_tyndall,
            'oi_camara_profundidad': self.oi_camara_profundidad,
            'oi_camara_contenido': self.oi_camara_contenido,
            'oi_camara_tyndall': self.oi_camara_tyndall,
            # Iris
            'od_iris_color': self.od_iris_color,
            'od_iris_patron': self.od_iris_patron,
            'od_iris_lesiones': self.od_iris_lesiones,
            'oi_iris_color': self.oi_iris_color,
            'oi_iris_patron': self.oi_iris_patron,
            'oi_iris_lesiones': self.oi_iris_lesiones,
            # Cristalino
            'od_cristalino_transparencia': self.od_cristalino_transparencia,
            'od_cristalino_posicion': self.od_cristalino_posicion,
            'od_cristalino_pseudofaquia': self.od_cristalino_pseudofaquia,
            'od_cristalino_lente_tipo': self.od_cristalino_lente_tipo,
            'oi_cristalino_transparencia': self.oi_cristalino_transparencia,
            'oi_cristalino_posicion': self.oi_cristalino_posicion,
            'oi_cristalino_pseudofaquia': self.oi_cristalino_pseudofaquia,
            'oi_cristalino_lente_tipo': self.oi_cristalino_lente_tipo,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }