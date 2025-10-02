from app.infraestructure.repositories.sql_consulta_medica_repository import SqlConsultaMedicaRepository
from app.infraestructure.repositories.sql_diagnostico_repository import SqlDiagnosticoRepository
from typing import List, Optional, Dict
from datetime import datetime, date

class ConsultaMedicaService:
    def __init__(self):
        self.consulta_repository = SqlConsultaMedicaRepository()
        self.diagnostico_repository = SqlDiagnosticoRepository()
    
    def get_all_consultas(self) -> List[Dict]:
        """Obtiene todas las consultas médicas"""
        try:
            consultas = self.consulta_repository.get_all_consultas()
            return [consulta.to_dict() for consulta in consultas]
        except Exception as e:
            print(f"Error en servicio de consultas: {str(e)}")
            return []
    
    def get_consulta_by_id(self, consulta_id: int) -> Optional[Dict]:
        """Obtiene una consulta por ID"""
        try:
            consulta = self.consulta_repository.get_consulta_by_id(consulta_id)
            return consulta.to_dict() if consulta else None
        except Exception as e:
            print(f"Error al obtener consulta: {str(e)}")
            return None
    
    def get_consultas_by_paciente(self, paciente_id: int) -> List[Dict]:
        """Obtiene consultas de un paciente"""
        try:
            consultas = self.consulta_repository.get_consultas_by_paciente(paciente_id)
            return [consulta.to_dict() for consulta in consultas]
        except Exception as e:
            print(f"Error al obtener consultas del paciente: {str(e)}")
            return []
    
    def create_consulta(self, consulta_data: Dict) -> Optional[Dict]:
        """Crea una nueva consulta médica"""
        try:
            # Procesar fecha_consulta si viene como string
            if 'fecha_consulta' in consulta_data and isinstance(consulta_data['fecha_consulta'], str):
                if consulta_data['fecha_consulta'].strip():  # Solo si no está vacía
                    consulta_data['fecha_consulta'] = datetime.fromisoformat(consulta_data['fecha_consulta'])
                else:
                    consulta_data['fecha_consulta'] = datetime.now()  # Fecha actual por defecto
            
            # Procesar proxima_cita si viene como string y no está vacía
            if 'proxima_cita' in consulta_data and isinstance(consulta_data['proxima_cita'], str):
                if consulta_data['proxima_cita'].strip():  # Solo si no está vacía
                    consulta_data['proxima_cita'] = datetime.strptime(consulta_data['proxima_cita'], '%Y-%m-%d').date()
                else:
                    consulta_data.pop('proxima_cita', None)  # Remover si está vacía
            
            consulta = self.consulta_repository.create_consulta(consulta_data)
            return consulta.to_dict() if consulta else None
        except Exception as e:
            print(f"Error al crear consulta: {str(e)}")
            return None
    
    def update_consulta(self, consulta_id: int, consulta_data: Dict) -> Optional[Dict]:
        """Actualiza una consulta existente"""
        try:
            # Procesar fechas si vienen como string
            if 'fecha_consulta' in consulta_data and isinstance(consulta_data['fecha_consulta'], str):
                if consulta_data['fecha_consulta'].strip():  # Solo si no está vacía
                    consulta_data['fecha_consulta'] = datetime.fromisoformat(consulta_data['fecha_consulta'])
                else:
                    consulta_data['fecha_consulta'] = datetime.now()  # Fecha actual por defecto
            
            if 'proxima_cita' in consulta_data and isinstance(consulta_data['proxima_cita'], str):
                if consulta_data['proxima_cita'].strip():  # Solo si no está vacía
                    consulta_data['proxima_cita'] = datetime.strptime(consulta_data['proxima_cita'], '%Y-%m-%d').date()
                else:
                    consulta_data.pop('proxima_cita', None)  # Remover si está vacía
            
            consulta = self.consulta_repository.update_consulta(consulta_id, consulta_data)
            return consulta.to_dict() if consulta else None
        except Exception as e:
            print(f"Error al actualizar consulta: {str(e)}")
            return None
    
    def delete_consulta(self, consulta_id: int) -> bool:
        """Elimina una consulta"""
        try:
            return self.consulta_repository.delete_consulta(consulta_id)
        except Exception as e:
            print(f"Error al eliminar consulta: {str(e)}")
            return False
    
    def get_consultas_hoy(self) -> List[Dict]:
        """Obtiene las consultas de hoy"""
        try:
            hoy = date.today()
            consultas = self.consulta_repository.get_consultas_by_fecha(hoy, hoy)
            return [consulta.to_dict() for consulta in consultas]
        except Exception as e:
            print(f"Error al obtener consultas de hoy: {str(e)}")
            return []
    
    def get_consultas_by_estado(self, estado: str) -> List[Dict]:
        """Obtiene consultas por estado"""
        try:
            consultas = self.consulta_repository.get_consultas_by_estado(estado)
            return [consulta.to_dict() for consulta in consultas]
        except Exception as e:
            print(f"Error al obtener consultas por estado: {str(e)}")
            return []
    
    def count_consultas(self) -> int:
        """Cuenta el total de consultas"""
        try:
            return self.consulta_repository.count_consultas()
        except Exception as e:
            print(f"Error al contar consultas: {str(e)}")
            return 0
    
    def count_consultas_hoy(self) -> int:
        """Cuenta las consultas de hoy"""
        try:
            return self.consulta_repository.count_consultas_hoy()
        except Exception as e:
            print(f"Error al contar consultas de hoy: {str(e)}")
            return 0
    
    def get_diagnosticos_disponibles(self) -> List[Dict]:
        """Obtiene todos los diagnósticos disponibles"""
        try:
            diagnosticos = self.diagnostico_repository.get_all_diagnosticos()
            return [diagnostico.to_dict() for diagnostico in diagnosticos]
        except Exception as e:
            print(f"Error al obtener diagnósticos: {str(e)}")
            return []
    
    def search_diagnosticos(self, query: str) -> List[Dict]:
        """Busca diagnósticos"""
        try:
            diagnosticos = self.diagnostico_repository.search_diagnosticos(query)
            return [diagnostico.to_dict() for diagnostico in diagnosticos]
        except Exception as e:
            print(f"Error al buscar diagnósticos: {str(e)}")
            return []