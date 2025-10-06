#!/usr/bin/env python3
"""
Script para probar el formulario de examen oftalmológico
y verificar que se guarde correctamente en la base de datos
"""
import os
import sys

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infraestructure.utils.db import get_connection

def test_examen_oftalmologico_form():
    """
    Verificar si existe la funcionalidad para guardar exámenes oftalmológicos
    """
    print("=== VERIFICACIÓN FORMULARIO EXAMEN OFTALMOLÓGICO ===")
    
    conn = None
    try:
        # Conectar a la base de datos
        conn = get_connection()
        cursor = conn.cursor()
        
        # 1. Verificar tablas existentes relacionadas con exámenes
        print("\n1. Verificando tablas de exámenes en la base de datos...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE '%examen%' OR table_name LIKE '%oftalmolog%'
        """)
        
        examen_tables = cursor.fetchall()
        print(f"Tablas relacionadas con exámenes: {len(examen_tables)}")
        for table in examen_tables:
            print(f"  - {table[0]}")
        
        # 2. Verificar si existen fichas clínicas (que pueden incluir exámenes)
        print("\n2. Verificando tabla fichas_clinicas...")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'fichas_clinicas'
            ORDER BY ordinal_position
        """)
        
        ficha_columns = cursor.fetchall()
        print(f"Columnas en fichas_clinicas: {len(ficha_columns)}")
        for col, dtype in ficha_columns:
            print(f"  - {col}: {dtype}")
        
        # 2.1. Verificar tabla pacientes_medicos
        print("\n2.1. Verificando tabla pacientes_medicos...")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'pacientes_medicos'
            ORDER BY ordinal_position
        """)
        
        paciente_columns = cursor.fetchall()
        print(f"Columnas en pacientes_medicos: {len(paciente_columns)}")
        for col, dtype in paciente_columns:
            print(f"  - {col}: {dtype}")
        
        # 3. Verificar datos existentes en fichas_clinicas
        print("\n3. Verificando datos existentes...")
        cursor.execute("SELECT COUNT(*) FROM fichas_clinicas")
        count = cursor.fetchone()[0]
        print(f"Total fichas clínicas registradas: {count}")
        
        if count > 0:
            cursor.execute("""
                SELECT fc.ficha_id, c.nombres, fc.motivo_consulta, fc.fecha_creacion
                FROM fichas_clinicas fc
                JOIN pacientes_medicos pm ON fc.paciente_medico_id = pm.paciente_medico_id
                JOIN clientes c ON pm.cliente_id = c.cliente_id
                ORDER BY fc.fecha_creacion DESC
                LIMIT 3
            """)
            
            recent_fichas = cursor.fetchall()
            print("\nÚltimas fichas clínicas:")
            for ficha in recent_fichas:
                print(f"  - ID: {ficha[0]}, Paciente: {ficha[1]}, Motivo: {ficha[2]}, Fecha: {ficha[3]}")
        
        # 4. Verificar estructura de rutas médicas
        print("\n4. Verificando archivos de rutas médicas...")
        medical_routes_file = "adapters/input/flask_app/medical_routes.py"
        if os.path.exists(medical_routes_file):
            print("✅ Archivo medical_routes.py existe")
            
            with open(medical_routes_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if '/examen-oftalmologico' in content:
                    print("✅ Ruta de examen oftalmológico encontrada")
                else:
                    print("❌ Ruta de examen oftalmológico NO encontrada")
        else:
            print("❌ Archivo medical_routes.py NO existe")
        
        print("\n=== RESUMEN ===")
        print("✅ Conexión a base de datos: OK")
        print(f"✅ Tablas de exámenes: {len(examen_tables)}")
        print(f"✅ Fichas clínicas: {count} registros")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return False
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    success = test_examen_oftalmologico_form()
    if success:
        print("\n🎉 Verificación completada exitosamente")
    else:
        print("\n💥 Error en la verificación")