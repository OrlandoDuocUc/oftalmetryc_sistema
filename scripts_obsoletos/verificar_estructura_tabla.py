#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICAR ESTRUCTURA DE TABLA examenes_basicos
"""

import psycopg2

DATABASE_URL = "postgresql://oftalmetryc_user:0WdPbRIzVrbH6xYFCye20Q7ST4e3v7Kn@dpg-d3efatffte5s73chd9r0-a.oregon-postgres.render.com:5432/oftalmetryc_db"

def verificar_estructura():
    """Verificar la estructura exacta de examenes_basicos"""
    print("🔍 VERIFICANDO ESTRUCTURA DE TABLA examenes_basicos")
    print("=" * 55)
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Obtener todas las columnas de examenes_basicos
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'examenes_basicos' 
            ORDER BY ordinal_position
        """)
        
        columnas = cursor.fetchall()
        
        print(f"📊 Total de columnas: {len(columnas)}")
        print("\n📋 ESTRUCTURA COMPLETA:")
        
        for i, (nombre, tipo, nullable) in enumerate(columnas, 1):
            print(f"  {i:3d}. {nombre:<30} ({tipo})")
        
        # Buscar columnas relacionadas con paciente
        print("\n🔍 COLUMNAS RELACIONADAS CON PACIENTE:")
        for nombre, tipo, nullable in columnas:
            if 'paciente' in nombre.lower():
                print(f"  ✅ {nombre} ({tipo})")
        
        # Buscar columnas de ID
        print("\n🆔 COLUMNAS DE ID:")
        for nombre, tipo, nullable in columnas:
            if 'id' in nombre.lower():
                print(f"  ✅ {nombre} ({tipo})")
                
    except Exception as e:
        print(f"❌ ERROR: {e}")
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    verificar_estructura()