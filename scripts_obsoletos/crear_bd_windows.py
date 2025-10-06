#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOLUCIÓN COMPATIBLE WINDOWS - BASE DE DATOS OPTICA
================================================
Crear base de datos compatible con Windows y Chile
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

def crear_bd_compatible():
    """Crear base de datos compatible con Windows"""
    print("🪟 CREANDO BASE DE DATOS COMPATIBLE WINDOWS")
    print("=" * 50)
    
    admin_params = {
        'host': 'localhost',
        'user': 'postgres',
        'password': '12345',
        'port': 5432
    }
    
    try:
        # Conectar como administrador
        print("1️⃣ Conectando...")
        conn = psycopg2.connect(database='postgres', **admin_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Eliminar BD existente
        print("2️⃣ Eliminando BD existente...")
        cursor.execute("DROP DATABASE IF EXISTS optica_bd;")
        
        # Crear BD con configuración simple
        print("3️⃣ Creando BD compatible...")
        cursor.execute("""
            CREATE DATABASE optica_bd
                WITH 
                OWNER = postgres
                ENCODING = 'UTF8'
                TEMPLATE = template0;
        """)
        
        print("✅ Base de datos creada")
        conn.close()
        
        # Probar conexión
        print("4️⃣ Probando conexión...")
        conn_test = psycopg2.connect(database='optica_bd', **admin_params)
        cursor_test = conn_test.cursor()
        
        # Configurar encoding en la sesión
        cursor_test.execute("SET client_encoding TO 'UTF8';")
        
        cursor_test.execute("SELECT current_database();")
        db_name = cursor_test.fetchone()[0]
        print(f"✅ Conectado a: {db_name}")
        
        # Crear tablas básicas
        print("5️⃣ Creando tablas...")
        
        tables_sql = """
        -- ROLES
        CREATE TABLE roles (
            rol_id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) UNIQUE NOT NULL,
            descripcion TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado BOOLEAN DEFAULT TRUE
        );
        
        -- USUARIOS
        CREATE TABLE usuarios (
            usuario_id SERIAL PRIMARY KEY,
            rol_id INTEGER REFERENCES roles(rol_id),
            username VARCHAR(80) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            nombre VARCHAR(100) NOT NULL,
            ap_pat VARCHAR(100) NOT NULL,
            ap_mat VARCHAR(100),
            email VARCHAR(120) UNIQUE NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado BOOLEAN DEFAULT TRUE
        );
        
        -- CLIENTES
        CREATE TABLE clientes (
            cliente_id SERIAL PRIMARY KEY,
            nombres VARCHAR(100) NOT NULL,
            ap_pat VARCHAR(100) NOT NULL,
            ap_mat VARCHAR(100),
            rut VARCHAR(20) UNIQUE NOT NULL,
            email VARCHAR(120),
            telefono VARCHAR(20),
            direccion TEXT,
            fecha_nacimiento DATE,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado BOOLEAN DEFAULT TRUE
        );
        
        -- PRODUCTOS
        CREATE TABLE productos (
            producto_id SERIAL PRIMARY KEY,
            nombre VARCHAR(200) NOT NULL,
            descripcion TEXT,
            stock INTEGER DEFAULT 0,
            precio_unitario DECIMAL(10,2) NOT NULL,
            categoria VARCHAR(100),
            marca VARCHAR(100),
            sku VARCHAR(50) UNIQUE,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado BOOLEAN DEFAULT TRUE
        );
        
        -- VENTAS
        CREATE TABLE ventas (
            venta_id SERIAL PRIMARY KEY,
            cliente_id INTEGER REFERENCES clientes(cliente_id),
            usuario_id INTEGER REFERENCES usuarios(usuario_id),
            fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total DECIMAL(10,2) NOT NULL,
            descuento DECIMAL(5,2) DEFAULT 0,
            metodo_pago VARCHAR(50),
            observaciones TEXT,
            estado VARCHAR(20) DEFAULT 'completada'
        );
        
        -- DETALLE VENTAS
        CREATE TABLE detalle_ventas (
            detalle_id SERIAL PRIMARY KEY,
            venta_id INTEGER REFERENCES ventas(venta_id),
            producto_id INTEGER REFERENCES productos(producto_id),
            cantidad INTEGER NOT NULL,
            precio_unitario DECIMAL(10,2) NOT NULL,
            subtotal DECIMAL(10,2) NOT NULL
        );
        """
        
        # Ejecutar creación de tablas
        for statement in tables_sql.split(';'):
            if statement.strip():
                cursor_test.execute(statement)
        
        conn_test.commit()
        
        # Insertar datos iniciales
        print("6️⃣ Insertando datos iniciales...")
        
        # Roles
        cursor_test.execute("""
            INSERT INTO roles (nombre, descripcion) VALUES 
            ('Administrador', 'Acceso total al sistema'),
            ('Médico Oftalmólogo', 'Acceso al módulo médico'),
            ('Vendedor', 'Acceso al módulo comercial'),
            ('Recepcionista', 'Registro de pacientes');
        """)
        
        # Usuario administrador
        cursor_test.execute("""
            INSERT INTO usuarios (rol_id, username, password, nombre, ap_pat, ap_mat, email) 
            VALUES (
                1, 
                'admin', 
                '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewfy1QopLkknB5YG',
                'Administrador', 
                'Sistema', 
                '', 
                'admin@opticamaipu.cl'
            );
        """)
        
        conn_test.commit()
        conn_test.close()
        
        print("\n🎉 ¡BASE DE DATOS CREADA EXITOSAMENTE!")
        print("✅ Configuración compatible Windows")
        print("✅ Encoding UTF-8")
        print("✅ Tablas comerciales creadas")
        print("✅ Usuario admin creado (admin/admin123)")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    crear_bd_compatible()