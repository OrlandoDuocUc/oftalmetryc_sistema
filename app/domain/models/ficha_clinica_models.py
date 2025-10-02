# ===============================================================================
# MODELOS SQLALCHEMY - MÓDULO FICHA CLÍNICA DIGITAL
# Sistema: Oftalmetryc - Ficha Clínica Completa
# Autor: Orlando Rodriguez
# Fecha: 2 de octubre de 2025
# ===============================================================================

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

# ===============================================================================
# MODELO: PACIENTE V2 (EVOLUCIONADO)
# ===============================================================================

class PacienteV2(Base):
    """
    Modelo evolucionado de Paciente con campos adicionales para Ecuador
    """
    __tablename__ = 'pacientes_v2'
    
    # Campos principales
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ci = Column(String(20), unique=True, nullable=False, index=True)  # Cédula Ecuador
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    telefono = Column(String(20))
    email = Column(String(100))
    direccion = Column(Text)
    fecha_nacimiento = Column(Date)
    edad = Column(Integer)  # Calculable automáticamente
    genero = Column(String(10))  # M/F/Otro
    ocupacion = Column(String(100))
    hobby = Column(String(200))
    observaciones_generales = Column(Text)
    estado = Column(String(20), default='Activo')
    
    # Timestamps
    fecha_creacion = Column(DateTime, default=func.current_timestamp())
    fecha_actualizacion = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relaciones
    fichas_clinicas = relationship("FichaClinica", back_populates="paciente", cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.fecha_nacimiento and not self.edad:
            self.calcular_edad()
    
    def calcular_edad(self):
        """Calcula la edad basada en la fecha de nacimiento"""
        if self.fecha_nacimiento:
            today = datetime.today().date()
            self.edad = today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del paciente"""
        return f"{self.nombres} {self.apellidos}"
    
    def __repr__(self):
        return f"<PacienteV2(id={self.id}, ci='{self.ci}', nombre='{self.nombre_completo}')>"

# ===============================================================================
# MODELO: FICHA CLÍNICA
# ===============================================================================

class FichaClinica(Base):
    """
    Modelo para registrar cada consulta/visita del paciente
    """
    __tablename__ = 'fichas_clinicas'
    
    # Campos principales
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    paciente_id = Column(BigInteger, ForeignKey('pacientes_v2.id', ondelete='CASCADE'), nullable=False)
    fecha_consulta = Column(DateTime, default=func.current_timestamp())
    motivo_consulta = Column(Text)
    ultimo_control_visual = Column(Date)
    usa_lentes = Column(Boolean, default=False)
    ultimo_cambio_lentes = Column(Date)
    antecedentes_personales = Column(Text)
    antecedentes_familiares = Column(Text)
    diagnostico_general = Column(Text)
    tratamiento_general = Column(Text)
    firma_responsable = Column(String(100))
    conforme_evaluado = Column(Boolean, default=True)
    
    # Timestamps
    fecha_actualizacion = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relaciones
    paciente = relationship("PacienteV2", back_populates="fichas_clinicas")
    examen_oftalmologico = relationship("ExamenOftalmologicoCompleto", back_populates="ficha_clinica", 
                                      uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<FichaClinica(id={self.id}, paciente_id={self.paciente_id}, fecha='{self.fecha_consulta}')>"

# ===============================================================================
# MODELO: EXAMEN OFTALMOLÓGICO COMPLETO
# ===============================================================================

class ExamenOftalmologicoCompleto(Base):
    """
    Modelo completo para todos los exámenes oftalmológicos detallados
    """
    __tablename__ = 'examenes_oftalmologicos_completos'
    
    # Campo principal
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ficha_clinica_id = Column(BigInteger, ForeignKey('fichas_clinicas.id', ondelete='CASCADE'), 
                             unique=True, nullable=False)
    
    # ===== SECCIÓN 1: AGUDEZA VISUAL =====
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
    
    # ===== SECCIÓN 2: LENSOMETRÍA =====
    lensometria_od = Column(String(50))
    lensometria_oi = Column(String(50))
    
    # ===== SECCIÓN 3: QUERATOMETRÍA =====
    queratometria_od = Column(String(50))
    queratometria_oi = Column(String(50))
    
    # ===== SECCIÓN 4: AUTOREFRACTOR =====
    ar_esf_od = Column(String(10))
    ar_cyl_od = Column(String(10))
    ar_eje_od = Column(String(10))
    ar_av_od = Column(String(10))
    ar_esf_oi = Column(String(10))
    ar_cyl_oi = Column(String(10))
    ar_eje_oi = Column(String(10))
    ar_av_oi = Column(String(10))
    
    # ===== SECCIÓN 5: SUBJETIVO =====
    sub_esf_od = Column(String(10))
    sub_cyl_od = Column(String(10))
    sub_eje_od = Column(String(10))
    sub_av_od = Column(String(10))
    sub_esf_oi = Column(String(10))
    sub_cyl_oi = Column(String(10))
    sub_eje_oi = Column(String(10))
    sub_av_oi = Column(String(10))
    
    # ===== SECCIÓN 6: RX FINAL =====
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
    
    # ===== SECCIÓN 7: LENTES DE CONTACTO =====
    lc_poder_od = Column(String(10))
    lc_curva_base_od = Column(String(10))
    lc_diametro_od = Column(String(10))
    lc_adicion_od = Column(String(10))
    lc_diseno_od = Column(String(50))
    lc_material_od = Column(String(50))
    lc_poder_oi = Column(String(10))
    lc_curva_base_oi = Column(String(10))
    lc_diametro_oi = Column(String(10))
    lc_adicion_oi = Column(String(10))
    lc_diseno_oi = Column(String(50))
    lc_material_oi = Column(String(50))
    
    # ===== SECCIÓN 8: TEST ADICIONALES =====
    hirschberg_od = Column(Integer)  # 0, 15, 30, 45
    hirschberg_oi = Column(Integer)
    campimetria_t100_od = Column(String(20))
    campimetria_n60_od = Column(String(20))
    campimetria_s60_od = Column(String(20))
    campimetria_i70_od = Column(String(20))
    campimetria_t100_oi = Column(String(20))
    campimetria_n60_oi = Column(String(20))
    campimetria_s60_oi = Column(String(20))
    campimetria_i70_oi = Column(String(20))
    cover_test_pfc = Column(String(50))
    cover_test_foria = Column(String(50))
    cover_test_tropia = Column(String(50))
    cover_test_mag_desviacion = Column(String(50))
    mov_oculares = Column(String(100))
    luces_worth_lejos = Column(String(50))
    luces_worth_cerca = Column(String(50))
    test_ishihara = Column(String(50))
    presion_intraocular_od = Column(String(20))
    presion_intraocular_oi = Column(String(20))
    test_adicionales_otros = Column(Text)
    
    # ===== SECCIÓN 9: BIOMICROSCOPÍA =====
    biomic_cornea_od = Column(Text)
    biomic_cornea_oi = Column(Text)
    biomic_cristalino_od = Column(Text)
    biomic_cristalino_oi = Column(Text)
    biomic_pupila_od = Column(Text)
    biomic_pupila_oi = Column(Text)
    biomic_pestanas_od = Column(Text)
    biomic_pestanas_oi = Column(Text)
    biomic_conjuntiva_bulbar_od = Column(Text)
    biomic_conjuntiva_bulbar_oi = Column(Text)
    biomic_conjuntiva_tarsal_od = Column(Text)
    biomic_conjuntiva_tarsal_oi = Column(Text)
    biomic_esclera_od = Column(Text)
    biomic_esclera_oi = Column(Text)
    biomic_pliegue_semilunar_od = Column(Text)
    biomic_pliegue_semilunar_oi = Column(Text)
    biomic_caruncula_od = Column(Text)
    biomic_caruncula_oi = Column(Text)
    biomic_conductos_lagrimales_od = Column(Text)
    biomic_conductos_lagrimales_oi = Column(Text)
    biomic_parpado_superior_od = Column(Text)
    biomic_parpado_superior_oi = Column(Text)
    biomic_camara_anterior_od = Column(Text)
    biomic_camara_anterior_oi = Column(Text)
    biomic_parpado_inferior_od = Column(Text)
    biomic_parpado_inferior_oi = Column(Text)
    biomic_otros = Column(Text)
    
    # ===== SECCIÓN 10: REFLEJOS PUPILARES =====
    reflejo_acomodativo_miosis_od = Column(String(50))
    reflejo_acomodativo_convergencia_od = Column(String(50))
    reflejo_acomodativo_midriasis_od = Column(String(50))
    reflejo_acomodativo_miosis_oi = Column(String(50))
    reflejo_acomodativo_convergencia_oi = Column(String(50))
    reflejo_acomodativo_midriasis_oi = Column(String(50))
    reflejo_fotomotor_miosis_od = Column(String(50))
    reflejo_fotomotor_midriasis_od = Column(String(50))
    reflejo_consensual_od = Column(String(50))
    reflejo_fotomotor_miosis_oi = Column(String(50))
    reflejo_fotomotor_midriasis_oi = Column(String(50))
    reflejo_consensual_oi = Column(String(50))
    
    # ===== SECCIÓN 11: FONDO DE OJO =====
    fondo_ojo_av_temp_sup_od = Column(Text)
    fondo_ojo_av_temp_inf_od = Column(Text)
    fondo_ojo_av_nasal_sup_od = Column(Text)
    fondo_ojo_av_nasal_inf_od = Column(Text)
    fondo_ojo_retina_od = Column(Text)
    fondo_ojo_macula_od = Column(Text)
    fondo_ojo_excavacion_od = Column(Text)
    fondo_ojo_vasos_od = Column(Text)
    fondo_ojo_papila_od = Column(Text)
    fondo_ojo_fijacion_od = Column(Text)
    fondo_ojo_color_od = Column(Text)
    fondo_ojo_borde_od = Column(Text)
    fondo_ojo_av_temp_sup_oi = Column(Text)
    fondo_ojo_av_temp_inf_oi = Column(Text)
    fondo_ojo_av_nasal_sup_oi = Column(Text)
    fondo_ojo_av_nasal_inf_oi = Column(Text)
    fondo_ojo_retina_oi = Column(Text)
    fondo_ojo_macula_oi = Column(Text)
    fondo_ojo_excavacion_oi = Column(Text)
    fondo_ojo_vasos_oi = Column(Text)
    fondo_ojo_papila_oi = Column(Text)
    fondo_ojo_fijacion_oi = Column(Text)
    fondo_ojo_color_oi = Column(Text)
    fondo_ojo_borde_oi = Column(Text)
    fondo_ojo_otros = Column(Text)
    
    # ===== SECCIÓN 12: OTROS DATOS MÉDICOS =====
    presion_arterial_sistolica = Column(Integer)
    presion_arterial_diastolica = Column(Integer)
    saturacion_o2 = Column(Integer)
    glucosa = Column(String(20))
    trigliceridos = Column(String(20))
    atp = Column(String(20))
    colesterol = Column(String(20))
    
    # Timestamp
    fecha_creacion = Column(DateTime, default=func.current_timestamp())
    
    # Relación
    ficha_clinica = relationship("FichaClinica", back_populates="examen_oftalmologico")
    
    def __repr__(self):
        return f"<ExamenOftalmologicoCompleto(id={self.id}, ficha_clinica_id={self.ficha_clinica_id})>"

# ===============================================================================
# FUNCIONES AUXILIARES
# ===============================================================================

def crear_todas_las_tablas(engine):
    """
    Crea todas las tablas en la base de datos
    """
    Base.metadata.create_all(engine)

def obtener_estructura_tablas():
    """
    Retorna información sobre la estructura de las tablas
    """
    return {
        'pacientes_v2': {
            'campos': len(PacienteV2.__table__.columns),
            'relaciones': ['fichas_clinicas']
        },
        'fichas_clinicas': {
            'campos': len(FichaClinica.__table__.columns),
            'relaciones': ['paciente', 'examen_oftalmologico']
        },
        'examenes_oftalmologicos_completos': {
            'campos': len(ExamenOftalmologicoCompleto.__table__.columns),
            'relaciones': ['ficha_clinica']
        }
    }