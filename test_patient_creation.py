#!/usr/bin/env python3
"""
Script para probar creación de pacientes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.domain.use_cases.services.paciente_service import PacienteService
from app.infraestructure.repositories.sql_paciente_repository import SqlPacienteRepository

def test_patient_creation():
    """Prueba la creación de un paciente"""
    
    # Inicializar servicios
    paciente_repository = SqlPacienteRepository()
    paciente_service = PacienteService(paciente_repository)
    
    # Datos de prueba
    test_data = {
        'rut': '1234567890',  # Cédula ecuatoriana de prueba
        'nombre': 'Juan Carlos',
        'apellido': 'Pérez González',
        'fecha_nacimiento': '1990-05-15',
        'telefono': '0987654321',
        'email': 'juan.perez@email.com',
        'direccion': 'Av. Amazonas y Naciones Unidas, Quito',
        'ocupacion': 'Ingeniero',
        'contacto_emergencia': 'María Pérez',
        'telefono_emergencia': '0987654322',
        'observaciones': 'Paciente de prueba para demo'
    }
    
    try:
        print("🔍 Probando validación de cédula...")
        is_valid = paciente_service.validate_rut(test_data['rut'])
        print(f"✅ Cédula {test_data['rut']} es válida: {is_valid}")
        
        if is_valid:
            print("\n🏥 Intentando crear paciente...")
            resultado = paciente_service.create_paciente(test_data)
            print(f"✅ Paciente creado exitosamente: {resultado}")
            return True
        else:
            print("❌ Cédula no válida")
            return False
            
    except Exception as e:
        print(f"❌ Error al crear paciente: {str(e)}")
        return False

if __name__ == "__main__":
    print("🇪🇨 Probando sistema de pacientes - Demo Ecuador")
    print("=" * 50)
    
    success = test_patient_creation()
    
    if success:
        print("\n🎉 ¡Prueba exitosa! El sistema está funcionando correctamente.")
    else:
        print("\n🚨 La prueba falló. Revisar configuración.")