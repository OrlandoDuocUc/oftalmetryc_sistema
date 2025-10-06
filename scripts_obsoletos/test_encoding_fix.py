#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRUEBA RÁPIDA DE CONEXIÓN CON ENCODING CORRECTO
===============================================
"""

import os
import sys
from dotenv import load_dotenv

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    import locale
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

# Cargar variables de entorno
load_dotenv()

def test_connection():
    """Probar conexión con configuraciones de encoding"""
    print("🔧 PROBANDO CONEXIÓN CON ENCODING CORRECTO")
    print("=" * 50)
    
    try:
        import psycopg2
        
        # Configuración explícita
        conn_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'optica_bd'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '12345'),
            'port': os.getenv('DB_PORT', '5432'),
            'client_encoding': 'utf8'
        }
        
        print(f"📋 Parámetros de conexión:")
        for key, value in conn_params.items():
            if key == 'password':
                print(f"  {key}: ***")
            else:
                print(f"  {key}: {value}")
        
        # Conectar
        print("\n🔗 Conectando...")
        conn = psycopg2.connect(**conn_params)
        
        # Configurar encoding en la sesión
        conn.set_client_encoding('UTF8')
        
        cursor = conn.cursor()
        
        # Verificar encoding
        cursor.execute("SHOW client_encoding;")
        encoding = cursor.fetchone()[0]
        print(f"✅ Encoding cliente: {encoding}")
        
        cursor.execute("SHOW server_encoding;")
        server_encoding = cursor.fetchone()[0]
        print(f"✅ Encoding servidor: {server_encoding}")
        
        # Verificar base de datos
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()[0]
        print(f"✅ Base de datos: {db_name}")
        
        # Verificar tablas
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        table_count = cursor.fetchone()[0]
        print(f"📊 Tablas encontradas: {table_count}")
        
        # Verificar usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios;")
        user_count = cursor.fetchone()[0]
        print(f"👥 Usuarios registrados: {user_count}")
        
        conn.close()
        print("\n✅ CONEXIÓN EXITOSA - SIN PROBLEMAS DE ENCODING")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR DE CONEXIÓN: {e}")
        return False

if __name__ == "__main__":
    test_connection()