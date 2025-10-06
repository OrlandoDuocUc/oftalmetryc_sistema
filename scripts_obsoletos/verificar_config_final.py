#!/usr/bin/env python3
"""
VERIFICADOR FINAL DE CONFIGURACIÓN - OPTICA_BD
==================================================
Script para verificar que todas las configuraciones apunten a optica_bd
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def verificar_configuracion():
    print("🔍 VERIFICACIÓN FINAL DE CONFIGURACIÓN")
    print("=" * 50)
    
    # Variables de entorno
    print("\n📋 VARIABLES DE ENTORNO:")
    print(f"FLASK_ENV: {os.getenv('FLASK_ENV', 'No configurado')}")
    print(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'No configurado')}")
    print(f"DB_NAME: {os.getenv('DB_NAME', 'No configurado')}")
    print(f"DB_HOST: {os.getenv('DB_HOST', 'No configurado')}")
    print(f"DB_USER: {os.getenv('DB_USER', 'No configurado')}")
    
    # Verificar db.py
    print("\n🔧 VERIFICANDO db.py:")
    try:
        from app.infraestructure.utils.db import DATABASE_URL
        print(f"URL desde db.py: {DATABASE_URL}")
        
        if 'optica_bd' in DATABASE_URL:
            print("✅ db.py apunta a optica_bd")
        else:
            print("❌ db.py NO apunta a optica_bd")
            
    except Exception as e:
        print(f"❌ Error verificando db.py: {e}")
    
    # Verificar settings.py
    print("\n⚙️ VERIFICANDO settings.py:")
    try:
        from config.settings import BaseConfig
        uri = BaseConfig.SQLALCHEMY_DATABASE_URI
        print(f"URI desde settings.py: {uri}")
        
        if 'optica_bd' in uri:
            print("✅ settings.py apunta a optica_bd")
        else:
            print("❌ settings.py NO apunta a optica_bd")
            
    except Exception as e:
        print(f"❌ Error verificando settings.py: {e}")
    
    # Verificación de conexión
    print("\n🔗 PROBANDO CONEXIÓN:")
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'optica_bd'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '12345')
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()[0]
        print(f"✅ Conectado a base de datos: {db_name}")
        
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
        table_count = cursor.fetchone()[0]
        print(f"📊 Tablas encontradas: {table_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    verificar_configuracion()