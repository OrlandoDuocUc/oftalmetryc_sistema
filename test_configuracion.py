#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración de la base de datos
según la estructura SQL real de optica_bd
"""

import sys
import os

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    try:
        from app.infraestructure.utils.db import SessionLocal
        session = SessionLocal()
        print("✅ Conexión a la base de datos exitosa")
        session.close()
        return True
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        return False

def test_models_import():
    """Prueba la importación de todos los modelos"""
    try:
        from app.domain.models.paciente import PacienteMedico
        from app.domain.models.consulta_medica import FichaClinica
        from app.domain.models.biomicroscopia import Biomicroscopia
        from app.domain.models.examenes_medicos import FondoOjo, PresionIntraocular
        from app.domain.models.user import User
        from app.domain.models.cliente import Cliente
        
        print("✅ Todos los modelos importados correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al importar modelos: {e}")
        return False

def test_models_structure():
    """Prueba la estructura de los modelos"""
    try:
        from app.domain.models.paciente import PacienteMedico
        from app.domain.models.consulta_medica import FichaClinica
        
        # Verificar que las tablas tienen los nombres correctos
        assert PacienteMedico.__tablename__ == 'pacientes_medicos'
        assert FichaClinica.__tablename__ == 'fichas_clinicas'
        
        # Verificar campos clave
        pm = PacienteMedico()
        assert hasattr(pm, 'paciente_medico_id')
        assert hasattr(pm, 'numero_ficha')
        assert hasattr(pm, 'cliente_id')
        
        fc = FichaClinica()
        assert hasattr(fc, 'ficha_id')
        assert hasattr(fc, 'paciente_medico_id')
        assert hasattr(fc, 'numero_consulta')
        assert hasattr(fc, 'av_od_sc')  # Agudeza visual ojo derecho sin corrección
        assert hasattr(fc, 'esfera_od')  # Refracción esfera ojo derecho
        
        print("✅ Estructura de modelos verificada correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en estructura de modelos: {e}")
        return False

def test_controllers():
    """Prueba los controladores"""
    try:
        from adapters.input.flask_app.controllers.paciente_controller import PacienteMedicoController
        from adapters.input.flask_app.controllers.ficha_clinica_controller_nuevo import FichaClinicaController
        
        pm_controller = PacienteMedicoController()
        fc_controller = FichaClinicaController()
        
        print("✅ Controladores inicializados correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en controladores: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("🔍 INICIANDO PRUEBAS DE CONFIGURACIÓN")
    print("=" * 50)
    
    tests = [
        ("Conexión a base de datos", test_database_connection),
        ("Importación de modelos", test_models_import),
        ("Estructura de modelos", test_models_structure),
        ("Controladores", test_controllers)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Ejecutando: {test_name}")
        if test_func():
            passed += 1
        
    print("\n" + "=" * 50)
    print(f"📊 RESULTADOS: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La configuración es correcta.")
        print("\n📝 PRÓXIMOS PASOS:")
        print("1. Verificar que la base de datos 'optica_bd' existe")
        print("2. Ejecutar las tablas SQL si no existen")
        print("3. Probar la aplicación Flask")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)