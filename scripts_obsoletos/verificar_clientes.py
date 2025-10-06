#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICAR ESTRUCTURA TABLA CLIENTES
=================================
"""

import psycopg2

def verificar_clientes():
    """Verificar estructura tabla clientes"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='optica_bd',
            user='postgres',
            password='12345',
            port=5432
        )
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'clientes' 
            ORDER BY ordinal_position;
        """)
        
        columnas = cursor.fetchall()
        print("📋 ESTRUCTURA TABLA CLIENTES:")
        print("-" * 40)
        for col in columnas:
            nombre, tipo, longitud, nullable = col
            nullable_str = "NULL" if nullable == 'YES' else "NOT NULL"
            longitud_str = f"({longitud})" if longitud else ""
            print(f"   {nombre}: {tipo}{longitud_str} {nullable_str}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    verificar_clientes()