#!/usr/bin/env python3
"""
Script para probar la conexión a la nueva base de datos en Render
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Cargar variables de entorno
load_dotenv()

def test_database_connection():
    """Probar conexión a la base de datos"""
    try:
        # Obtener DATABASE_URL
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ ERROR: No se encontró DATABASE_URL en las variables de entorno")
            return False
        
        print(f"🔗 Intentando conectar a: {database_url[:60]}...")
        
        # Crear engine
        engine = create_engine(database_url, 
                             pool_pre_ping=True,
                             pool_recycle=300)
        
        # Probar conexión
        with engine.connect() as connection:
            # Ejecutar consulta simple
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ CONEXIÓN EXITOSA!")
            print(f"📋 PostgreSQL Version: {version}")
            
            # Verificar tablas existentes
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """))
            
            tables = result.fetchall()
            print(f"\n📊 TABLAS ENCONTRADAS ({len(tables)}):")
            for table in tables:
                print(f"   - {table[0]}")
            
            # Verificar datos del usuario admin
            try:
                result = connection.execute(text("SELECT COUNT(*) FROM users;"))
                user_count = result.fetchone()[0]
                print(f"\n👥 USUARIOS EN BD: {user_count}")
                
                if user_count > 0:
                    result = connection.execute(text("SELECT username, email FROM users LIMIT 5;"))
                    users = result.fetchall()
                    print("   Usuarios encontrados:")
                    for user in users:
                        print(f"   - {user[0]} ({user[1]})")
                        
            except Exception as e:
                print(f"ℹ️  No se pudo verificar usuarios: {str(e)}")
            
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ ERROR DE CONEXIÓN: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ ERROR GENERAL: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 PROBANDO CONEXIÓN A RENDER DATABASE")
    print("=" * 50)
    
    success = test_database_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ PRUEBA EXITOSA - La aplicación puede conectarse a Render")
    else:
        print("❌ PRUEBA FALLIDA - Revisar configuración")