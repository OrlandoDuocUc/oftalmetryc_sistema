from __future__ import annotations

from typing import Any, Dict, Optional

from app.infraestructure.utils.db import SessionLocal
from app.infraestructure.repositories.biomicroscopia_repository import (
    BiomicroscopiaExamRepository,
)
from app.domain.models.examenes_medicos import DiagnosticoMedico, Tratamiento


class BiomicroscopiaService:
    """Caso de uso para gestionar el examen de biomicroscopía completo."""

    def obtener_examen(self, ficha_id: int) -> Dict[str, Optional[Dict[str, Any]]]:
        session = SessionLocal()
        try:
            repo = BiomicroscopiaExamRepository(session)
            data = repo.obtener_examen_completo(ficha_id)

            diag = (
                session.query(DiagnosticoMedico)
                .filter(DiagnosticoMedico.ficha_id == ficha_id)
                .order_by(DiagnosticoMedico.fecha_diagnostico.desc())
                .first()
            )
            tx = (
                session.query(Tratamiento)
                .filter(Tratamiento.ficha_id == ficha_id)
                .order_by(Tratamiento.fecha_tratamiento.desc())
                .first()
            )

            data['diagnostico'] = diag.to_dict() if diag else None
            data['tratamiento'] = tx.to_dict() if tx else None

            return data
        finally:
            session.close()

    def guardar_examen(self, ficha_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        session = SessionLocal()
        try:
            repo = BiomicroscopiaExamRepository(session)

            seccion_bio = payload.get('biomicroscopia') or {}
            seccion_reflejos = payload.get('reflejos') or {}
            seccion_fondo = payload.get('fondo_ojo') or {}
            seccion_parametros = payload.get('parametros') or {}

            bio = repo.upsert_biomicroscopia(ficha_id, seccion_bio)
            reflejos = repo.upsert_reflejos(ficha_id, seccion_reflejos)
            fondo = repo.upsert_fondo_ojo(ficha_id, seccion_fondo)
            parametros = repo.upsert_parametros(ficha_id, seccion_parametros)

            session.commit()

            return {
                'biomicroscopia': bio.to_dict(),
                'reflejos': reflejos.to_dict(),
                'fondo_ojo': fondo.to_dict(),
                'parametros': parametros.to_dict(),
            }
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
