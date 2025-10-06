#!/usr/bin/env python3
"""
Script para probar la funcionalidad del historial de consultas de un paciente
"""
import os
import sys

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infraestructure.utils.db import get_connection

def test_historial_consultas():
    """
    Verificar si el historial de consultas funciona correctamente
    """
    print("=== VERIFICACIÓN HISTORIAL DE CONSULTAS ===")
    
    conn = None
    try:
        # Conectar a la base de datos
        conn = get_connection()
        cursor = conn.cursor()
        
        # 1. Verificar pacientes existentes
        print("\n1. Verificando pacientes médicos...")
        cursor.execute("""
            SELECT pm.paciente_medico_id, c.nombres, c.ap_pat, pm.numero_ficha
            FROM pacientes_medicos pm
            JOIN clientes c ON pm.cliente_id = c.cliente_id
            WHERE pm.estado = true
            ORDER BY pm.fecha_registro DESC
            LIMIT 5
        """)
        
        pacientes = cursor.fetchall()
        print(f"Pacientes activos: {len(pacientes)}")
        for paciente in pacientes:
            print(f"  - ID: {paciente[0]}, Nombre: {paciente[1]} {paciente[2]}, Ficha: {paciente[3]}")
        
        if len(pacientes) == 0:
            print("❌ No hay pacientes médicos activos")
            return False
        
        # 2. Verificar consultas para el primer paciente
        primer_paciente_id = pacientes[0][0]
        print(f"\n2. Verificando consultas del paciente ID {primer_paciente_id}...")
        
        cursor.execute("""
            SELECT fc.ficha_id, fc.motivo_consulta, fc.fecha_consulta, fc.estado, u.nombre
            FROM fichas_clinicas fc
            LEFT JOIN usuarios u ON fc.usuario_id = u.usuario_id
            WHERE fc.paciente_medico_id = %s
            ORDER BY fc.fecha_consulta DESC
        """, (primer_paciente_id,))
        
        consultas = cursor.fetchall()
        print(f"Consultas encontradas: {len(consultas)}")
        for consulta in consultas:
            print(f"  - ID: {consulta[0]}, Motivo: {consulta[1]}, Fecha: {consulta[2]}, Estado: {consulta[3]}, Dr: {consulta[4] or 'N/A'}")
        
        # 3. Probar la consulta como la hace la API
        print(f"\n3. Probando consulta completa de API...")
        cursor.execute("""
            SELECT fc.*, pm.numero_ficha, c.nombres, c.ap_pat, u.nombre as doctor_nombre
            FROM fichas_clinicas fc
            LEFT JOIN pacientes_medicos pm ON fc.paciente_medico_id = pm.paciente_medico_id
            LEFT JOIN clientes c ON pm.cliente_id = c.cliente_id
            LEFT JOIN usuarios u ON fc.usuario_id = u.usuario_id
            WHERE fc.paciente_medico_id = %s
            ORDER BY fc.fecha_consulta DESC
        """, (primer_paciente_id,))
        
        consultas_completas = cursor.fetchall()
        print(f"Consultas completas: {len(consultas_completas)}")
        
        # 4. Verificar estructura de tablas
        print(f"\n4. Verificando estructura de fichas_clinicas...")
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'fichas_clinicas'
            ORDER BY ordinal_position
        """)
        
        columnas = cursor.fetchall()
        print(f"Columnas en fichas_clinicas: {[col[0] for col in columnas]}")
        
        print("\n=== RESUMEN ===")
        print(f"✅ Pacientes activos: {len(pacientes)}")
        print(f"✅ Consultas del primer paciente: {len(consultas)}")
        print(f"✅ Consulta API completa: {len(consultas_completas)}")
        
        return len(consultas) > 0
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return False
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    success = test_historial_consultas()
    if success:
        print("\n🎉 El historial debería funcionar correctamente")
    else:
        print("\n💥 Hay problemas con el historial de consultas")