#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diagnóstico con manejo de codificación específica para Windows
"""

import psycopg2
import os
from datetime import datetime

def test_with_windows_encoding():
    """Prueba de conexión con manejo específico de codificación Windows"""
    print("🪟 DIAGNÓSTICO CON CODIFICACIÓN WINDOWS")
    print("=" * 50)
    
    # Configurar variables de entorno para forzar UTF-8
    os.environ['PGCLIENTENCODING'] = 'UTF8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    try:
        # Conexión con configuración específica para Windows
        conn = psycopg2.connect(
            host='localhost',
            database='oftalmetryc_db',
            user='postgres',
            password='admin',
            port='5432',
            client_encoding='utf8'
        )
        
        cursor = conn.cursor()
        print("✅ Conexión exitosa con UTF-8!")
        
        # Verificar base de datos
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()[0]
        print(f"🗄️ Base de datos: {db_name}")
        
        # Verificar encoding de la base de datos
        cursor.execute("SHOW server_encoding;")
        server_encoding = cursor.fetchone()[0]
        print(f"🌐 Server encoding: {server_encoding}")
        
        cursor.execute("SHOW client_encoding;")
        client_encoding = cursor.fetchone()[0]
        print(f"💻 Client encoding: {client_encoding}")
        
        # Verificar tablas médicas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('pacientes', 'consultas_medicas', 'examenes_basicos')
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"\n📋 Tablas médicas encontradas:")
        
        total_fichas = 0
        total_consultas = 0
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"   - {table_name}: {count} registros")
            
            # Si es examenes_basicos (fichas oftalmológicas)
            if table_name == 'examenes_basicos':
                total_fichas = count
                if count > 0:
                    print(f"     👁️ Últimas 3 fichas oftalmológicas:")
                    cursor.execute("""
                        SELECT e.id, e.paciente_id, 
                               TO_CHAR(e.fecha_examen, 'DD/MM/YYYY') as fecha,
                               e.agudeza_visual_od, 
                               SUBSTRING(e.diagnostico_principal, 1, 40),
                               TO_CHAR(e.created_at, 'DD/MM/YYYY HH24:MI') as creado
                        FROM examenes_basicos e
                        ORDER BY e.created_at DESC 
                        LIMIT 3;
                    """)
                    fichas = cursor.fetchall()
                    for f in fichas:
                        diag = f[4] + "..." if f[4] and len(f[4]) >= 40 else (f[4] or "Sin diagnóstico")
                        print(f"       📄 ID:{f[0]} | Paciente:{f[1]} | {f[2]} | AV:{f[3] or 'N/A'}")
                        print(f"          Diagnóstico: {diag}")
                        print(f"          Creado: {f[5]}")
                        print()
            
            # Si es consultas_medicas
            if table_name == 'consultas_medicas':
                total_consultas = count
                if count > 0:
                    print(f"     🩺 Últimas 3 consultas médicas:")
                    cursor.execute("""
                        SELECT c.id, c.paciente_id,
                               TO_CHAR(c.fecha_consulta, 'DD/MM/YYYY') as fecha,
                               SUBSTRING(c.motivo_consulta, 1, 30),
                               SUBSTRING(c.diagnostico, 1, 30),
                               TO_CHAR(c.created_at, 'DD/MM/YYYY HH24:MI') as creado
                        FROM consultas_medicas c
                        ORDER BY c.created_at DESC 
                        LIMIT 3;
                    """)
                    consultas = cursor.fetchall()
                    for c in consultas:
                        motivo = c[3] + "..." if c[3] and len(c[3]) >= 30 else (c[3] or "Sin motivo")
                        diag = c[4] + "..." if c[4] and len(c[4]) >= 30 else (c[4] or "Sin diagnóstico")
                        print(f"       📋 ID:{c[0]} | Paciente:{c[1]} | {c[2]}")
                        print(f"          Motivo: {motivo}")
                        print(f"          Diagnóstico: {diag}")
                        print(f"          Creado: {c[5]}")
                        print()
        
        # Análisis final
        print(f"\n🎯 ANÁLISIS DEL PROBLEMA:")
        
        if total_fichas == 0 and total_consultas == 0:
            print(f"   ❌ PROBLEMA IDENTIFICADO: No hay fichas clínicas en ninguna tabla")
            print(f"   💡 POSIBLES CAUSAS:")
            print(f"      - Las fichas no se están guardando correctamente")
            print(f"      - Error en el proceso de creación de fichas")
            print(f"      - Las fichas se están guardando en otra base de datos")
            
        elif total_fichas > 0:
            print(f"   ✅ Las fichas oftalmológicas SÍ están en la base de datos")
            print(f"   📊 Total de fichas encontradas: {total_fichas}")
            print(f"   🔍 El problema puede estar en:")
            print(f"      - La interfaz de historial no está mostrando los datos")
            print(f"      - Error en las consultas del frontend")
            print(f"      - Problema en el controlador o servicio de consultas")
            
        elif total_consultas > 0:
            print(f"   ✅ Las consultas médicas SÍ están en la base de datos")
            print(f"   📊 Total de consultas encontradas: {total_consultas}")
            print(f"   ❓ Verificar si las fichas oftalmológicas usan otra tabla")
            
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_with_windows_encoding()