#!/usr/bin/env python3
"""
Script simple para crear tablas y datos iniciales
"""

import psycopg2
from datetime import datetime
import hashlib

# Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'database': 'oftalmetryc_db',
    'user': 'postgres',
    'password': '12345',
    'port': '5432'
}

def create_tables_and_data():
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("🔨 Creando tablas...")
        
        # Crear tabla rol
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rol (
            rol_id BIGSERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            descripcion TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT NOW(),
            estado CHAR(1) DEFAULT 'A'
        );
        """)
        
        # Crear tabla usuario
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            usuario_id BIGSERIAL PRIMARY KEY,
            rol_id BIGINT REFERENCES rol(rol_id),
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            nombre VARCHAR(100) NOT NULL,
            ap_pat VARCHAR(100) NOT NULL,
            ap_mat VARCHAR(100),
            email VARCHAR(100),
            fecha_creacion TIMESTAMP DEFAULT NOW(),
            estado CHAR(1) DEFAULT 'A'
        );
        """)
        
        # Crear tabla cliente
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
            cliente_id BIGSERIAL PRIMARY KEY,
            nombres VARCHAR(100) NOT NULL,
            ap_pat VARCHAR(100) NOT NULL,
            ap_mat VARCHAR(100),
            email TEXT,
            telefono VARCHAR(20),
            direccion TEXT,
            fecha_creacion TIMESTAMP DEFAULT NOW(),
            estado CHAR(1) DEFAULT 'A'
        );
        """)
        
        # Crear tabla producto
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS producto (
            producto_id BIGSERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            descripcion VARCHAR(255),
            stock INTEGER NOT NULL,
            precio_unitario DECIMAL(10,2) NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT NOW(),
            estado VARCHAR(20) DEFAULT 'activo'
        );
        """)
        
        # Crear tabla venta
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS venta (
            venta_id BIGSERIAL PRIMARY KEY,
            producto_id BIGINT REFERENCES producto(producto_id),
            usuario_id BIGINT REFERENCES usuario(usuario_id),
            cliente_id BIGINT REFERENCES cliente(cliente_id),
            cantidad INTEGER NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            fecha TIMESTAMP DEFAULT NOW()
        );
        """)
        
        print("✅ Tablas creadas!")
        
        # Insertar datos iniciales
        print("📊 Insertando datos iniciales...")
        
        # Roles
        cursor.execute("""
        INSERT INTO rol (nombre, descripcion) VALUES 
        ('Administrador', 'Usuario con acceso completo al sistema'),
        ('Vendedor', 'Usuario con acceso a ventas e inventario')
        ON CONFLICT DO NOTHING;
        """)
        
        # Usuario admin (password: admin)
        password_hash = hashlib.sha256('admin'.encode()).hexdigest()
        cursor.execute("""
        INSERT INTO usuario (rol_id, username, password, nombre, ap_pat, ap_mat, email) 
        VALUES (1, 'admin', %s, 'Administrador', 'Sistema', 'Oftalmetryc', 'admin@oftalmetryc.com')
        ON CONFLICT (username) DO NOTHING;
        """, (password_hash,))
        
        # Productos de ejemplo
        cursor.execute("""
        INSERT INTO producto (nombre, descripcion, stock, precio_unitario) VALUES 
        ('Lentes de Sol Ray-Ban', 'Lentes de sol clásicos con protección UV', 25, 89990),
        ('Montura Oakley Classic', 'Montura deportiva resistente', 15, 125000),
        ('Lentes Progresivos Zeiss', 'Lentes progresivos de alta calidad', 10, 180000),
        ('Lentes de Contacto Acuvue', 'Lentes de contacto mensuales', 50, 35000),
        ('Líquido Limpiador', 'Líquido para limpieza de lentes', 30, 8500)
        ON CONFLICT DO NOTHING;
        """)
        
        # Cliente de ejemplo
        cursor.execute("""
        INSERT INTO cliente (nombres, ap_pat, ap_mat, email, telefono, direccion) VALUES 
        ('Juan Carlos', 'García', 'López', 'juan.garcia@email.com', '+56912345678', 'Av. Providencia 123, Santiago')
        ON CONFLICT DO NOTHING;
        """)
        
        conn.commit()
        print("✅ Datos iniciales cargados!")
        print("👤 Usuario admin creado: admin / admin")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = create_tables_and_data()
    if success:
        print("🎉 Base de datos lista para Oftalmetryc!")
    else:
        print("💥 Error al configurar la base de datos")