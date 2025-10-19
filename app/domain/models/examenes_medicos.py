# app/domain/models/examenes_medicos.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Time, ForeignKey, func
from sqlalchemy.orm import relationship
from app.infraestructure.utils.tables import Base

class FondoOjo(Base):
    __tablename__ = 'fondo_ojo'

    fondo_ojo_id = Column(Integer, primary_key=True, autoincrement=True)
    ficha_id = Column(Integer, ForeignKey('fichas_clinicas.ficha_id', ondelete='CASCADE'), nullable=False)

    # OJO DERECHO
    disco_optico_od = Column(Text)
    macula_od = Column(Text)
    vasos_od = Column(Text)
    retina_periferica_od = Column(Text)
    av_temp_sup_od = Column(Text)
    av_temp_inf_od = Column(Text)
    av_nasal_sup_od = Column(Text)
    av_nasal_inf_od = Column(Text)
    retina_od = Column(Text)
    excavacion_od = Column(Text)
    papila_detalle_od = Column(Text)
    fijacion_od = Column(Text)
    color_od = Column(Text)
    borde_od = Column(Text)

    # OJO IZQUIERDO
    disco_optico_oi = Column(Text)
    macula_oi = Column(Text)
    vasos_oi = Column(Text)
    retina_periferica_oi = Column(Text)
    av_temp_sup_oi = Column(Text)
    av_temp_inf_oi = Column(Text)
    av_nasal_sup_oi = Column(Text)
    av_nasal_inf_oi = Column(Text)
    retina_oi = Column(Text)
    excavacion_oi = Column(Text)
    papila_detalle_oi = Column(Text)
    fijacion_oi = Column(Text)
    color_oi = Column(Text)
    borde_oi = Column(Text)

    observaciones = Column(Text)
    otros_detalles = Column(Text)
    fecha_examen = Column(DateTime, default=func.now(), nullable=False)

    # Relación
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
            'av_temp_sup_od': self.av_temp_sup_od,
            'av_temp_inf_od': self.av_temp_inf_od,
            'av_nasal_sup_od': self.av_nasal_sup_od,
            'av_nasal_inf_od': self.av_nasal_inf_od,
            'retina_od': self.retina_od,
            'excavacion_od': self.excavacion_od,
            'papila_detalle_od': self.papila_detalle_od,
            'fijacion_od': self.fijacion_od,
            'color_od': self.color_od,
            'borde_od': self.borde_od,
            'disco_optico_oi': self.disco_optico_oi,
            'macula_oi': self.macula_oi,
            'vasos_oi': self.vasos_oi,
            'retina_periferica_oi': self.retina_periferica_oi,
            'av_temp_sup_oi': self.av_temp_sup_oi,
            'av_temp_inf_oi': self.av_temp_inf_oi,
            'av_nasal_sup_oi': self.av_nasal_sup_oi,
            'av_nasal_inf_oi': self.av_nasal_inf_oi,
            'retina_oi': self.retina_oi,
            'excavacion_oi': self.excavacion_oi,
            'papila_detalle_oi': self.papila_detalle_oi,
            'fijacion_oi': self.fijacion_oi,
            'color_oi': self.color_oi,
            'borde_oi': self.borde_oi,
            'observaciones': self.observaciones,
            'otros_detalles': self.otros_detalles,
            'fecha_examen': self.fecha_examen.isoformat() if self.fecha_examen else None
        }

class PresionIntraocular(Base):
    __tablename__ = 'presion_intraocular'

    pio_id = Column(Integer, primary_key=True, autoincrement=True)
    ficha_id = Column(Integer, ForeignKey('fichas_clinicas.ficha_id', ondelete='CASCADE'), nullable=False)
    pio_od = Column(String(10))
    pio_oi = Column(String(10))
    metodo_medicion = Column(String(50))
    hora_medicion = Column(Time)
    observaciones = Column(Text)
    fecha_medicion = Column(DateTime, default=func.now(), nullable=False)

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
    ficha_id = Column(Integer, ForeignKey('fichas_clinicas.ficha_id', ondelete='CASCADE'), nullable=False)
    tipo_campo = Column(String(50))
    resultado_od = Column(Text)
    resultado_oi = Column(Text)
    interpretacion = Column(Text)
    fecha_examen = Column(DateTime, default=func.now(), nullable=False)

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
    ficha_id = Column(Integer, ForeignKey('fichas_clinicas.ficha_id', ondelete='CASCADE'), nullable=False)
    medicamentos = Column(Text)
    tratamiento_no_farmacologico = Column(Text)
    recomendaciones = Column(Text)
    plan_seguimiento = Column(Text)
    proxima_cita = Column(Date)
    urgencia_seguimiento = Column(String(20))
    fecha_tratamiento = Column(DateTime, default=func.now(), nullable=False)

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


class ReflejosPupilares(Base):
    __tablename__ = 'reflejos_pupilares'

    reflejo_id = Column(Integer, primary_key=True, autoincrement=True)
    ficha_id = Column(Integer, ForeignKey('fichas_clinicas.ficha_id', ondelete='CASCADE'), nullable=False)
    acomodativo_uno = Column(Text)
    fotomotor_uno = Column(Text)
    consensual_uno = Column(Text)
    acomodativo_dos = Column(Text)
    fotomotor_dos = Column(Text)
    consensual_dos = Column(Text)
    observaciones = Column(Text)
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)

    ficha = relationship("FichaClinica", foreign_keys=[ficha_id])

    def __repr__(self):
        return f"<ReflejosPupilares(reflejo_id={self.reflejo_id}, ficha_id={self.ficha_id})>"

    def to_dict(self):
        return {
            'reflejo_id': self.reflejo_id,
            'ficha_id': self.ficha_id,
            'acomodativo_uno': self.acomodativo_uno,
            'fotomotor_uno': self.fotomotor_uno,
            'consensual_uno': self.consensual_uno,
            'acomodativo_dos': self.acomodativo_dos,
            'fotomotor_dos': self.fotomotor_dos,
            'consensual_dos': self.consensual_dos,
            'observaciones': self.observaciones,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }


class ParametrosClinicos(Base):
    __tablename__ = 'parametros_clinicos'

    parametro_id = Column(Integer, primary_key=True, autoincrement=True)
    ficha_id = Column(Integer, ForeignKey('fichas_clinicas.ficha_id', ondelete='CASCADE'), nullable=False)
    presion_sistolica = Column(String(10))
    presion_diastolica = Column(String(10))
    saturacion_o2 = Column(String(10))
    glucosa = Column(String(20))
    trigliceridos = Column(String(20))
    ttp = Column(String(20))
    atp = Column(String(20))
    colesterol = Column(String(20))
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)

    ficha = relationship("FichaClinica", foreign_keys=[ficha_id])

    def __repr__(self):
        return f"<ParametrosClinicos(parametro_id={self.parametro_id}, ficha_id={self.ficha_id})>"

    def to_dict(self):
        return {
            'parametro_id': self.parametro_id,
            'ficha_id': self.ficha_id,
            'presion_sistolica': self.presion_sistolica,
            'presion_diastolica': self.presion_diastolica,
            'saturacion_o2': self.saturacion_o2,
            'glucosa': self.glucosa,
            'trigliceridos': self.trigliceridos,
            'ttp': self.ttp,
            'atp': self.atp,
            'colesterol': self.colesterol,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }
