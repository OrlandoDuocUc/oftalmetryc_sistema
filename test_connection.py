#!/usr/bin/env python3
"""
Script para probar la conexión a la base de datos
"""
from app.infraestructure.utils.db import engine
from sqlalchemy import text

def test_connection():
    try:
        print("🔍 Probando conexión a la base de datos...")
        
        # Intentar conectar
        with engine.connect() as connection:
            print("✅ Conexión exitosa!")
            
            # Probar una consulta simple
            result = connection.execute(text("SELECT @@VERSION as version"))
            version = result.fetchone()
            print(f"📊 Versión de SQL Server: {version[0]}")
            
            # Verificar si la base de datos existe
            result = connection.execute(text("SELECT DB_NAME() as current_db"))
            current_db = result.fetchone()
            print(f"🗄️ Base de datos actual: {current_db[0]}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection() 