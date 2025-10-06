#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar qué tablas existen en la base de datos
"""

import psycopg2
from config.settings import BaseConfig

def check_tables():
    """Verifica qué tablas existen en la base de datos"""
    try:
        # Conectar a PostgreSQL
        config = BaseConfig()
        conn = psycopg2.connect(config.DATABASE_URL)
        cursor = conn.cursor()
        
        print("🔍 VERIFICANDO TABLAS EN LA BASE DE DATOS")
        print("=" * 50)
        
        # Obtener todas las tablas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"📋 Total de tablas encontradas: {len(tables)}")
        print("\n📊 TABLAS EXISTENTES:")
        for table in tables:
            print(f"   ✅ {table[0]}")
        
        # Verificar específicamente la tabla pacientes_medicos
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'pacientes_medicos'
            );
        """)
        
        existe_pacientes_medicos = cursor.fetchone()[0]
        
        print(f"\n🔍 TABLA 'pacientes_medicos': {'✅ EXISTE' if existe_pacientes_medicos else '❌ NO EXISTE'}")
        
        if existe_pacientes_medicos:
            # Si existe, verificar su estructura
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'pacientes_medicos' 
                ORDER BY ordinal_position;
            """)
            
            columns = cursor.fetchall()
            print(f"\n📋 ESTRUCTURA DE 'pacientes_medicos' ({len(columns)} columnas):")
            for col in columns:
                print(f"   - {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    check_tables()