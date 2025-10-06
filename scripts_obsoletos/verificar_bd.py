#!/usr/bin/env python3
"""
Script simple para verificar estado de la base de datos
"""
import os
import psycopg2

def verificar_bd():
    """Verificar si la BD tiene las tablas"""
    try:
        database_url = "postgresql://oftalmetryc_user:0WdPbRIzVrbH6xYFCye20Q7ST4e3v7Kn@dpg-d3efatffte5s73chd9r0-a.oregon-postgres.render.com/oftalmetryc_db"
        
        print("🔄 Conectando a la base de datos...")
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        # Verificar tablas
        cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
        tables = cur.fetchall()
        
        if tables:
            print(f"✅ BD CONECTADA - {len(tables)} tablas encontradas:")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("❌ BD vacía - no hay tablas")
            
        # Verificar usuarios
        if any('usuario' in str(table) for table in tables):
            cur.execute("SELECT username, nombre FROM usuario;")
            users = cur.fetchall()
            print(f"👥 Usuarios en la BD: {len(users)}")
            for user in users:
                print(f"  - {user[0]} ({user[1]})")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error conectando a BD: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Verificando estado de la base de datos...")
    verificar_bd()