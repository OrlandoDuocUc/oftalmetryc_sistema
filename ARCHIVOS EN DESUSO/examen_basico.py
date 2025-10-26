"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, Numeric, Boolean
from sqlalchemy.orm import relationship
from app.infraestructure.utils.tables import Base

class ExamenBasico(Base):
    __tablename__ = 'examenes_basicos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    consulta_id = Column(Integer, ForeignKey('consultas_medicas.id', ondelete='CASCADE'), nullable=False)
    
    # Agudeza Visual Sin Corrección
    od_sc_lejos = Column(String(10))  # Ojo derecho sin corrección lejos
    oi_sc_lejos = Column(String(10))  # Ojo izquierdo sin corrección lejos
    ao_sc_lejos = Column(String(10))  # Ambos ojos sin corrección lejos
    od_sc_cerca = Column(String(10))
    oi_sc_cerca = Column(String(10))
    ao_sc_cerca = Column(String(10))
    
    # Agudeza Visual Con Corrección
    od_cc_lejos = Column(String(10))
    oi_cc_lejos = Column(String(10))
    ao_cc_lejos = Column(String(10))
    od_cc_cerca = Column(String(10))
    oi_cc_cerca = Column(String(10))
    ao_cc_cerca = Column(String(10))
    
    # Refracción Objetiva (Autorrefractómetro)
    od_esfera_obj = Column(Numeric(4,2))
    od_cilindro_obj = Column(Numeric(4,2))
    od_eje_obj = Column(Integer)
    oi_esfera_obj = Column(Numeric(4,2))
    oi_cilindro_obj = Column(Numeric(4,2))
    oi_eje_obj = Column(Integer)
    
    # Refracción Subjetiva
    od_esfera_subj = Column(Numeric(4,2))
    od_cilindro_subj = Column(Numeric(4,2))
    od_eje_subj = Column(Integer)
    od_add = Column(Numeric(4,2))  # Adición para presbicia
    oi_esfera_subj = Column(Numeric(4,2))
    oi_cilindro_subj = Column(Numeric(4,2))
    oi_eje_subj = Column(Integer)
    oi_add = Column(Numeric(4,2))
    
    # Presión Intraocular
    pio_od = Column(Integer)  # mmHg
    pio_oi = Column(Integer)
    metodo_pio = Column(String(50))  # Goldmann, aire, etc.
    
    # Evaluación Pupilar
    od_pupila_tamano = Column(Numeric(3,1))  # mm
    oi_pupila_tamano = Column(Numeric(3,1))
    od_reaccion_luz = Column(String(20))  # normal, perezosa, ausente
    oi_reaccion_luz = Column(String(20))
    defecto_pupilar_aferente = Column(Boolean, default=False)
    
    # Motilidad Ocular
    motilidad_normal = Column(Boolean, default=True)
    limitacion_movimientos = Column(Text)
    nistagmo = Column(Boolean, default=False)
    tipo_nistagmo = Column(String(50))
    
    # Visión de Colores
    ishihara_resultado = Column(String(10))  # 21/21, defecto, etc.
    tipo_discromatopsia = Column(String(30))
    
    # NUEVOS CAMPOS FICHA CLÍNICA DIGITAL
    
    # Agudeza Visual Expandida
    av_distancia_od = Column(String(10))
    av_distancia_oi = Column(String(10))
    av_c_c_od = Column(String(10))  # Sin corrección
    av_c_c_oi = Column(String(10))
    av_s_c_od = Column(String(10))  # Con corrección
    av_s_c_oi = Column(String(10))
    av_ph_od = Column(String(10))   # Pin Hole
    av_ph_oi = Column(String(10))
    av_proxima_od = Column(String(10))
    av_proxima_oi = Column(String(10))
    av_ao_distancia = Column(String(10))
    av_ao_proxima = Column(String(10))
    dominante_od = Column(String(10))
    dominante_oi = Column(String(10))
    av_otros = Column(Text)
    
    # Lensometría
    lensometria_od = Column(String(50))
    lensometria_oi = Column(String(50))
    
    # Queratometría
    queratometria_od = Column(String(50))
    queratometria_oi = Column(String(50))
    
    # Autorefractor Expandido
    ar_esf_od = Column(String(10))
    ar_cyl_od = Column(String(10))
    ar_eje_od = Column(String(10))
    ar_av_od = Column(String(10))
    ar_esf_oi = Column(String(10))
    ar_cyl_oi = Column(String(10))
    ar_eje_oi = Column(String(10))
    ar_av_oi = Column(String(10))
    
    # Subjetivo Expandido
    sub_esf_od = Column(String(10))
    sub_cyl_od = Column(String(10))
    sub_eje_od = Column(String(10))
    sub_av_od = Column(String(10))
    sub_esf_oi = Column(String(10))
    sub_cyl_oi = Column(String(10))
    sub_eje_oi = Column(String(10))
    sub_av_oi = Column(String(10))
    
    # RX Final Completo
    rx_esf_od = Column(String(10))
    rx_cyl_od = Column(String(10))
    rx_eje_od = Column(String(10))
    rx_avl_od = Column(String(10))
    rx_avc_od = Column(String(10))
    rx_dp_od = Column(String(10))
    rx_np_od = Column(String(10))
    rx_add_od = Column(String(10))
    rx_alt_od = Column(String(10))
    rx_ao_od = Column(String(10))
    rx_esf_oi = Column(String(10))
    rx_cyl_oi = Column(String(10))
    rx_eje_oi = Column(String(10))
    rx_avl_oi = Column(String(10))
    rx_avc_oi = Column(String(10))
    rx_dp_oi = Column(String(10))
    rx_np_oi = Column(String(10))
    rx_add_oi = Column(String(10))
    rx_alt_oi = Column(String(10))
    rx_ao_oi = Column(String(10))
    
    # Lentes de Contacto
    lc_poder_od = Column(String(10))
    lc_curva_base_od = Column(String(10))
    lc_diametro_od = Column(String(10))
    lc_material_od = Column(String(50))
    lc_poder_oi = Column(String(10))
    lc_curva_base_oi = Column(String(10))
    lc_diametro_oi = Column(String(10))
    lc_material_oi = Column(String(50))
    
    # Test Adicionales Expandidos
    hirschberg_od = Column(Integer)
    hirschberg_oi = Column(Integer)
    test_ishihara = Column(String(50))
    presion_intraocular_od = Column(String(20))
    presion_intraocular_oi = Column(String(20))
    cover_test_pfc = Column(String(50))
    cover_test_foria = Column(String(50))
    mov_oculares = Column(String(100))
    test_adicionales_otros = Column(Text)

    observaciones = Column(Text)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Relaciones
    consulta = relationship("ConsultaMedica", foreign_keys=[consulta_id])

    def __repr__(self):
        return f"<ExamenBasico(id={self.id}, consulta_id={self.consulta_id})>"

    def to_dict(self):
        return {
            'id': self.id,
            'consulta_id': self.consulta_id,
            'od_sc_lejos': self.od_sc_lejos,
            'oi_sc_lejos': self.oi_sc_lejos,
            'ao_sc_lejos': self.ao_sc_lejos,
            'od_sc_cerca': self.od_sc_cerca,
            'oi_sc_cerca': self.oi_sc_cerca,
            'ao_sc_cerca': self.ao_sc_cerca,
            'od_cc_lejos': self.od_cc_lejos,
            'oi_cc_lejos': self.oi_cc_lejos,
            'ao_cc_lejos': self.ao_cc_lejos,
            'od_cc_cerca': self.od_cc_cerca,
            'oi_cc_cerca': self.oi_cc_cerca,
            'ao_cc_cerca': self.ao_cc_cerca,
            'od_esfera_obj': float(self.od_esfera_obj) if self.od_esfera_obj else None,
            'od_cilindro_obj': float(self.od_cilindro_obj) if self.od_cilindro_obj else None,
            'od_eje_obj': self.od_eje_obj,
            'oi_esfera_obj': float(self.oi_esfera_obj) if self.oi_esfera_obj else None,
            'oi_cilindro_obj': float(self.oi_cilindro_obj) if self.oi_cilindro_obj else None,
            'oi_eje_obj': self.oi_eje_obj,
            'od_esfera_subj': float(self.od_esfera_subj) if self.od_esfera_subj else None,
            'od_cilindro_subj': float(self.od_cilindro_subj) if self.od_cilindro_subj else None,
            'od_eje_subj': self.od_eje_subj,
            'od_add': float(self.od_add) if self.od_add else None,
            'oi_esfera_subj': float(self.oi_esfera_subj) if self.oi_esfera_subj else None,
            'oi_cilindro_subj': float(self.oi_cilindro_subj) if self.oi_cilindro_subj else None,
            'oi_eje_subj': self.oi_eje_subj,
            'oi_add': float(self.oi_add) if self.oi_add else None,
            'pio_od': self.pio_od,
            'pio_oi': self.pio_oi,
            'metodo_pio': self.metodo_pio,
            'od_pupila_tamano': float(self.od_pupila_tamano) if self.od_pupila_tamano else None,
            'oi_pupila_tamano': float(self.oi_pupila_tamano) if self.oi_pupila_tamano else None,
            'od_reaccion_luz': self.od_reaccion_luz,
            'oi_reaccion_luz': self.oi_reaccion_luz,
            'defecto_pupilar_aferente': self.defecto_pupilar_aferente,
            'motilidad_normal': self.motilidad_normal,
            'limitacion_movimientos': self.limitacion_movimientos,
            'nistagmo': self.nistagmo,
            'tipo_nistagmo': self.tipo_nistagmo,
            'ishihara_resultado': self.ishihara_resultado,
            'tipo_discromatopsia': self.tipo_discromatopsia,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
"""        