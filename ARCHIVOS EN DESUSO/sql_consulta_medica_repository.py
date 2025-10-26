"""Archivado: repository consulta medica (sin uso)"""
# from sqlalchemy.orm import Session, joinedload
# from sqlalchemy.exc import SQLAlchemyError
# from app.domain.models.consulta_medica import ConsultaMedica
# from app.domain.models.paciente import Paciente
# from app.infraestructure.utils.db_session import get_db_session
# from typing import List, Optional
# from datetime import datetime, date
# 
# class SqlConsultaMedicaRepository:
#     def __init__(self):
#         pass
#     
#     def get_all_consultas(self) -> List[ConsultaMedica]:
#         """Obtiene todas las consultas médicas"""
#         with get_db_session() as session:
#             try:
#                 return session.query(ConsultaMedica)\
#                     .options(joinedload(ConsultaMedica.paciente))\
#                     .order_by(ConsultaMedica.fecha_consulta.desc()).all()
#             except SQLAlchemyError as e:
#                 print(f"Error al obtener consultas: {str(e)}")
#                 return []
#     
#     def get_consulta_by_id(self, consulta_id: int) -> Optional[ConsultaMedica]:
#         """Obtiene una consulta por ID"""
#         with get_db_session() as session:
#             try:
#                 return session.query(ConsultaMedica)\
#                     .options(joinedload(ConsultaMedica.paciente))\
#                     .filter(ConsultaMedica.id == consulta_id).first()
#             except SQLAlchemyError as e:
#                 print(f"Error al obtener consulta por ID: {str(e)}")
#                 return None
#     
#     def get_consultas_by_paciente(self, paciente_id: int) -> List[ConsultaMedica]:
#         """Obtiene consultas de un paciente específico"""
#         with get_db_session() as session:
#             try:
#                 return session.query(ConsultaMedica)\
#                     .filter(ConsultaMedica.paciente_id == paciente_id)\
#                     .order_by(ConsultaMedica.fecha_consulta.desc()).all()
#             except SQLAlchemyError as e:
#                 print(f"Error al obtener consultas del paciente: {str(e)}")
#                 return []
#     
#     def get_consultas_by_fecha(self, fecha_inicio: date, fecha_fin: date) -> List[ConsultaMedica]:
#         """Obtiene consultas en un rango de fechas"""
#         with get_db_session() as session:
#             try:
#                 return session.query(ConsultaMedica)\
#                     .options(joinedload(ConsultaMedica.paciente))\
#                     .filter(ConsultaMedica.fecha_consulta.between(fecha_inicio, fecha_fin))\
#                     .order_by(ConsultaMedica.fecha_consulta.desc()).all()
#             except SQLAlchemyError as e:
#                 print(f"Error al obtener consultas por fecha: {str(e)}")
#                 return []
#     
#     def get_consultas_by_estado(self, estado: str) -> List[ConsultaMedica]:
#         """Obtiene consultas por estado"""
#         with get_db_session() as session:
#             try:
#                 return session.query(ConsultaMedica)\
#                     .options(joinedload(ConsultaMedica.paciente))\
#                     .filter(ConsultaMedica.estado == estado)\
#                     .order_by(ConsultaMedica.fecha_consulta.desc()).all()
#             except SQLAlchemyError as e:
#                 print(f"Error al obtener consultas por estado: {str(e)}")
#                 return []
#     
#     def create_consulta(self, consulta_data: dict) -> Optional[ConsultaMedica]:
#         """Crea una nueva consulta médica"""
#         with get_db_session() as session:
#             try:
#                 consulta = ConsultaMedica(**consulta_data)
#                 session.add(consulta)
#                 session.commit()
#                 session.refresh(consulta)
#                 return consulta
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 print(f"Error al crear consulta: {str(e)}")
#                 return None
#     
#     def update_consulta(self, consulta_id: int, consulta_data: dict) -> Optional[ConsultaMedica]:
#         """Actualiza una consulta existente"""
#         with get_db_session() as session:
#             try:
#                 consulta = session.query(ConsultaMedica).filter(ConsultaMedica.id == consulta_id).first()
#                 if consulta:
#                     for key, value in consulta_data.items():
#                         if hasattr(consulta, key):
#                             setattr(consulta, key, value)
#                     session.commit()
#                     session.refresh(consulta)
#                     return consulta
#                 return None
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 print(f"Error al actualizar consulta: {str(e)}")
#                 return None
#     
#     def delete_consulta(self, consulta_id: int) -> bool:
#         """Elimina una consulta"""
#         with get_db_session() as session:
#             try:
#                 consulta = session.query(ConsultaMedica).filter(ConsultaMedica.id == consulta_id).first()
#                 if consulta:
#                     session.delete(consulta)
#                     session.commit()
#                     return True
#                 return False
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 print(f"Error al eliminar consulta: {str(e)}")
#                 return False
#     
#     def count_consultas(self) -> int:
#         """Cuenta el total de consultas"""
#         with get_db_session() as session:
#             try:
#                 return session.query(ConsultaMedica).count()
#             except SQLAlchemyError as e:
#                 print(f"Error al contar consultas: {str(e)}")
#                 return 0
#     
#     def count_consultas_hoy(self) -> int:
#         """Cuenta las consultas de hoy"""
#         with get_db_session() as session:
#             try:
#                 hoy = date.today()
#                 return session.query(ConsultaMedica)\
#                     .filter(ConsultaMedica.fecha_consulta >= hoy)\
#                     .filter(ConsultaMedica.fecha_consulta < hoy + datetime.timedelta(days=1))\
#                     .count()
#             except SQLAlchemyError as e:
#                 print(f"Error al contar consultas de hoy: {str(e)}")
#                 return 0
