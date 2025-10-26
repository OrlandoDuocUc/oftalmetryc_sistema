"""
from app.infraestructure.repositories.sql_paciente_repository import SqlPacienteRepository
from typing import List, Optional, Dict

class PacienteService:
    def __init__(self):
        self.paciente_repository = SqlPacienteRepository()
'''
    def get_all_pacientes(self) -> List[Dict]:
        """Obtiene todos los pacientes"""
        try:
            pacientes = self.paciente_repository.get_all_pacientes()
            return [paciente.to_dict() for paciente in pacientes]
        except Exception as e:
            print(f"Error en servicio de pacientes: {str(e)}")
            return []
    
    def get_paciente_by_id(self, paciente_id: int) -> Optional[Dict]:
        """Obtiene un paciente por ID"""
        try:
            paciente = self.paciente_repository.get_paciente_by_id(paciente_id)
            return paciente.to_dict() if paciente else None
        except Exception as e:
            print(f"Error al obtener paciente: {str(e)}")
            return None
    
    def search_pacientes(self, query: str) -> List[Dict]:
        """Busca pacientes"""
        try:
            pacientes = self.paciente_repository.search_pacientes(query)
            return [paciente.to_dict() for paciente in pacientes]
        except Exception as e:
            print(f"Error al buscar pacientes: {str(e)}")
            return []
    
    def create_paciente(self, paciente_data: Dict) -> Optional[Dict]:
        """Crea un nuevo paciente"""
        try:
            # Validar RUT único
            existing_paciente = self.paciente_repository.get_paciente_by_rut(paciente_data.get('rut'))
            if existing_paciente:
                raise ValueError("Ya existe un paciente con este RUT")
            
            paciente = self.paciente_repository.create_paciente(paciente_data)
            return paciente.to_dict() if paciente else None
        except Exception as e:
            print(f"Error al crear paciente: {str(e)}")
            return None
    
    def update_paciente(self, paciente_id: int, paciente_data: Dict) -> Optional[Dict]:
        """Actualiza un paciente existente"""
        try:
            # Validar RUT único si se está cambiando
            if 'rut' in paciente_data:
                existing_paciente = self.paciente_repository.get_paciente_by_rut(paciente_data['rut'])
                if existing_paciente and existing_paciente.id != paciente_id:
                    raise ValueError("Ya existe otro paciente con este RUT")
            
            paciente = self.paciente_repository.update_paciente(paciente_id, paciente_data)
            return paciente.to_dict() if paciente else None
        except Exception as e:
            print(f"Error al actualizar paciente: {str(e)}")
            return None
    
    def delete_paciente(self, paciente_id: int) -> bool:
        """Elimina un paciente"""
        try:
            return self.paciente_repository.delete_paciente(paciente_id)
        except Exception as e:
            print(f"Error al eliminar paciente: {str(e)}")
            return False
    
    def count_pacientes(self) -> int:
        """Cuenta el total de pacientes"""
        try:
            return self.paciente_repository.count_pacientes()
        except Exception as e:
            print(f"Error al contar pacientes: {str(e)}")
            return 0
'''
    def validate_rut(self, rut: str) -> bool:
        """Validación simplificada para demo: acepta cédula ecuatoriana (10 dígitos)"""
        try:
            # Eliminar puntos y guión
            rut_clean = rut.replace('.', '').replace('-', '').strip()
            
            # Para demo: aceptar 10 dígitos (cédula ecuatoriana)
            if len(rut_clean) == 10 and rut_clean.isdigit():
                return True
            
            # Mantener compatibilidad básica con cualquier formato
            if len(rut_clean) >= 2:
                return True
            
            return False
        except:
            return False
            
"""