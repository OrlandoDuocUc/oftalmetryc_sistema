from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey, func, Numeric, Boolean
from sqlalchemy.orm import relationship
from app.infraestructure.utils.tables import Base
from datetime import datetime

class FichaClinica(Base):
    __tablename__ = 'fichas_clinicas'

    ficha_id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_medico_id = Column(Integer, ForeignKey('pacientes_medicos.paciente_medico_id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'), nullable=False)
    numero_consulta = Column(String(20), unique=True, nullable=False)
    fecha_consulta = Column(DateTime, nullable=False)
    motivo_consulta = Column(Text)
    historia_actual = Column(Text)
    
    # AGUDEZA VISUAL OJO DERECHO
    av_od_sc = Column(String(20))  # Sin corrección
    av_od_cc = Column(String(20))  # Con corrección
    av_od_ph = Column(String(20))  # Pin hole
    av_od_cerca = Column(String(20))
    
    # AGUDEZA VISUAL OJO IZQUIERDO
    av_oi_sc = Column(String(20))
    av_oi_cc = Column(String(20))
    av_oi_ph = Column(String(20))
    av_oi_cerca = Column(String(20))
    
    # REFRACCIÓN OJO DERECHO
    esfera_od = Column(String(10))
    cilindro_od = Column(String(10))
    eje_od = Column(String(10))
    adicion_od = Column(String(10))
    
    # REFRACCIÓN OJO IZQUIERDO
    esfera_oi = Column(String(10))
    cilindro_oi = Column(String(10))
    eje_oi = Column(String(10))
    adicion_oi = Column(String(10))
    
    # DATOS GENERALES REFRACCIÓN
    distancia_pupilar = Column(String(10))
    tipo_lente = Column(String(50))
    
    estado = Column(String(20), default='en_proceso')
    fecha_creacion = Column(DateTime, default=func.now())

    # Relaciones
    paciente_medico = relationship("PacienteMedico", foreign_keys=[paciente_medico_id])
    usuario = relationship("User", foreign_keys=[usuario_id])

    def __repr__(self):
        return f"<FichaClinica(ficha_id={self.ficha_id}, numero_consulta={self.numero_consulta}, estado={self.estado})>"

    def to_dict(self):
        return {
            'ficha_id': self.ficha_id,
            'paciente_medico_id': self.paciente_medico_id,
            'usuario_id': self.usuario_id,
            'numero_consulta': self.numero_consulta,
            'fecha_consulta': self.fecha_consulta.isoformat() if self.fecha_consulta else None,
            'motivo_consulta': self.motivo_consulta,
            'historia_actual': self.historia_actual,
            # Agudeza Visual OD
            'av_od_sc': self.av_od_sc,
            'av_od_cc': self.av_od_cc,
            'av_od_ph': self.av_od_ph,
            'av_od_cerca': self.av_od_cerca,
            # Agudeza Visual OI
            'av_oi_sc': self.av_oi_sc,
            'av_oi_cc': self.av_oi_cc,
            'av_oi_ph': self.av_oi_ph,
            'av_oi_cerca': self.av_oi_cerca,
            # Refracción OD
            'esfera_od': self.esfera_od,
            'cilindro_od': self.cilindro_od,
            'eje_od': self.eje_od,
            'adicion_od': self.adicion_od,
            # Refracción OI
            'esfera_oi': self.esfera_oi,
            'cilindro_oi': self.cilindro_oi,
            'eje_oi': self.eje_oi,
            'adicion_oi': self.adicion_oi,
            # Datos generales
            'distancia_pupilar': self.distancia_pupilar,
            'tipo_lente': self.tipo_lente,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

# Alias para compatibilidad con diferentes importaciones
ConsultaMedica = FichaClinica