#!/usr/bin/env python3
"""
Script para probar conexión directa a la base de datos
"""
import psycopg2
from sqlalchemy import create_engine, text

def test_direct_connection():
    """Prueba conexión directa con psycopg2"""
    try:
        print("🔍 Probando conexión directa con psycopg2...")
        conn = psycopg2.connect(
            host='localhost',
            database='optica_bd', 
            user='postgres',
            password='12345',
            port=5432
        )
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa!")
        
        # Contar usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios;")
        count_usuarios = cursor.fetchone()[0]
        print(f"📊 Total usuarios en BD: {count_usuarios}")
        
        # Contar productos
        cursor.execute("SELECT COUNT(*) FROM productos;")
        count_productos = cursor.fetchone()[0]
        print(f"📦 Total productos en BD: {count_productos}")
        
        # Mostrar últimos usuarios
        cursor.execute("SELECT usuario_id, username, nombre, estado FROM usuarios ORDER BY usuario_id DESC LIMIT 5;")
        usuarios = cursor.fetchall()
        print(f"\n👥 Últimos 5 usuarios:")
        for u in usuarios:
            print(f"  ID: {u[0]}, Username: {u[1]}, Nombre: {u[2]}, Estado: {u[3]}")
        
        # Mostrar últimos productos
        cursor.execute("SELECT producto_id, nombre, stock, estado FROM productos ORDER BY producto_id DESC LIMIT 5;")
        productos = cursor.fetchall()
        print(f"\n📦 Últimos 5 productos:")
        for p in productos:
            print(f"  ID: {p[0]}, Nombre: {p[1]}, Stock: {p[2]}, Estado: {p[3]}")
            
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error con psycopg2: {e}")
        return False

def test_sqlalchemy_connection():
    """Prueba conexión con SQLAlchemy"""
    try:
        print("\n🔍 Probando conexión con SQLAlchemy...")
        DATABASE_URL = "postgresql://postgres:12345@localhost:5432/optica_bd?client_encoding=utf8"
        engine = create_engine(DATABASE_URL, echo=False)
        
        with engine.connect() as connection:
            print("✅ Conexión SQLAlchemy exitosa!")
            
            # Contar usuarios
            result = connection.execute(text("SELECT COUNT(*) FROM usuarios"))
            count_usuarios = result.scalar()
            print(f"📊 Total usuarios en BD (SQLAlchemy): {count_usuarios}")
            
            # Contar productos
            result = connection.execute(text("SELECT COUNT(*) FROM productos"))
            count_productos = result.scalar()
            print(f"📦 Total productos en BD (SQLAlchemy): {count_productos}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error con SQLAlchemy: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de conexión a base de datos...")
    print("=" * 60)
    
    # Prueba 1: Conexión directa
    direct_ok = test_direct_connection()
    
    # Prueba 2: Conexión SQLAlchemy
    sqlalchemy_ok = test_sqlalchemy_connection()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN:")
    print(f"   Conexión directa (psycopg2): {'✅ OK' if direct_ok else '❌ FALLO'}")
    print(f"   Conexión SQLAlchemy: {'✅ OK' if sqlalchemy_ok else '❌ FALLO'}")
    
    if direct_ok and sqlalchemy_ok:
        print("🎉 Todas las conexiones funcionan correctamente!")
    else:
        print("⚠️  Hay problemas de conexión que deben resolverse.")