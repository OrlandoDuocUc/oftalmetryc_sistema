#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diagnóstico mínimo sin importar ningún módulo del proyecto
"""

import psycopg2

def test_minimal():
    """Prueba de conexión mínima sin importar nada del proyecto"""
    print("🔬 DIAGNÓSTICO MÍNIMO - SIN IMPORTS DEL PROYECTO")
    print("=" * 50)
    
    try:
        # Conexión directa sin importar nada del proyecto
        conn = psycopg2.connect(
            host='localhost',
            database='oftalmetryc_db',
            user='postgres',
            password='admin',
            port='5432'
        )
        
        cursor = conn.cursor()
        print("✅ Conexión exitosa!")
        
        # Verificar base de datos
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()[0]
        print(f"🗄️ Base de datos: {db_name}")
        
        # Verificar tablas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('pacientes', 'consultas_medicas', 'examenes_basicos')
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"📋 Tablas médicas encontradas:")
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"   - {table_name}: {count} registros")
            
            # Si es examenes_basicos, mostrar últimos registros
            if table_name == 'examenes_basicos' and count > 0:
                print(f"     👁️ Últimas fichas oftalmológicas:")
                cursor.execute("""
                    SELECT id, paciente_id, TO_CHAR(fecha_examen, 'YYYY-MM-DD'), 
                           agudeza_visual_od, TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI')
                    FROM examenes_basicos 
                    ORDER BY created_at DESC 
                    LIMIT 3;
                """)
                fichas = cursor.fetchall()
                for f in fichas:
                    print(f"       📄 ID:{f[0]} | Paciente:{f[1]} | Fecha:{f[2]} | AV:{f[3] or 'N/A'} | Creado:{f[4]}")
            
            # Si es consultas_medicas, mostrar últimos registros  
            if table_name == 'consultas_medicas' and count > 0:
                print(f"     🩺 Últimas consultas médicas:")
                cursor.execute("""
                    SELECT id, paciente_id, TO_CHAR(fecha_consulta, 'YYYY-MM-DD'), 
                           SUBSTRING(motivo_consulta, 1, 30), TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI')
                    FROM consultas_medicas 
                    ORDER BY created_at DESC 
                    LIMIT 3;
                """)
                consultas = cursor.fetchall()
                for c in consultas:
                    motivo = c[3] + "..." if c[3] and len(c[3]) >= 30 else (c[3] or "Sin motivo")
                    print(f"       📋 ID:{c[0]} | Paciente:{c[1]} | Fecha:{c[2]} | Motivo:{motivo} | Creado:{c[4]}")
        
        cursor.close()
        conn.close()
        
        print(f"\n🎯 CONCLUSIÓN:")
        if not tables:
            print(f"   ❌ No se encontraron tablas médicas en la base de datos")
            print(f"   💡 Posible problema: Base de datos no inicializada")
        else:
            print(f"   ✅ Base de datos funcionando correctamente")
            print(f"   📊 Tablas médicas disponibles: {len(tables)}")
        
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")

if __name__ == "__main__":
    test_minimal()