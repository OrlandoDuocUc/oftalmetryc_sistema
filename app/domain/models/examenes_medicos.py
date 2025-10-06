from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, func, Time
from sqlalchemy.orm import relationship
from app.infraestructure.utils.tables import Base

class FondoOjo(Base):
    __tablename__ = 'fondo_ojo'

    fondo_ojo_id = Column(Integer, primary_key=True, autoincrement=True)
    ficha_id = Column(Integer, ForeignKey('fichas_clinicas.ficha_id'), nullable=False)
    
    # OJO DERECHO
    disco_optico_od = Column(Text)
    macula_od = Column(Text)
    vasos_od = Column(Text)
    retina_periferica_od = Column(Text)
    
    # OJO IZQUIERDO
    disco_optico_oi = Column(Text)
    macula_oi = Column(Text)
    vasos_oi = Column(Text)
    retina_periferica_oi = Column(Text)
    
    observaciones = Column(Text)
    fecha_examen = Column(DateTime, default=func.now())

    # Relaciones
    ficha = relationship("FichaClinica", foreign_keys=[ficha_id])

    def __repr__(self):
        return f"<FondoOjo(fondo_ojo_id={self.fondo_ojo_id}, ficha_id={self.ficha_id})>"

    def to_dict(self):
        return {
            'fondo_ojo_id': self.fondo_ojo_id,
            'ficha_id': self.ficha_id,
            'disco_optico_od': self.disco_optico_od,
            'macula_od': self.macula_od,
            'vasos_od': self.vasos_od,
            'retina_periferica_od': self.retina_periferica_od,
            'disco_optico_oi': self.disco_optico_oi,
            'macula_oi': self.macula_oi,
            'vasos_oi': self.vasos_oi,
            'retina_periferica_oi': self.retina_periferica_oi,
            'observaciones': self.observaciones,
            'fecha_examen': self.fecha_examen.isoformat() if self.fecha_examen else None
        }

class PresionIntraocular(Base):
    __tablename__ = 'presion_intraocular'

    pio_id = Column(Integer, primary_key=True, autoincrement=True)
    ficha_id = Column(Integer, ForeignKey('fichas_clinicas.ficha_id'), nullable=False)
    pio_od = Column(String(10))
    pio_oi = Column(String(10))
    metodo_medicion = Column(String(50))
    hora_medicion = Column(Time)
    observaciones = Column(Text)
    fecha_medicion = Column(DateTime, default=func.now())

    # Relaciones
    ficha = relationship("FichaClinica", foreign_keys=[ficha_id])

    def __repr__(self):
        return f"<PresionIntraocular(pio_id={self.pio_id}, ficha_id={self.ficha_id})>"

    def to_dict(self):
        return {
            'pio_id': self.pio_id,
            'ficha_id': self.ficha_id,
            'pio_od': self.pio_od,
            'pio_oi': self.pio_oi,
            'metodo_medicion': self.metodo_medicion,
            'hora_medicion': self.hora_medicion.isoformat() if self.hora_medicion else None,
            'observaciones': self.observaciones,
            'fecha_medicion': self.fecha_medicion.isoformat() if self.fecha_medicion else None
        }

class CampoVisual(Base):
    __tablename__ = 'campos_visuales'

    campo_visual_id = Column(Integer, primary_key=True, autoincrement=True)
    ficha_id = Column(Integer, ForeignKey('fichas_clinicas.ficha_id'), nullable=False)
    tipo_campo = Column(String(50))
    resultado_od = Column(Text)
    resultado_oi = Column(Text)
    interpretacion = Column(Text)
    fecha_examen = Column(DateTime, default=func.now())

    # Relaciones
    ficha = relationship("FichaClinica", foreign_keys=[ficha_id])

    def __repr__(self):
        return f"<CampoVisual(campo_visual_id={self.campo_visual_id}, ficha_id={self.ficha_id})>"

    def to_dict(self):
        return {
            'campo_visual_id': self.campo_visual_id,
            'ficha_id': self.ficha_id,
            'tipo_campo': self.tipo_campo,
            'resultado_od': self.resultado_od,
            'resultado_oi': self.resultado_oi,
            'interpretacion': self.interpretacion,
            'fecha_examen': self.fecha_examen.isoformat() if self.fecha_examen else None
        }

class DiagnosticoMedico(Base):
    __tablename__ = 'diagnosticos'

    diagnostico_id = Column(Integer, primary_key=True, autoincrement=True)
    ficha_id = Column(Integer, ForeignKey('fichas_clinicas.ficha_id'), nullable=False)
    diagnostico_principal = Column(Text, nullable=False)
    diagnosticos_secundarios = Column(Text)
    cie_10_principal = Column(String(10))
    cie_10_secundarios = Column(Text)
    severidad = Column(String(20))
    observaciones = Column(Text)
    fecha_diagnostico = Column(DateTime, default=func.now())

    # Relaciones
    ficha = relationship("FichaClinica", foreign_keys=[ficha_id])

    def __repr__(self):
        return f"<DiagnosticoMedico(diagnostico_id={self.diagnostico_id}, ficha_id={self.ficha_id})>"

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

class Tratamiento(Base):
    __tablename__ = 'tratamientos'

    tratamiento_id = Column(Integer, primary_key=True, autoincrement=True)
    ficha_id = Column(Integer, ForeignKey('fichas_clinicas.ficha_id'), nullable=False)
    medicamentos = Column(Text)
    tratamiento_no_farmacologico = Column(Text)
    recomendaciones = Column(Text)
    plan_seguimiento = Column(Text)
    proxima_cita = Column(Date)
    urgencia_seguimiento = Column(String(20))
    fecha_tratamiento = Column(DateTime, default=func.now())

    # Relaciones
    ficha = relationship("FichaClinica", foreign_keys=[ficha_id])

    def __repr__(self):
        return f"<Tratamiento(tratamiento_id={self.tratamiento_id}, ficha_id={self.ficha_id})>"

    def to_dict(self):
        return {
            'tratamiento_id': self.tratamiento_id,
            'ficha_id': self.ficha_id,
            'medicamentos': self.medicamentos,
            'tratamiento_no_farmacologico': self.tratamiento_no_farmacologico,
            'recomendaciones': self.recomendaciones,
            'plan_seguimiento': self.plan_seguimiento,
            'proxima_cita': self.proxima_cita.isoformat() if self.proxima_cita else None,
            'urgencia_seguimiento': self.urgencia_seguimiento,
            'fecha_tratamiento': self.fecha_tratamiento.isoformat() if self.fecha_tratamiento else None
        }