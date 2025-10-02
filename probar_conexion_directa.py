#!/usr/bin/env python3
"""
PRUEBA DIRECTA CONEXIÓN RENDER
"""
import psycopg2

def probar_conexion_render():
    """Prueba directa a la base de datos de Render"""
    print("🔄 Probando conexión directa a Render...")
    
    # URL directa de Render
    DATABASE_URL = "postgresql://oftalmetryc_user:0WdPbRIzVrbH6xYFCye20Q7ST4e3v7Kn@dpg-d3efatffte5s73chd9r0-a.oregon-postgres.render.com/oftalmetryc_db"
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Verificar pacientes
        cur.execute("SELECT COUNT(*) FROM paciente;")
        pacientes = cur.fetchone()[0]
        
        # Verificar consultas médicas
        cur.execute("SELECT COUNT(*) FROM consulta_medica;")
        consultas = cur.fetchone()[0]
        
        # Verificar últimas consultas
        cur.execute("""
            SELECT cm.id, p.nombre, p.apellido, cm.fecha_consulta, cm.diagnostico
            FROM consulta_medica cm
            JOIN paciente p ON cm.paciente_id = p.id
            ORDER BY cm.fecha_consulta DESC
            LIMIT 5;
        """)
        ultimas_consultas = cur.fetchall()
        
        print("✅ ¡CONEXIÓN EXITOSA A RENDER!")
        print(f"📋 Pacientes registrados: {pacientes}")
        print(f"👁️ Consultas médicas: {consultas}")
        print("\n🔍 Últimas 5 consultas:")
        for consulta in ultimas_consultas:
            print(f"   ID: {consulta[0]} | {consulta[1]} {consulta[2]} | {consulta[3]} | {consulta[4][:50]}...")
        
        cur.close()
        conn.close()
        
        print("\n🎉 ¡LA BASE DE DATOS DE RENDER FUNCIONA PERFECTAMENTE!")
        print("✅ El problema está resuelto para el deploy en GitHub")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    probar_conexion_render()