#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISIS DE DISCREPANCIAS CRÍTICAS
=================================
"""

import psycopg2

def analizar_discrepancias():
    """Analizar discrepancias específicas"""
    print("🚨 ANÁLISIS DE DISCREPANCIAS CRÍTICAS")
    print("=" * 50)
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='optica_bd',
            user='postgres',
            password='12345',
            port=5432
        )
        cursor = conn.cursor()
        
        # PROBLEMA 1: TABLA USUARIOS - TIPOS DE DATOS
        print("🔍 PROBLEMA 1: TABLA USUARIOS")
        print("-" * 30)
        
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'usuarios' 
            ORDER BY ordinal_position;
        """)
        
        columnas_usuarios = cursor.fetchall()
        print("ESTRUCTURA REAL:")
        for col in columnas_usuarios:
            nombre, tipo, longitud, nullable = col
            nullable_str = "NULL" if nullable == 'YES' else "NOT NULL"
            longitud_str = f"({longitud})" if longitud else ""
            print(f"   {nombre}: {tipo}{longitud_str} {nullable_str}")
        
        # PROBLEMA 2: FOREIGN KEYS
        print("\n🔍 PROBLEMA 2: FOREIGN KEYS EN USUARIOS")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                tc.constraint_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_name = 'usuarios';
        """)
        
        fks_usuarios = cursor.fetchall()
        if fks_usuarios:
            for fk in fks_usuarios:
                constraint, col, ref_table, ref_col = fk
                print(f"   FK: {col} → {ref_table}.{ref_col}")
        else:
            print("   ⚠️ NO HAY FOREIGN KEYS DEFINIDAS")
        
        # PROBLEMA 3: VERIFICAR TABLA ROLES
        print("\n🔍 PROBLEMA 3: TABLA ROLES")
        print("-" * 25)
        
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'roles' 
            ORDER BY ordinal_position;
        """)
        
        columnas_roles = cursor.fetchall()
        print("ESTRUCTURA REAL:")
        for col in columnas_roles:
            nombre, tipo, nullable = col
            nullable_str = "NULL" if nullable == 'YES' else "NOT NULL"
            print(f"   {nombre}: {tipo} {nullable_str}")
        
        # PROBLEMA 4: VERIFICAR DATOS DE PRUEBA
        print("\n🔍 PROBLEMA 4: DATOS DE PRUEBA")
        print("-" * 30)
        
        cursor.execute("SELECT COUNT(*) FROM usuarios;")
        count_usuarios = cursor.fetchone()[0]
        print(f"   Usuarios registrados: {count_usuarios}")
        
        if count_usuarios > 0:
            cursor.execute("SELECT usuario_id, username, nombre FROM usuarios LIMIT 3;")
            usuarios = cursor.fetchall()
            for usuario in usuarios:
                print(f"   Usuario: ID={usuario[0]}, username='{usuario[1]}', nombre='{usuario[2]}'")
        
        cursor.execute("SELECT COUNT(*) FROM roles;")
        count_roles = cursor.fetchone()[0]
        print(f"   Roles registrados: {count_roles}")
        
        if count_roles > 0:
            cursor.execute("SELECT rol_id, nombre FROM roles LIMIT 5;")
            roles = cursor.fetchall()
            for rol in roles:
                print(f"   Rol: ID={rol[0]}, nombre='{rol[1]}'")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    analizar_discrepancias()