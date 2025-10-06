#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para inicializar y verificar la base de datos con encoding correcto
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def setup_encoding():
    """Configurar variables de entorno para UTF-8"""
    os.environ['PGCLIENTENCODING'] = 'UTF8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    print("✅ Variables de entorno configuradas para UTF-8")

def create_database_if_not_exists():
    """Crear la base de datos si no existe"""
    try:
        # Conectar a postgres para crear la base de datos
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password='admin',
            client_encoding='utf8'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='oftalmetryc_db'")
        exists = cursor.fetchone()
        
        if not exists:
            print("📝 Creando base de datos oftalmetryc_db...")
            cursor.execute("CREATE DATABASE oftalmetryc_db WITH ENCODING 'UTF8'")
            print("✅ Base de datos creada exitosamente")
        else:
            print("✅ Base de datos oftalmetryc_db ya existe")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al crear base de datos: {str(e)}")
        return False

def verify_database_connection():
    """Verificar conexión a la base de datos con encoding correcto"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='oftalmetryc_db',
            user='postgres',
            password='admin',
            client_encoding='utf8'
        )
        
        cursor = conn.cursor()
        
        # Verificar encoding
        cursor.execute("SHOW client_encoding;")
        client_encoding = cursor.fetchone()[0]
        
        cursor.execute("SHOW server_encoding;")
        server_encoding = cursor.fetchone()[0]
        
        print(f"✅ Conexión exitosa a oftalmetryc_db")
        print(f"📊 Client encoding: {client_encoding}")
        print(f"📊 Server encoding: {server_encoding}")
        
        # Verificar tablas existentes
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print(f"📋 Tablas encontradas ({len(tables)}):")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
            count = cursor.fetchone()[0]
            print(f"   - {table[0]}: {count} registros")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def initialize_medical_tables():
    """Inicializar tablas médicas si no existen"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='oftalmetryc_db',
            user='postgres',
            password='admin',
            client_encoding='utf8'
        )
        
        cursor = conn.cursor()
        
        # Verificar si existen las tablas médicas principales
        medical_tables = ['pacientes', 'consultas_medicas', 'examenes_basicos']
        missing_tables = []
        
        for table in medical_tables:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, (table,))
            
            if not cursor.fetchone()[0]:
                missing_tables.append(table)
        
        if missing_tables:
            print(f"📝 Falta crear tablas: {', '.join(missing_tables)}")
            print("💡 Ejecutando create_tables.py para crear las tablas...")
            
            # Intentar ejecutar el script de creación de tablas
            import subprocess
            result = subprocess.run([sys.executable, 'create_tables.py'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Tablas médicas creadas exitosamente")
            else:
                print(f"❌ Error al crear tablas: {result.stderr}")
        else:
            print("✅ Todas las tablas médicas existen")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al inicializar tablas: {str(e)}")
        return False

def main():
    """Función principal de inicialización"""
    print("🔧 INICIALIZANDO SISTEMA DE BASE DE DATOS")
    print("=" * 50)
    
    # Paso 1: Configurar encoding
    setup_encoding()
    
    # Paso 2: Crear base de datos si no existe
    if not create_database_if_not_exists():
        print("❌ No se pudo crear/verificar la base de datos")
        return False
    
    # Paso 3: Verificar conexión
    if not verify_database_connection():
        print("❌ No se pudo conectar a la base de datos")
        return False
    
    # Paso 4: Inicializar tablas médicas
    if not initialize_medical_tables():
        print("❌ No se pudieron inicializar las tablas médicas")
        return False
    
    print("\n🎉 INICIALIZACIÓN COMPLETADA EXITOSAMENTE")
    print("📋 Base de datos lista para usar")
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n💡 Ahora puedes probar la aplicación Flask")
        print("🚀 Ejecuta: python boot.py")
    else:
        print("\n❌ Revisa los errores y ejecuta nuevamente")
        sys.exit(1)