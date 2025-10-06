#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICAR ESTRUCTURA TABLAS VENTAS
=================================
"""

import psycopg2

def verificar_ventas():
    """Verificar estructura tablas ventas"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='optica_bd',
            user='postgres',
            password='12345',
            port=5432
        )
        cursor = conn.cursor()
        
        # TABLA VENTAS
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'ventas' 
            ORDER BY ordinal_position;
        """)
        
        columnas_ventas = cursor.fetchall()
        print("📋 ESTRUCTURA TABLA VENTAS:")
        print("-" * 40)
        for col in columnas_ventas:
            nombre, tipo, longitud, nullable = col
            nullable_str = "NULL" if nullable == 'YES' else "NOT NULL"
            longitud_str = f"({longitud})" if longitud else ""
            print(f"   {nombre}: {tipo}{longitud_str} {nullable_str}")
        
        # TABLA DETALLE_VENTAS
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'detalle_ventas' 
            ORDER BY ordinal_position;
        """)
        
        columnas_detalle = cursor.fetchall()
        print("\n📋 ESTRUCTURA TABLA DETALLE_VENTAS:")
        print("-" * 40)
        for col in columnas_detalle:
            nombre, tipo, longitud, nullable = col
            nullable_str = "NULL" if nullable == 'YES' else "NOT NULL"
            longitud_str = f"({longitud})" if longitud else ""
            print(f"   {nombre}: {tipo}{longitud_str} {nullable_str}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    verificar_ventas()