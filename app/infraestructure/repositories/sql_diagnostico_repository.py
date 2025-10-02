from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.domain.models.diagnostico import Diagnostico
from app.infraestructure.utils.db_session import get_db_session
from typing import List, Optional

class SqlDiagnosticoRepository:
    def __init__(self):
        pass
    
    def get_all_diagnosticos(self) -> List[Diagnostico]:
        """Obtiene todos los diagnósticos"""
        with get_db_session() as session:
            try:
                return session.query(Diagnostico).order_by(Diagnostico.categoria, Diagnostico.codigo_cie10).all()
            except SQLAlchemyError as e:
                print(f"Error al obtener diagnósticos: {str(e)}")
                return []
    
    def get_diagnostico_by_id(self, diagnostico_id: int) -> Optional[Diagnostico]:
        """Obtiene un diagnóstico por ID"""
        with get_db_session() as session:
            try:
                return session.query(Diagnostico).filter(Diagnostico.id == diagnostico_id).first()
            except SQLAlchemyError as e:
                print(f"Error al obtener diagnóstico por ID: {str(e)}")
                return None
    
    def get_diagnosticos_by_categoria(self, categoria: str) -> List[Diagnostico]:
        """Obtiene diagnósticos por categoría"""
        with get_db_session() as session:
            try:
                return session.query(Diagnostico)\
                    .filter(Diagnostico.categoria == categoria)\
                    .order_by(Diagnostico.codigo_cie10).all()
            except SQLAlchemyError as e:
                print(f"Error al obtener diagnósticos por categoría: {str(e)}")
                return []
    
    def search_diagnosticos(self, query: str) -> List[Diagnostico]:
        """Busca diagnósticos por código o descripción"""
        with get_db_session() as session:
            try:
                search_term = f"%{query}%"
                return session.query(Diagnostico).filter(
                    (Diagnostico.codigo_cie10.ilike(search_term)) |
                    (Diagnostico.descripcion.ilike(search_term))
                ).order_by(Diagnostico.codigo_cie10).all()
            except SQLAlchemyError as e:
                print(f"Error al buscar diagnósticos: {str(e)}")
                return []
    
    def get_categorias(self) -> List[str]:
        """Obtiene todas las categorías disponibles"""
        with get_db_session() as session:
            try:
                result = session.query(Diagnostico.categoria)\
                    .distinct()\
                    .filter(Diagnostico.categoria.isnot(None))\
                    .order_by(Diagnostico.categoria).all()
                return [categoria[0] for categoria in result]
            except SQLAlchemyError as e:
                print(f"Error al obtener categorías: {str(e)}")
                return []