#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diagnóstico integral del sistema de fichas clínicas
Verifica ambas tablas: consultas_medicas y examenes_basicos
"""

import sys
import os
import psycopg2
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_database_url():
    """Obtiene la URL de la base de datos desde las variables de entorno o config"""
    try:
        from config.settings import DATABASE_URL
        return DATABASE_URL
    except:
        # Configuración por defecto para desarrollo local
        return "postgresql://postgres:admin@localhost:5432/oftalmetryc_db"

def test_connection_and_encoding():
    """Prueba la conexión a la base de datos con diferentes configuraciones de encoding"""
    db_url = get_database_url()
    print(f"🔍 Probando conexión a: {db_url.replace('admin', '****')}")
    
    encodings_to_try = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings_to_try:
        try:
            print(f"\n📊 Probando encoding: {encoding}")
            
            # Configurar la conexión con el encoding específico
            conn = psycopg2.connect(
                db_url,
                client_encoding=encoding
            )
            conn.set_client_encoding(encoding)
            
            cursor = conn.cursor()
            
            # Probar una consulta simple
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Conexión exitosa con {encoding}: {version[0][:50]}...")
            
            cursor.close()
            conn.close()
            return encoding
            
        except Exception as e:
            print(f"❌ Error con {encoding}: {str(e)[:100]}...")
    
    return None

def verify_tables_structure():
    """Verifica la estructura de las tablas relacionadas con fichas clínicas"""
    working_encoding = test_connection_and_encoding()
    if not working_encoding:
        print("❌ No se pudo establecer conexión con ningún encoding")
        return
    
    db_url = get_database_url()
    
    try:
        conn = psycopg2.connect(db_url, client_encoding=working_encoding)
        cursor = conn.cursor()
        
        print(f"\n🏥 === DIAGNÓSTICO INTEGRAL DEL SISTEMA MÉDICO ===")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Encoding usado: {working_encoding}")
        
        # 1. Verificar existencia de tablas
        tables_to_check = ['pacientes', 'consultas_medicas', 'examenes_basicos']
        print(f"\n📋 1. VERIFICACIÓN DE TABLAS:")
        
        for table in tables_to_check:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, (table,))
            exists = cursor.fetchone()[0]
            status = "✅ Existe" if exists else "❌ No existe"
            print(f"   {table}: {status}")
        
        # 2. Conteo de registros en cada tabla
        print(f"\n📊 2. CONTEO DE REGISTROS:")
        
        cursor.execute("SELECT COUNT(*) FROM pacientes;")
        pacientes_count = cursor.fetchone()[0]
        print(f"   👥 Pacientes: {pacientes_count}")
        
        cursor.execute("SELECT COUNT(*) FROM consultas_medicas;")
        consultas_count = cursor.fetchone()[0]
        print(f"   🩺 Consultas médicas: {consultas_count}")
        
        cursor.execute("SELECT COUNT(*) FROM examenes_basicos;")
        examenes_count = cursor.fetchone()[0]
        print(f"   👁️ Exámenes básicos (fichas oftalmológicas): {examenes_count}")
        
        # 3. Últimos registros creados
        print(f"\n🕒 3. ÚLTIMOS REGISTROS CREADOS:")
        
        # Últimos pacientes
        cursor.execute("""
            SELECT id, nombres, apellidos, created_at 
            FROM pacientes 
            ORDER BY created_at DESC 
            LIMIT 3;
        """)
        ultimos_pacientes = cursor.fetchall()
        print(f"   👥 Últimos pacientes:")
        for p in ultimos_pacientes:
            print(f"      ID: {p[0]}, Nombre: {p[1]} {p[2]}, Creado: {p[3]}")
        
        # Últimas consultas médicas
        cursor.execute("""
            SELECT c.id, c.paciente_id, c.fecha_consulta, c.motivo_consulta, c.created_at
            FROM consultas_medicas c
            ORDER BY c.created_at DESC 
            LIMIT 3;
        """)
        ultimas_consultas = cursor.fetchall()
        print(f"   🩺 Últimas consultas médicas:")
        for c in ultimas_consultas:
            motivo = c[3][:50] + "..." if c[3] and len(c[3]) > 50 else c[3]
            print(f"      ID: {c[0]}, Paciente ID: {c[1]}, Fecha: {c[2]}, Motivo: {motivo}")
        
        # Últimos exámenes básicos (fichas oftalmológicas)
        cursor.execute("""
            SELECT e.id, e.paciente_id, e.fecha_examen, e.agudeza_visual_od, e.created_at
            FROM examenes_basicos e
            ORDER BY e.created_at DESC 
            LIMIT 3;
        """)
        ultimos_examenes = cursor.fetchall()
        print(f"   👁️ Últimas fichas oftalmológicas:")
        for e in ultimos_examenes:
            av = e[3] if e[3] else "No registrada"
            print(f"      ID: {e[0]}, Paciente ID: {e[1]}, Fecha: {e[2]}, AV OD: {av}")
        
        # 4. Verificar relaciones entre tablas
        print(f"\n🔗 4. VERIFICACIÓN DE RELACIONES:")
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM consultas_medicas c
            JOIN pacientes p ON c.paciente_id = p.id;
        """)
        consultas_con_pacientes = cursor.fetchone()[0]
        print(f"   🩺 Consultas médicas con pacientes válidos: {consultas_con_pacientes}/{consultas_count}")
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM examenes_basicos e
            JOIN pacientes p ON e.paciente_id = p.id;
        """)
        examenes_con_pacientes = cursor.fetchone()[0]
        print(f"   👁️ Fichas oftalmológicas con pacientes válidos: {examenes_con_pacientes}/{examenes_count}")
        
        # 5. Campos más utilizados en fichas oftalmológicas
        print(f"\n📝 5. CAMPOS MÁS UTILIZADOS EN FICHAS OFTALMOLÓGICAS:")
        
        campos_importantes = [
            'agudeza_visual_od', 'agudeza_visual_oi', 'presion_intraocular_od', 
            'presion_intraocular_oi', 'diagnostico_principal', 'observaciones'
        ]
        
        for campo in campos_importantes:
            cursor.execute(f"""
                SELECT COUNT(*) 
                FROM examenes_basicos 
                WHERE {campo} IS NOT NULL AND {campo} != '';
            """)
            count = cursor.fetchone()[0]
            percentage = (count / examenes_count * 100) if examenes_count > 0 else 0
            print(f"   {campo}: {count}/{examenes_count} ({percentage:.1f}%)")
        
        # 6. Recomendaciones
        print(f"\n💡 6. DIAGNÓSTICO Y RECOMENDACIONES:")
        
        if examenes_count == 0 and consultas_count == 0:
            print(f"   ⚠️  No hay fichas clínicas en ninguna tabla")
            print(f"   📝 Las fichas pueden estar guardándose en otra ubicación")
        elif examenes_count > 0:
            print(f"   ✅ Las fichas oftalmológicas están en la tabla 'examenes_basicos'")
            print(f"   📊 Total de fichas encontradas: {examenes_count}")
        elif consultas_count > 0:
            print(f"   ✅ Las consultas médicas están en la tabla 'consultas_medicas'")
            print(f"   📊 Total de consultas encontradas: {consultas_count}")
        
        if pacientes_count == 0:
            print(f"   ❌ No hay pacientes registrados - esto puede causar problemas")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {str(e)}")

if __name__ == "__main__":
    print("🏥 DIAGNÓSTICO INTEGRAL DEL SISTEMA DE FICHAS CLÍNICAS")
    print("=" * 60)
    verify_tables_structure()