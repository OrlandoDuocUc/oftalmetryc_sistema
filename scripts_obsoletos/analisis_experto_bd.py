#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISIS EXPERTO DE CORRELACIÓN BD vs APLICACIÓN
===============================================
Verificar estructura real de la base de datos
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def analizar_estructura_bd():
    """Analizar estructura real de la base de datos"""
    print("🔍 ANÁLISIS EXPERTO: ESTRUCTURA REAL DE LA BASE DE DATOS")
    print("=" * 70)
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='optica_bd',
            user='postgres',
            password='12345',
            port=5432
        )
        cursor = conn.cursor()
        
        # 1. VERIFICAR TODAS LAS TABLAS
        print("1️⃣ TABLAS EXISTENTES EN LA BASE DE DATOS:")
        print("-" * 50)
        cursor.execute("""
            SELECT table_name, table_type
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tablas = cursor.fetchall()
        for tabla, tipo in tablas:
            print(f"   📊 {tabla} ({tipo})")
        
        print(f"\n📈 TOTAL TABLAS: {len(tablas)}")
        
        # 2. VERIFICAR ESTRUCTURA DE CADA TABLA CRÍTICA
        tablas_criticas = ['usuarios', 'roles', 'clientes', 'productos', 'ventas', 'detalle_ventas']
        
        for tabla in tablas_criticas:
            print(f"\n2️⃣ ESTRUCTURA DE TABLA: {tabla.upper()}")
            print("-" * 50)
            
            # Verificar si la tabla existe
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                );
            """, (tabla,))
            
            existe = cursor.fetchone()[0]
            
            if existe:
                # Obtener columnas
                cursor.execute("""
                    SELECT 
                        column_name,
                        data_type,
                        character_maximum_length,
                        is_nullable,
                        column_default,
                        is_identity
                    FROM information_schema.columns 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                    ORDER BY ordinal_position;
                """, (tabla,))
                
                columnas = cursor.fetchall()
                for col in columnas:
                    nombre, tipo, longitud, nullable, default, identity = col
                    longitud_str = f"({longitud})" if longitud else ""
                    nullable_str = "NULL" if nullable == 'YES' else "NOT NULL"
                    default_str = f" DEFAULT {default}" if default else ""
                    identity_str = " IDENTITY" if identity == 'YES' else ""
                    
                    print(f"   🔹 {nombre}: {tipo}{longitud_str} {nullable_str}{default_str}{identity_str}")
                
                # Verificar claves primarias
                cursor.execute("""
                    SELECT column_name
                    FROM information_schema.key_column_usage
                    WHERE table_schema = 'public'
                    AND table_name = %s
                    AND constraint_name LIKE '%_pkey';
                """, (tabla,))
                
                pks = cursor.fetchall()
                if pks:
                    pk_cols = [pk[0] for pk in pks]
                    print(f"   🔑 PRIMARY KEY: {', '.join(pk_cols)}")
                
                # Verificar foreign keys
                cursor.execute("""
                    SELECT 
                        kcu.column_name,
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name
                    FROM information_schema.table_constraints AS tc 
                    JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                        AND tc.table_schema = kcu.table_schema
                    JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = tc.constraint_name
                        AND ccu.table_schema = tc.table_schema
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                    AND tc.table_name = %s;
                """, (tabla,))
                
                fks = cursor.fetchall()
                for fk in fks:
                    col, ref_table, ref_col = fk
                    print(f"   🔗 FOREIGN KEY: {col} → {ref_table}.{ref_col}")
                
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {tabla};")
                count = cursor.fetchone()[0]
                print(f"   📊 REGISTROS: {count}")
                
            else:
                print(f"   ❌ TABLA '{tabla}' NO EXISTE")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ ERROR EN ANÁLISIS: {e}")
        return False

if __name__ == "__main__":
    analizar_estructura_bd()