
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.domain.models.paciente import Paciente
from app.infraestructure.utils.db_session import get_db_session
from typing import List, Optional

class SqlPacienteRepository:
    def __init__(self):
        pass
    
    def get_all_pacientes(self) -> List[Paciente]:
        """Obtiene todos los pacientes"""
        with get_db_session() as session:
            try:
                return session.query(Paciente).order_by(Paciente.apellido, Paciente.nombre).all()
            except SQLAlchemyError as e:
                print(f"Error al obtener pacientes: {str(e)}")
                return []
    
    def get_paciente_by_id(self, paciente_id: int) -> Optional[Paciente]:
        """Obtiene un paciente por ID"""
        with get_db_session() as session:
            try:
                return session.query(Paciente).filter(Paciente.id == paciente_id).first()
            except SQLAlchemyError as e:
                print(f"Error al obtener paciente por ID: {str(e)}")
                return None
    
    def get_paciente_by_rut(self, rut: str) -> Optional[Paciente]:
        """Obtiene un paciente por RUT"""
        with get_db_session() as session:
            try:
                return session.query(Paciente).filter(Paciente.rut == rut).first()
            except SQLAlchemyError as e:
                print(f"Error al obtener paciente por RUT: {str(e)}")
                return None
    
    def search_pacientes(self, query: str) -> List[Paciente]:
        """Busca pacientes por nombre, apellido o RUT"""
        with get_db_session() as session:
            try:
                search_term = f"%{query}%"
                return session.query(Paciente).filter(
                    (Paciente.nombre.ilike(search_term)) |
                    (Paciente.apellido.ilike(search_term)) |
                    (Paciente.rut.ilike(search_term))
                ).order_by(Paciente.apellido, Paciente.nombre).all()
            except SQLAlchemyError as e:
                print(f"Error al buscar pacientes: {str(e)}")
                return []
    
    def create_paciente(self, paciente_data: dict) -> Optional[Paciente]:
        """Crea un nuevo paciente"""
        with get_db_session() as session:
            try:
                paciente = Paciente(**paciente_data)
                session.add(paciente)
                session.commit()
                session.refresh(paciente)
                return paciente
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error al crear paciente: {str(e)}")
                return None
    
    def update_paciente(self, paciente_id: int, paciente_data: dict) -> Optional[Paciente]:
        """Actualiza un paciente existente"""
        with get_db_session() as session:
            try:
                paciente = session.query(Paciente).filter(Paciente.id == paciente_id).first()
                if paciente:
                    for key, value in paciente_data.items():
                        if hasattr(paciente, key):
                            setattr(paciente, key, value)
                    session.commit()
                    session.refresh(paciente)
                    return paciente
                return None
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error al actualizar paciente: {str(e)}")
                return None
    
    def delete_paciente(self, paciente_id: int) -> bool:
        """Elimina un paciente"""
        with get_db_session() as session:
            try:
                paciente = session.query(Paciente).filter(Paciente.id == paciente_id).first()
                if paciente:
                    session.delete(paciente)
                    session.commit()
                    return True
                return False
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error al eliminar paciente: {str(e)}")
                return False
    
    def count_pacientes(self) -> int:
        """Cuenta el total de pacientes"""
        with get_db_session() as session:
            try:
                return session.query(Paciente).count()
            except SQLAlchemyError as e:
                print(f"Error al contar pacientes: {str(e)}")
                return 0
"""                