#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test completo de la Ficha Clínica Digital
Verifica que todos los componentes estén funcionando
"""

import sys
import os
import traceback
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """Test conexión a base de datos"""
    try:
        from app.infraestructure.utils.db import get_db_connection
        conn = get_db_connection()
        if conn:
            conn.close()
            print("✅ Conexión a base de datos: OK")
            return True
        else:
            print("❌ Conexión a base de datos: FALLO")
            return False
    except Exception as e:
        print(f"❌ Error conexión BD: {e}")
        return False

def test_models():
    """Test modelos de datos"""
    try:
        from app.domain.models.paciente import Paciente
        from app.domain.models.examen_basico import ExamenBasico
        print("✅ Modelos importados: OK")
        
        # Test modelo Paciente
        paciente_test = Paciente()
        print("✅ Modelo Paciente instanciado: OK")
        
        # Test modelo ExamenBasico
        examen_test = ExamenBasico()
        print("✅ Modelo ExamenBasico instanciado: OK")
        
        return True
    except Exception as e:
        print(f"❌ Error modelos: {e}")
        traceback.print_exc()
        return False

def test_flask_routes():
    """Test rutas de Flask"""
    try:
        from adapters.input.flask_app.ficha_clinica_routes import ficha_clinica_bp
        print("✅ Rutas Flask importadas: OK")
        print(f"✅ Blueprint registrado: {ficha_clinica_bp.name}")
        return True
    except Exception as e:
        print(f"❌ Error rutas Flask: {e}")
        traceback.print_exc()
        return False

def test_templates():
    """Test templates"""
    try:
        template_path = "adapters/input/flask_app/templates/ficha_clinica_digital.html"
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) > 1000:  # Template tiene contenido substancial
                    print("✅ Template ficha clínica: OK")
                    return True
                else:
                    print("❌ Template muy pequeño")
                    return False
        else:
            print(f"❌ Template no encontrado: {template_path}")
            return False
    except Exception as e:
        print(f"❌ Error templates: {e}")
        return False

def test_database_fields():
    """Test campos de base de datos"""
    try:
        from app.infraestructure.utils.db import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Test tabla pacientes
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'pacientes'
            ORDER BY ordinal_position
        """)
        pacientes_fields = [row[0] for row in cursor.fetchall()]
        print(f"✅ Campos en pacientes: {len(pacientes_fields)}")
        
        # Verificar campos específicos
        campos_esperados = ['ci', 'nombres', 'apellidos', 'genero', 'hobby']
        campos_encontrados = [campo for campo in campos_esperados if campo in pacientes_fields]
        print(f"✅ Campos Ecuador encontrados: {campos_encontrados}")
        
        # Test tabla examenes_basicos
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'examenes_basicos'
            ORDER BY ordinal_position
        """)
        examenes_fields = [row[0] for row in cursor.fetchall()]
        print(f"✅ Campos en examenes_basicos: {len(examenes_fields)}")
        
        # Verificar campos oftalmológicos específicos
        campos_oftalmo = ['av_distancia_od', 'av_distancia_oi', 'refraccion_od_esfera', 'pio_od']
        campos_oftalmo_encontrados = [campo for campo in campos_oftalmo if campo in examenes_fields]
        print(f"✅ Campos oftalmológicos encontrados: {campos_oftalmo_encontrados}")
        
        conn.close()
        return len(pacientes_fields) >= 20 and len(examenes_fields) >= 100
    except Exception as e:
        print(f"❌ Error verificando campos BD: {e}")
        return False

def test_app_creation():
    """Test creación de app Flask"""
    try:
        from adapters.input.flask_app import create_app
        app = create_app('development')
        print("✅ App Flask creada: OK")
        print(f"✅ Blueprints registrados: {len(app.blueprints)}")
        return True
    except Exception as e:
        print(f"❌ Error creando app: {e}")
        traceback.print_exc()
        return False

def main():
    """Ejecutar todos los tests"""
    print("="*60)
    print("🔬 TEST COMPLETO - FICHA CLÍNICA DIGITAL")
    print("="*60)
    print(f"⏰ Hora de test: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Models", test_models),
        ("Flask Routes", test_flask_routes),
        ("Templates", test_templates),
        ("Database Fields", test_database_fields),
        ("App Creation", test_app_creation),
    ]
    
    results = []
    
    for test_name, test_function in tests:
        print(f"🧪 Ejecutando: {test_name}")
        try:
            result = test_function()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error crítico en {test_name}: {e}")
            results.append((test_name, False))
        print()
    
    # Resumen final
    print("="*60)
    print("📊 RESUMEN DE RESULTADOS")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print()
    print(f"🎯 TOTAL: {passed}/{total} tests pasados")
    
    if passed == total:
        print("🎉 ¡IMPLEMENTACIÓN COMPLETA Y FUNCIONAL!")
        print("✅ El sistema de Ficha Clínica Digital está listo para usar")
    else:
        print(f"⚠️  Quedan {total - passed} issues por resolver")
    
    print("="*60)

if __name__ == "__main__":
    main()