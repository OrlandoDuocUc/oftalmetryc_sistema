from __future__ import annotations

from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.domain.models.biomicroscopia import Biomicroscopia
from app.domain.models.examenes_medicos import (
    FondoOjo,
    ReflejosPupilares,
    ParametrosClinicos,
)


def _assign_attributes(model: Any, data: Dict[str, Any], allowed: Optional[set] = None) -> None:
    """Setea atributos en *model* solo si existen y el valor es distinto de None.

    Args:
        model: instancia SQLAlchemy a modificar.
        data: diccionario con valores entrantes.
        allowed: conjunto opcional de campos permitidos; si es None se usan los keys presentes.
    """

    fields = allowed or set(data.keys())
    for key in fields:
        if key in data and hasattr(model, key):
            setattr(model, key, data[key])


class BiomicroscopiaExamRepository:
    """Repositorio auxiliar para las secciones del examen de biomicroscopía.

    Todas las operaciones se ejecutan sobre una sesión inyectada; el commit/rollback
    queda a cargo del llamador para permitir transacciones compuestas.
    """

    def __init__(self, session: Session):
        self.session = session

    # ------------------------------------------------------------------
    # Biomicroscopía anterior
    # ------------------------------------------------------------------
    def upsert_biomicroscopia(self, ficha_id: int, data: Dict[str, Any]) -> Biomicroscopia:
        record = (
            self.session.query(Biomicroscopia)
            .filter(Biomicroscopia.ficha_id == ficha_id)
            .first()
        )

        if not record:
            record = Biomicroscopia(ficha_id=ficha_id)
            self.session.add(record)

        allowed = {
            'parpados_od', 'conjuntiva_od', 'cornea_od', 'camara_anterior_od', 'iris_od',
            'pupila_od_mm', 'pupila_od_reaccion', 'cristalino_od', 'pupila_desc_od',
            'pestanas_od', 'conjuntiva_bulbar_od', 'conjuntiva_tarsal_od', 'orbita_od',
            'pliegue_semilunar_od', 'caruncula_od', 'conductos_lagrimales_od',
            'parpado_superior_od', 'parpado_inferior_od',
            'parpados_oi', 'conjuntiva_oi', 'cornea_oi', 'camara_anterior_oi', 'iris_oi',
            'pupila_oi_mm', 'pupila_oi_reaccion', 'cristalino_oi', 'pupila_desc_oi',
            'pestanas_oi', 'conjuntiva_bulbar_oi', 'conjuntiva_tarsal_oi', 'orbita_oi',
            'pliegue_semilunar_oi', 'caruncula_oi', 'conductos_lagrimales_oi',
            'parpado_superior_oi', 'parpado_inferior_oi', 'observaciones_generales',
            'otros_detalles'
        }
        _assign_attributes(record, data, allowed)
        return record

    def get_biomicroscopia(self, ficha_id: int) -> Optional[Dict[str, Any]]:
        record = (
            self.session.query(Biomicroscopia)
            .filter(Biomicroscopia.ficha_id == ficha_id)
            .first()
        )
        return record.to_dict() if record else None

    # ------------------------------------------------------------------
    # Reflejos pupilares
    # ------------------------------------------------------------------
    def upsert_reflejos(self, ficha_id: int, data: Dict[str, Any]) -> ReflejosPupilares:
        record = (
            self.session.query(ReflejosPupilares)
            .filter(ReflejosPupilares.ficha_id == ficha_id)
            .first()
        )

        if not record:
            record = ReflejosPupilares(ficha_id=ficha_id)
            self.session.add(record)

        allowed = {
            'acomodativo_uno', 'fotomotor_uno', 'consensual_uno',
            'acomodativo_dos', 'fotomotor_dos', 'consensual_dos', 'observaciones'
        }
        _assign_attributes(record, data, allowed)
        return record

    def get_reflejos(self, ficha_id: int) -> Optional[Dict[str, Any]]:
        record = (
            self.session.query(ReflejosPupilares)
            .filter(ReflejosPupilares.ficha_id == ficha_id)
            .first()
        )
        return record.to_dict() if record else None

    # ------------------------------------------------------------------
    # Fondo de ojo extendido
    # ------------------------------------------------------------------
    def upsert_fondo_ojo(self, ficha_id: int, data: Dict[str, Any]) -> FondoOjo:
        record = (
            self.session.query(FondoOjo)
            .filter(FondoOjo.ficha_id == ficha_id)
            .first()
        )

        if not record:
            record = FondoOjo(ficha_id=ficha_id)
            self.session.add(record)

        allowed = {
            'disco_optico_od', 'macula_od', 'vasos_od', 'retina_periferica_od',
            'av_temp_sup_od', 'av_temp_inf_od', 'av_nasal_sup_od', 'av_nasal_inf_od',
            'retina_od', 'excavacion_od', 'papila_detalle_od', 'fijacion_od',
            'color_od', 'borde_od',
            'disco_optico_oi', 'macula_oi', 'vasos_oi', 'retina_periferica_oi',
            'av_temp_sup_oi', 'av_temp_inf_oi', 'av_nasal_sup_oi', 'av_nasal_inf_oi',
            'retina_oi', 'excavacion_oi', 'papila_detalle_oi', 'fijacion_oi',
            'color_oi', 'borde_oi', 'observaciones', 'otros_detalles'
        }
        _assign_attributes(record, data, allowed)
        return record

    def get_fondo_ojo(self, ficha_id: int) -> Optional[Dict[str, Any]]:
        record = (
            self.session.query(FondoOjo)
            .filter(FondoOjo.ficha_id == ficha_id)
            .first()
        )
        return record.to_dict() if record else None

    # ------------------------------------------------------------------
    # Parámetros clínicos
    # ------------------------------------------------------------------
    def upsert_parametros(self, ficha_id: int, data: Dict[str, Any]) -> ParametrosClinicos:
        record = (
            self.session.query(ParametrosClinicos)
            .filter(ParametrosClinicos.ficha_id == ficha_id)
            .first()
        )

        if not record:
            record = ParametrosClinicos(ficha_id=ficha_id)
            self.session.add(record)

        allowed = {
            'presion_sistolica', 'presion_diastolica', 'saturacion_o2',
            'glucosa', 'trigliceridos', 'ttp', 'atp', 'colesterol'
        }
        _assign_attributes(record, data, allowed)
        return record

    def get_parametros(self, ficha_id: int) -> Optional[Dict[str, Any]]:
        record = (
            self.session.query(ParametrosClinicos)
            .filter(ParametrosClinicos.ficha_id == ficha_id)
            .first()
        )
        return record.to_dict() if record else None

    # ------------------------------------------------------------------
    # Lectura agregada
    # ------------------------------------------------------------------
    def obtener_examen_completo(self, ficha_id: int) -> Dict[str, Any]:
        return {
            'biomicroscopia': self.get_biomicroscopia(ficha_id),
            'reflejos': self.get_reflejos(ficha_id),
            'fondo_ojo': self.get_fondo_ojo(ficha_id),
            'parametros': self.get_parametros(ficha_id),
        }
