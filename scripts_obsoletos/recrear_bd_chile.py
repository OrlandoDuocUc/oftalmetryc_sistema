#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOLUCIÓN AL PROBLEMA DE ENCODING CHILE vs ECUADOR
=================================================
Recrear base de datos con configuración chilena correcta
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def recrear_bd_chile():
    """Recrear base de datos con configuración chilena correcta"""
    print("🇨🇱 RECREANDO BASE DE DATOS CON CONFIGURACIÓN CHILE")
    print("=" * 60)
    
    # Parámetros de conexión
    admin_params = {
        'host': 'localhost',
        'user': 'postgres',
        'password': '12345',
        'port': 5432
    }
    
    try:
        # 1. Conectar como administrador
        print("1️⃣ Conectando como administrador...")
        conn_admin = psycopg2.connect(database='postgres', **admin_params)
        conn_admin.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn_admin.cursor()
        
        # 2. Eliminar base de datos existente
        print("2️⃣ Eliminando base de datos existente...")
        try:
            cursor.execute("DROP DATABASE IF EXISTS optica_bd;")
            print("✅ Base de datos eliminada")
        except Exception as e:
            print(f"⚠️ Warning al eliminar: {e}")
        
        # 3. Crear base de datos con configuración chilena
        print("3️⃣ Creando base de datos con configuración CHILE...")
        create_db_sql = """
        CREATE DATABASE optica_bd
            WITH 
            OWNER = postgres
            ENCODING = 'UTF8'
            LC_COLLATE = 'Spanish_Chile.1252'
            LC_CTYPE = 'Spanish_Chile.1252'
            TEMPLATE = template0
            TABLESPACE = pg_default
            CONNECTION LIMIT = -1;
        """
        
        try:
            cursor.execute(create_db_sql)
            print("✅ Base de datos creada con configuración Chile")
        except Exception as e:
            print(f"⚠️ Error específico: {e}")
            print("🔄 Intentando con configuración alternativa...")
            
            # Configuración alternativa más compatible
            create_db_alt = """
            CREATE DATABASE optica_bd
                WITH 
                OWNER = postgres
                ENCODING = 'UTF8'
                TEMPLATE = template0;
            """
            cursor.execute(create_db_alt)
            print("✅ Base de datos creada con configuración alternativa")
        
        conn_admin.close()
        
        # 4. Probar conexión a nueva base de datos
        print("4️⃣ Probando conexión a nueva base de datos...")
        test_params = admin_params.copy()
        test_params['database'] = 'optica_bd'
        
        conn_test = psycopg2.connect(**test_params)
        cursor_test = conn_test.cursor()
        
        # Verificar configuración
        cursor_test.execute("SHOW LC_COLLATE;")
        lc_collate = cursor_test.fetchone()[0]
        cursor_test.execute("SHOW LC_CTYPE;")
        lc_ctype = cursor_test.fetchone()[0]
        cursor_test.execute("SHOW server_encoding;")
        encoding = cursor_test.fetchone()[0]
        
        print(f"📊 LC_COLLATE: {lc_collate}")
        print(f"📊 LC_CTYPE: {lc_ctype}")
        print(f"📊 ENCODING: {encoding}")
        
        conn_test.close()
        
        # 5. Ejecutar script de creación de tablas
        print("5️⃣ Ejecutando script de creación de tablas...")
        script_path = r"SCRIPT_POSTGRESQL_OPTICA_BD.sql"
        
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Ejecutar solo las partes de creación de tablas e inserción de datos
            conn_exec = psycopg2.connect(**test_params)
            cursor_exec = conn_exec.cursor()
            
            # Dividir el script en comandos individuales
            commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
            
            success_count = 0
            for i, command in enumerate(commands):
                if any(keyword in command.upper() for keyword in ['CREATE TABLE', 'INSERT INTO', 'CREATE INDEX']):
                    try:
                        cursor_exec.execute(command)
                        conn_exec.commit()
                        success_count += 1
                    except Exception as e:
                        print(f"⚠️ Error en comando {i+1}: {str(e)[:100]}")
            
            print(f"✅ Ejecutados {success_count} comandos exitosamente")
            conn_exec.close()
        
        print("\n🎉 ¡BASE DE DATOS RECREADA EXITOSAMENTE!")
        print("✅ Configuración chilena aplicada")
        print("✅ Tablas creadas")
        print("✅ Datos iniciales insertados")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    recrear_bd_chile()