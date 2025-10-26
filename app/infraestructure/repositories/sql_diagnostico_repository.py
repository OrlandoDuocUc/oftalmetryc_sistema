"""Repositorio alineado con la tabla diagnosticos.

Las operaciones definidas aqui utilizan las columnas vigentes (diagnostico_principal, cie_10_principal, etc.), por lo que este modulo puede usarse inmediatamente para gestionar diagnosticos en la aplicacion.
"""

from typing import Dict, List, Optional

from sqlalchemy.exc import SQLAlchemyError

from app.domain.models.diagnostico import Diagnostico
from app.infraestructure.utils.db_session import get_db_session


class SqlDiagnosticoRepository:
    """CRUD simple para la tabla `diagnosticos`."""

    # ---------------------------- Lecturas ---------------------------- #
    def get_all_diagnosticos(self) -> List[Diagnostico]:
        """Devuelve todos los diagnosticos ordenados por fecha (recientes primero)."""
        with get_db_session() as session:
            try:
                return (
                    session.query(Diagnostico)
                    .order_by(Diagnostico.fecha_diagnostico.desc())
                    .all()
                )
            except SQLAlchemyError as exc:
                print(f"Error al obtener diagnosticos: {exc}")
                return []

    def get_diagnostico_by_id(self, diagnostico_id: int) -> Optional[Diagnostico]:
        """Busca un diagnostico por su identificador."""
        with get_db_session() as session:
            try:
                return (
                    session.query(Diagnostico)
                    .filter(Diagnostico.diagnostico_id == diagnostico_id)
                    .first()
                )
            except SQLAlchemyError as exc:
                print(f"Error al obtener diagnostico por ID: {exc}")
                return None

    def get_diagnosticos_by_ficha(self, ficha_id: int) -> List[Diagnostico]:
        """Devuelve los diagnosticos asociados a una ficha clinica."""
        with get_db_session() as session:
            try:
                return (
                    session.query(Diagnostico)
                    .filter(Diagnostico.ficha_id == ficha_id)
                    .order_by(Diagnostico.fecha_diagnostico.desc())
                    .all()
                )
            except SQLAlchemyError as exc:
                print(f"Error al obtener diagnosticos por ficha: {exc}")
                return []

    def search_diagnosticos(self, term: str) -> List[Diagnostico]:
        """Busqueda libre entre diagnostico principal/secundarios y codigos CIE10."""
        like_value = f"%{term}%"
        with get_db_session() as session:
            try:
                return (
                    session.query(Diagnostico)
                    .filter(
                        (Diagnostico.diagnostico_principal.ilike(like_value))
                        | (Diagnostico.diagnosticos_secundarios.ilike(like_value))
                        | (Diagnostico.cie_10_principal.ilike(like_value))
                        | (Diagnostico.cie_10_secundarios.ilike(like_value))
                    )
                    .order_by(Diagnostico.fecha_diagnostico.desc())
                    .all()
                )
            except SQLAlchemyError as exc:
                print(f"Error al buscar diagnosticos: {exc}")
                return []

    # ---------------------------- Escrituras -------------------------- #
    def create_diagnostico(self, data: Dict) -> Optional[Diagnostico]:
        """Inserta un nuevo registro en `diagnosticos`."""
        with get_db_session() as session:
            try:
                diagnostico = Diagnostico(
                    ficha_id=data["ficha_id"],
                    diagnostico_principal=data.get("diagnostico_principal"),
                    diagnosticos_secundarios=data.get("diagnosticos_secundarios"),
                    cie_10_principal=data.get("cie_10_principal"),
                    cie_10_secundarios=data.get("cie_10_secundarios"),
                    severidad=data.get("severidad"),
                    observaciones=data.get("observaciones"),
                )
                session.add(diagnostico)
                session.commit()
                session.refresh(diagnostico)
                return diagnostico
            except (KeyError, SQLAlchemyError) as exc:
                session.rollback()
                print(f"Error al crear diagnostico: {exc}")
                return None

    def delete_diagnostico(self, diagnostico_id: int) -> bool:
        """Elimina un diagnostico existente."""
        with get_db_session() as session:
            try:
                diagnostico = (
                    session.query(Diagnostico)
                    .filter(Diagnostico.diagnostico_id == diagnostico_id)
                    .first()
                )
                if not diagnostico:
                    return False
                session.delete(diagnostico)
                session.commit()
                return True
            except SQLAlchemyError as exc:
                session.rollback()
                print(f"Error al eliminar diagnostico: {exc}")
                return False
