#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNÓSTICO AVANZADO DE POSTGRESQL
=================================
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_postgresql_config():
    """Probar diferentes configuraciones de PostgreSQL"""
    print("🔍 DIAGNÓSTICO POSTGRESQL AVANZADO")
    print("=" * 50)
    
    configurations = [
        {
            'name': 'Configuración 1: URL Simple',
            'params': {
                'dsn': 'postgresql://postgres:12345@localhost:5432/optica_bd'
            }
        },
        {
            'name': 'Configuración 2: URL con encoding',
            'params': {
                'dsn': 'postgresql://postgres:12345@localhost:5432/optica_bd?client_encoding=utf8'
            }
        },
        {
            'name': 'Configuración 3: Parámetros individuales',
            'params': {
                'host': 'localhost',
                'database': 'optica_bd', 
                'user': 'postgres',
                'password': '12345',
                'port': 5432
            }
        },
        {
            'name': 'Configuración 4: Con encoding explícito',
            'params': {
                'host': 'localhost',
                'database': 'optica_bd',
                'user': 'postgres', 
                'password': '12345',
                'port': 5432,
                'options': '-c client_encoding=utf8'
            }
        }
    ]
    
    for i, config in enumerate(configurations, 1):
        print(f"\n🧪 PROBANDO {config['name']}:")
        print("-" * 40)
        
        try:
            import psycopg2
            
            if 'dsn' in config['params']:
                conn = psycopg2.connect(config['params']['dsn'])
            else:
                conn = psycopg2.connect(**config['params'])
            
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ PostgreSQL version: {version[:50]}...")
            
            cursor.execute("SELECT current_database();")
            db = cursor.fetchone()[0]
            print(f"✅ Database: {db}")
            
            conn.close()
            print(f"✅ CONFIGURACIÓN {i} FUNCIONÓ!")
            return config
            
        except Exception as e:
            print(f"❌ CONFIGURACIÓN {i} FALLÓ: {str(e)[:100]}")
            continue
    
    print("\n❌ NINGUNA CONFIGURACIÓN FUNCIONÓ")
    return None

if __name__ == "__main__":
    working_config = test_postgresql_config()
    
    if working_config:
        print(f"\n🎉 CONFIGURACIÓN EXITOSA: {working_config['name']}")
        print("📋 Usar esta configuración en la aplicación")
    else:
        print("\n🚨 PROBLEMA GRAVE CON POSTGRESQL")
        print("💡 POSIBLES SOLUCIONES:")
        print("1. Verificar que PostgreSQL esté corriendo")
        print("2. Verificar credenciales (usuario: postgres, password: 12345)")
        print("3. Verificar que la base de datos 'optica_bd' exista")
        print("4. Verificar configuración de encoding en postgresql.conf")