#!/usr/bin/env python3
"""
Script para verificar que la conexión a Render funciona
"""
import os
from app.infraestructure.utils.db import get_connection

def verificar_conexion():
    """Verifica la conexión a la base de datos de Render"""
    try:
        print("🔄 Verificando conexión a Render...")
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM paciente;")
            pacientes = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM consulta_medica;")
            consultas = cur.fetchone()[0]
            
            print(f"✅ Conexión exitosa a Render:")
            print(f"   📋 Pacientes: {pacientes}")
            print(f"   👁️ Consultas médicas: {consultas}")
            
            cur.close()
            conn.close()
            return True
        else:
            print("❌ No se pudo conectar a la base de datos")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    verificar_conexion()
