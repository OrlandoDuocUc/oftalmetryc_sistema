#!/usr/bin/env python3
"""
Script para inicializar automáticamente la base de datos
Se ejecuta automáticamente cuando el sistema detecta BD vacía
"""

import os
import psycopg2
from psycopg2 import sql

def get_database_url():
    """Obtener URL de base de datos"""
    return os.environ.get('DATABASE_URL')

def init_database():
    """Inicializar base de datos con todas las tablas y datos"""
    
    # Script SQL completo
    sql_script = """
-- TABLAS PRINCIPALES DEL SISTEMA
CREATE TABLE IF NOT EXISTS rol (
    rol_id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    estado CHAR(1) DEFAULT 'A' NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS usuario (
    usuario_id BIGSERIAL PRIMARY KEY,
    rol_id BIGINT REFERENCES rol(rol_id),
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    ap_pat VARCHAR(100) NOT NULL,
    ap_mat VARCHAR(100),
    email VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado CHAR(1) DEFAULT 'A' NOT NULL
);

CREATE TABLE IF NOT EXISTS categoria (
    categoria_id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    estado CHAR(1) DEFAULT 'A' NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS producto (
    producto_id BIGSERIAL PRIMARY KEY,
    categoria_id BIGINT REFERENCES categoria(categoria_id),
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    stock INTEGER DEFAULT 0,
    precio_unitario DECIMAL(10,2) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado CHAR(1) DEFAULT 'A' NOT NULL
);

CREATE TABLE IF NOT EXISTS cliente (
    cliente_id BIGSERIAL PRIMARY KEY,
    rut VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado CHAR(1) DEFAULT 'A' NOT NULL
);

CREATE TABLE IF NOT EXISTS venta (
    venta_id BIGSERIAL PRIMARY KEY,
    producto_id BIGINT REFERENCES producto(producto_id),
    usuario_id BIGINT REFERENCES usuario(usuario_id),
    cliente_id BIGINT REFERENCES cliente(cliente_id),
    cantidad INTEGER NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLAS MÉDICAS OFTALMETRYC
CREATE TABLE IF NOT EXISTS pacientes (
    id SERIAL PRIMARY KEY,
    rut VARCHAR(12) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    ocupacion VARCHAR(100),
    contacto_emergencia VARCHAR(100),
    telefono_emergencia VARCHAR(20),
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS consultas_medicas (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER REFERENCES pacientes(id) ON DELETE CASCADE,
    fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    medico VARCHAR(100),
    motivo_consulta TEXT,
    anamnesis TEXT,
    antecedentes_personales TEXT,
    antecedentes_familiares TEXT,
    medicamentos_actuales TEXT,
    alergias TEXT,
    diagnostico TEXT,
    plan_tratamiento TEXT,
    observaciones_generales TEXT,
    proxima_cita DATE,
    estado VARCHAR(20) DEFAULT 'activa',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS examenes_basicos (
    id SERIAL PRIMARY KEY,
    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
    od_sc_lejos VARCHAR(10),
    oi_sc_lejos VARCHAR(10),
    ao_sc_lejos VARCHAR(10),
    od_sc_cerca VARCHAR(10),
    oi_sc_cerca VARCHAR(10),
    ao_sc_cerca VARCHAR(10),
    od_cc_lejos VARCHAR(10),
    oi_cc_lejos VARCHAR(10),
    ao_cc_lejos VARCHAR(10),
    od_cc_cerca VARCHAR(10),
    oi_cc_cerca VARCHAR(10),
    ao_cc_cerca VARCHAR(10),
    od_esfera_obj DECIMAL(4,2),
    od_cilindro_obj DECIMAL(4,2),
    od_eje_obj INTEGER,
    oi_esfera_obj DECIMAL(4,2),
    oi_cilindro_obj DECIMAL(4,2),
    oi_eje_obj INTEGER,
    od_esfera_subj DECIMAL(4,2),
    od_cilindro_subj DECIMAL(4,2),
    od_eje_subj INTEGER,
    od_add DECIMAL(4,2),
    oi_esfera_subj DECIMAL(4,2),
    oi_cilindro_subj DECIMAL(4,2),
    oi_eje_subj INTEGER,
    oi_add DECIMAL(4,2),
    pio_od INTEGER,
    pio_oi INTEGER,
    metodo_pio VARCHAR(50),
    od_pupila_tamano DECIMAL(3,1),
    oi_pupila_tamano DECIMAL(3,1),
    od_reaccion_luz VARCHAR(20),
    oi_reaccion_luz VARCHAR(20),
    defecto_pupilar_aferente BOOLEAN DEFAULT FALSE,
    motilidad_normal BOOLEAN DEFAULT TRUE,
    limitacion_movimientos TEXT,
    nistagmo BOOLEAN DEFAULT FALSE,
    tipo_nistagmo VARCHAR(50),
    ishihara_resultado VARCHAR(10),
    tipo_discromatopsia VARCHAR(30),
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS diagnosticos (
    id SERIAL PRIMARY KEY,
    codigo_cie10 VARCHAR(10) NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    categoria VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DATOS INICIALES
INSERT INTO rol (nombre, descripcion) VALUES 
('Administrador', 'Acceso completo al sistema'),
('Vendedor', 'Acceso a ventas y productos'),
('Médico', 'Acceso al módulo médico')
ON CONFLICT DO NOTHING;

INSERT INTO categoria (nombre, descripcion) VALUES 
('Lentes', 'Lentes oftálmicos y de contacto'),
('Armazones', 'Armazones para anteojos'),
('Accesorios', 'Accesorios para cuidado visual'),
('Medicamentos', 'Medicamentos oftálmicos')
ON CONFLICT DO NOTHING;

INSERT INTO usuario (nombre, ap_pat, ap_mat, username, email, password, estado, rol_id) VALUES 
('Administrador', 'Sistema', '', 'admin', 'admin@oftalmetryc.com', 'scrypt:32768:8:1$YNx7QtiZ2BTdqWeB$56f458904cb782fd026c1b4f11fe75c59c9b2e92b48fd0e09f084d29add66d3362a3b2adfdbce70e41f2df68377128072031785b0ff1201ac51040cf1da9b4f4', 'A', 1),
('Orlando', 'Usuario', 'Vendedor', 'orlando', 'orlando@oftalmetryc.com', 'scrypt:32768:8:1$nkA90b86YTTTtLjT$d3fe47fe13d965d07bfb90a885b86cb02149a10b24b7eb012b01f07d4abdf33e3d0e839f06badf78bd4dc6f10c06e3507a8d3d5b420eafa9dc024ecec9d92693', 'A', 2)
ON CONFLICT (username) DO NOTHING;

INSERT INTO producto (categoria_id, nombre, descripcion, stock, precio_unitario) VALUES 
(1, 'Lentes Bifocales', 'Lentes bifocales para presbicia', 50, 45000.00),
(1, 'Lentes Progresivos', 'Lentes progresivos premium', 30, 85000.00),
(2, 'Armazón Titanio', 'Armazón de titanio ultraliviano', 25, 35000.00),
(2, 'Armazón Acetato', 'Armazón de acetato clásico', 40, 25000.00),
(3, 'Líquido Limpiador', 'Solución limpiadora para lentes', 100, 5000.00)
ON CONFLICT DO NOTHING;

INSERT INTO diagnosticos (codigo_cie10, descripcion, categoria) VALUES
('H52.0', 'Hipermetropía', 'Refracción'),
('H52.1', 'Miopía', 'Refracción'),
('H52.2', 'Astigmatismo', 'Refracción'),
('H52.4', 'Presbicia', 'Refracción'),
('H25', 'Catarata senil', 'Cristalino'),
('H40.1', 'Glaucoma primario de ángulo abierto', 'Glaucoma'),
('H10.9', 'Conjuntivitis no especificada', 'Conjuntiva'),
('Z01.0', 'Examen de los ojos y de la visión', 'Preventivo')
ON CONFLICT DO NOTHING;

-- ÍNDICES
CREATE INDEX IF NOT EXISTS idx_usuario_username ON usuario(username);
CREATE INDEX IF NOT EXISTS idx_producto_categoria ON producto(categoria_id);
CREATE INDEX IF NOT EXISTS idx_venta_fecha ON venta(fecha);
CREATE INDEX IF NOT EXISTS idx_pacientes_rut ON pacientes(rut);
CREATE INDEX IF NOT EXISTS idx_consultas_paciente ON consultas_medicas(paciente_id);
"""
    
    try:
        # Conectar a la base de datos
        database_url = get_database_url()
        if not database_url:
            print("❌ No se encontró DATABASE_URL")
            return False
            
        print("🔄 Conectando a la base de datos...")
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        # Ejecutar script
        print("🚀 Creando tablas y datos iniciales...")
        cur.execute(sql_script)
        conn.commit()
        
        print("✅ Base de datos inicializada correctamente!")
        
        # Verificar tablas creadas
        cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
        tables = cur.fetchall()
        print(f"📊 Tablas creadas: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
            
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Inicializando base de datos...")
    success = init_database()
    if success:
        print("🎉 ¡Listo! Base de datos configurada.")
    else:
        print("💥 Error en la configuración.")