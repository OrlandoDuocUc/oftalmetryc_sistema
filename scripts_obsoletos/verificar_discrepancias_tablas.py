#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICAR DISCREPANCIAS DE NOMBRES DE TABLAS
==========================================
"""

import psycopg2

def verificar_discrepancias_tablas():
    """Verificar nombres reales vs esperados"""
    
    print("🔍 VERIFICANDO DISCREPANCIAS DE NOMBRES DE TABLAS")
    print("=" * 50)
    
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(
            host='localhost',
            database='optica_bd',
            user='postgres',
            password='12345',
            port=5432
        )
        cursor = conn.cursor()
        
        # 1. Listar todas las tablas que existen
        print("📋 TABLAS QUE EXISTEN EN LA BD:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        
        tablas_existentes = cursor.fetchall()
        for tabla in tablas_existentes:
            print(f"   ✅ {tabla[0]}")
        
        # 2. Verificar qué tablas busca el código
        print(f"\n🔍 TABLAS QUE BUSCA EL CÓDIGO:")
        tablas_esperadas = ['producto', 'usuario', 'cliente', 'venta', 'detalle_venta']
        
        nombres_reales = [t[0] for t in tablas_existentes]
        
        for tabla_esperada in tablas_esperadas:
            if tabla_esperada in nombres_reales:
                print(f"   ✅ {tabla_esperada} - EXISTE")
            else:
                # Buscar variaciones
                plural = tabla_esperada + 's'
                singular = tabla_esperada[:-1] if tabla_esperada.endswith('s') else tabla_esperada
                
                if plural in nombres_reales:
                    print(f"   ❌ {tabla_esperada} - NO EXISTE, pero SÍ está '{plural}'")
                elif singular in nombres_reales:
                    print(f"   ❌ {tabla_esperada} - NO EXISTE, pero SÍ está '{singular}'")
                else:
                    print(f"   ❌ {tabla_esperada} - NO EXISTE")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    verificar_discrepancias_tablas()