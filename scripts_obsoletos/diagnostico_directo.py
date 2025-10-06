#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diagnóstico directo a la base de datos sin configuración problemática
"""

import psycopg2
from datetime import datetime

def diagnostico_directo():
    """Conecta directamente a la base de datos sin usar archivos de configuración"""
    
    # Configuraciones de base de datos a probar
    configs = [
        {
            'name': 'Local oftalmetryc_db',
            'url': 'postgresql://postgres:admin@localhost:5432/oftalmetryc_db'
        },
        {
            'name': 'Local optica_db', 
            'url': 'postgresql://postgres:admin@localhost:5432/optica_db'
        },
        {
            'name': 'Local con password',
            'url': 'postgresql://postgres:password@localhost:5432/oftalmetryc_db'
        }
    ]
    
    print("🏥 DIAGNÓSTICO DIRECTO - SISTEMA DE FICHAS CLÍNICAS")
    print("=" * 60)
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    for config in configs:
        print(f"\n🔍 Probando: {config['name']}")
        try:
            # Intentar conexión con UTF-8
            conn = psycopg2.connect(config['url'])
            cursor = conn.cursor()
            
            print(f"✅ Conexión exitosa!")
            
            # Verificar versión de PostgreSQL
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"📊 PostgreSQL: {version.split(',')[0]}")
            
            # Verificar base de datos actual
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"🗄️ Base de datos: {db_name}")
            
            # Listar todas las tablas
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            print(f"📋 Tablas encontradas ({len(tables)}):")
            for table in tables:
                print(f"   - {table[0]}")
            
            # Verificar si existen las tablas clave
            tablas_clave = ['pacientes', 'consultas_medicas', 'examenes_basicos']
            print(f"\n🔍 Verificando tablas clave:")
            
            for tabla in tablas_clave:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = %s
                    );
                """, (tabla,))
                exists = cursor.fetchone()[0]
                
                if exists:
                    cursor.execute(f"SELECT COUNT(*) FROM {tabla};")
                    count = cursor.fetchone()[0]
                    print(f"   ✅ {tabla}: {count} registros")
                else:
                    print(f"   ❌ {tabla}: No existe")
            
            # Si encontramos examenes_basicos, ver últimos registros
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'examenes_basicos'
                );
            """)
            
            if cursor.fetchone()[0]:
                print(f"\n👁️ ÚLTIMAS FICHAS OFTALMOLÓGICAS:")
                cursor.execute("""
                    SELECT id, paciente_id, fecha_examen, agudeza_visual_od, 
                           diagnostico_principal, created_at
                    FROM examenes_basicos 
                    ORDER BY created_at DESC 
                    LIMIT 5;
                """)
                fichas = cursor.fetchall()
                
                if fichas:
                    for ficha in fichas:
                        print(f"   📄 ID: {ficha[0]}, Paciente: {ficha[1]}, Fecha: {ficha[2]}")
                        print(f"      AV OD: {ficha[3] or 'No registrada'}")
                        print(f"      Diagnóstico: {(ficha[4] or 'Sin diagnóstico')[:50]}...")
                        print(f"      Creado: {ficha[5]}")
                        print()
                else:
                    print("   📝 No hay fichas oftalmológicas registradas")
            
            # Si encontramos consultas_medicas, ver últimos registros  
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'consultas_medicas'
                );
            """)
            
            if cursor.fetchone()[0]:
                print(f"\n🩺 ÚLTIMAS CONSULTAS MÉDICAS:")
                cursor.execute("""
                    SELECT id, paciente_id, fecha_consulta, motivo_consulta, 
                           diagnostico, created_at
                    FROM consultas_medicas 
                    ORDER BY created_at DESC 
                    LIMIT 5;
                """)
                consultas = cursor.fetchall()
                
                if consultas:
                    for consulta in consultas:
                        print(f"   📋 ID: {consulta[0]}, Paciente: {consulta[1]}, Fecha: {consulta[2]}")
                        print(f"      Motivo: {(consulta[3] or 'Sin motivo')[:50]}...")
                        print(f"      Diagnóstico: {(consulta[4] or 'Sin diagnóstico')[:50]}...")
                        print(f"      Creado: {consulta[5]}")
                        print()
                else:
                    print("   📝 No hay consultas médicas registradas")
            
            cursor.close()
            conn.close()
            
            print(f"\n🎯 DIAGNÓSTICO PARA: {config['name']}")
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)[:100]}...")
    
    print(f"\n❌ No se pudo conectar a ninguna base de datos")
    return False

if __name__ == "__main__":
    diagnostico_directo()