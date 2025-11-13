#!/usr/bin/env python3
"""
Script simple para probar conexión a Render DB usando psycopg2
"""
import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_psycopg2_connection():
    """Probar conexión usando psycopg2 directamente"""
    try:
        # Datos de conexión
        database_url = os.getenv('DATABASE_URL')
        print(f"🔗 Conectando a: {database_url[:60]}...")
        
        # Conectar usando psycopg2
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("✅ CONEXIÓN EXITOSA CON PSYCOPG2!")
        
        # Probar consulta
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"📋 PostgreSQL: {version}")
        
        # Verificar tablas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"\n📊 TABLAS ENCONTRADAS ({len(tables)}):")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Verificar usuarios si existe tabla users
        try:
            cursor.execute("SELECT COUNT(*) FROM users;")
            user_count = cursor.fetchone()[0]
            print(f"\n👥 USUARIOS EN BD: {user_count}")
            
            if user_count > 0:
                cursor.execute("SELECT username, email FROM users LIMIT 5;")
                users = cursor.fetchall()
                print("   Usuarios encontrados:")
                for user in users:
                    print(f"   - {user[0]} ({user[1]})")
                    
        except Exception as e:
            print(f"ℹ️  Info sobre usuarios: {str(e)}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 PROBANDO CONEXIÓN A RENDER (psycopg2)")
    print("=" * 50)
    
    success = test_psycopg2_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ CONEXIÓN EXITOSA - Base de datos accesible")
    else:
        print("❌ CONEXIÓN FALLIDA - Revisar credenciales")