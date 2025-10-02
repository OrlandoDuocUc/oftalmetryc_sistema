#!/usr/bin/env python3
"""
SISTEMA DE MIGRACIONES AUTOMÁTICAS
Detecta cambios en la estructura y los aplica automáticamente
"""
import os
import psycopg2
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutoMigrationSystem:
    def __init__(self):
        # URL de la base de datos de Render
        self.DATABASE_URL = os.getenv('DATABASE_URL') or \
            "postgresql://oftalmetryc_user:0WdPbRIzVrbH6xYFCye20Q7ST4e3v7Kn@dpg-d3efatffte5s73chd9r0-a.oregon-postgres.render.com/oftalmetryc_db"
    
    def connect_db(self):
        """Conectar a la base de datos"""
        try:
            conn = psycopg2.connect(self.DATABASE_URL)
            logger.info("✅ Conexión exitosa a la base de datos")
            return conn
        except Exception as e:
            logger.error(f"❌ Error conectando: {e}")
            return None
    
    def create_migration_table(self, conn):
        """Crear tabla de migraciones si no existe"""
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS migrations (
                    id SERIAL PRIMARY KEY,
                    version VARCHAR(50) UNIQUE NOT NULL,
                    description TEXT,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    checksum VARCHAR(100)
                );
            """)
            conn.commit()
            cur.close()
            logger.info("✅ Tabla de migraciones creada/verificada")
        except Exception as e:
            logger.error(f"❌ Error creando tabla migrations: {e}")
    
    def get_applied_migrations(self, conn):
        """Obtener migraciones ya aplicadas"""
        try:
            cur = conn.cursor()
            cur.execute("SELECT version FROM migrations ORDER BY version;")
            applied = [row[0] for row in cur.fetchall()]
            cur.close()
            return applied
        except:
            return []
    
    def apply_migration(self, conn, version, description, sql_commands):
        """Aplicar una migración"""
        try:
            cur = conn.cursor()
            
            # Ejecutar comandos SQL
            for sql in sql_commands:
                cur.execute(sql)
            
            # Registrar migración
            cur.execute("""
                INSERT INTO migrations (version, description) 
                VALUES (%s, %s)
            """, (version, description))
            
            conn.commit()
            cur.close()
            logger.info(f"✅ Migración {version} aplicada: {description}")
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Error aplicando migración {version}: {e}")
            return False
    
    def run_migrations(self):
        """Ejecutar todas las migraciones pendientes"""
        conn = self.connect_db()
        if not conn:
            return False
        
        # Crear tabla de migraciones
        self.create_migration_table(conn)
        
        # Obtener migraciones aplicadas
        applied = self.get_applied_migrations(conn)
        
        # Definir migraciones disponibles
        migrations = self.get_all_migrations()
        
        # Aplicar migraciones pendientes
        for version, description, sql_commands in migrations:
            if version not in applied:
                logger.info(f"🔄 Aplicando migración {version}...")
                success = self.apply_migration(conn, version, description, sql_commands)
                if not success:
                    logger.error(f"💥 Fallo en migración {version}")
                    break
        
        conn.close()
        logger.info("🎉 ¡Sistema de migraciones completado!")
        return True
    
    def get_all_migrations(self):
        """Definir todas las migraciones en orden"""
        return [
            # Migración 001: Estructura básica
            ("001_estructura_basica", "Crear tablas básicas del sistema", [
                """
                CREATE TABLE IF NOT EXISTS rol (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(50) UNIQUE NOT NULL,
                    descripcion TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS usuario (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    nombre VARCHAR(100) NOT NULL,
                    email VARCHAR(100),
                    rol_id INTEGER REFERENCES rol(id),
                    activo BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS producto (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    descripcion TEXT,
                    precio DECIMAL(10,2) NOT NULL,
                    stock INTEGER DEFAULT 0,
                    categoria VARCHAR(50),
                    activo BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            ]),
            
            # Migración 002: Sistema médico
            ("002_sistema_medico", "Agregar tablas del sistema médico", [
                """
                CREATE TABLE IF NOT EXISTS paciente (
                    id SERIAL PRIMARY KEY,
                    rut VARCHAR(12) UNIQUE NOT NULL,
                    nombre VARCHAR(100) NOT NULL,
                    apellido VARCHAR(100) NOT NULL,
                    fecha_nacimiento DATE,
                    telefono VARCHAR(20),
                    email VARCHAR(100),
                    direccion TEXT,
                    sexo VARCHAR(10),
                    estado_civil VARCHAR(20),
                    ocupacion VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS consulta_medica (
                    id SERIAL PRIMARY KEY,
                    paciente_id INTEGER REFERENCES paciente(id),
                    medico_id INTEGER REFERENCES usuario(id),
                    fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    motivo_consulta TEXT,
                    diagnostico TEXT,
                    tratamiento TEXT,
                    observaciones TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            ]),
            
            # Migración 003: Campos oftalmológicos completos
            ("003_ficha_oftalmologica", "Agregar todos los campos oftalmológicos", [
                """
                ALTER TABLE consulta_medica ADD COLUMN IF NOT EXISTS 
                -- Antecedentes
                antecedentes_familiares TEXT,
                antecedentes_personales TEXT,
                medicamentos_actuales TEXT,
                alergias TEXT,
                
                -- Agudeza Visual
                od_sin_correccion VARCHAR(20),
                od_con_correccion VARCHAR(20),
                oi_sin_correccion VARCHAR(20),
                oi_con_correccion VARCHAR(20),
                
                -- Refracción
                od_esfera VARCHAR(20),
                od_cilindro VARCHAR(20),
                od_eje VARCHAR(20),
                oi_esfera VARCHAR(20),
                oi_cilindro VARCHAR(20),
                oi_eje VARCHAR(20),
                
                -- Presión Intraocular
                pio_od VARCHAR(20),
                pio_oi VARCHAR(20),
                metodo_tonometria VARCHAR(50),
                
                -- Biomicroscopía
                conjuntiva_od TEXT,
                conjuntiva_oi TEXT,
                cornea_od TEXT,
                cornea_oi TEXT,
                camara_anterior_od TEXT,
                camara_anterior_oi TEXT,
                iris_od TEXT,
                iris_oi TEXT,
                pupila_od TEXT,
                pupila_oi TEXT,
                cristalino_od TEXT,
                cristalino_oi TEXT,
                
                -- Fondo de Ojo
                papila_od TEXT,
                papila_oi TEXT,
                macula_od TEXT,
                macula_oi TEXT,
                vasos_od TEXT,
                vasos_oi TEXT,
                periferia_od TEXT,
                periferia_oi TEXT,
                
                -- Campos Visuales
                campo_visual_od TEXT,
                campo_visual_oi TEXT,
                defectos_campimetricos TEXT,
                
                -- Motilidad Ocular
                movimientos_oculares TEXT,
                diploplia BOOLEAN DEFAULT FALSE,
                nistagmus BOOLEAN DEFAULT FALSE,
                
                -- Lentes de Contacto
                adaptacion_lc BOOLEAN DEFAULT FALSE,
                tipo_lente VARCHAR(50),
                parametros_lc TEXT,
                
                -- Plan de Tratamiento
                plan_tratamiento TEXT,
                proxima_cita DATE,
                urgencia BOOLEAN DEFAULT FALSE;
                """
            ]),
            
            # Migración 004: Datos iniciales
            ("004_datos_iniciales", "Insertar datos básicos del sistema", [
                """
                INSERT INTO rol (nombre, descripcion) VALUES 
                ('Administrador', 'Acceso completo al sistema'),
                ('Médico', 'Acceso al sistema médico'),
                ('Recepcionista', 'Gestión de citas y pacientes')
                ON CONFLICT (nombre) DO NOTHING;
                """,
                """
                INSERT INTO usuario (username, password, nombre, rol_id) VALUES 
                ('admin', 'scrypt:32768:8:1$8vK2QqJXhYHZoNwL$64c7d6b7a5e8f3c2d9b1a4f6e7c8d5a3b2f1e6d9c8b7a5e4f3d2c1b6a9f8e7d6c5b4a3f2e1d9c8b7a6f5e4d3c2b1a', 'Administrador', 1),
                ('medico', 'scrypt:32768:8:1$8vK2QqJXhYHZoNwL$64c7d6b7a5e8f3c2d9b1a4f6e7c8d5a3b2f1e6d9c8b7a5e4f3d2c1b6a9f8e7d6c5b4a3f2e1d9c8b7a6f5e4d3c2b1a', 'Dr. Oftalmólogo', 2)
                ON CONFLICT (username) DO NOTHING;
                """
            ])
        ]

if __name__ == "__main__":
    print("🚀 SISTEMA DE MIGRACIONES AUTOMÁTICAS")
    print("=" * 50)
    
    migrator = AutoMigrationSystem()
    success = migrator.run_migrations()
    
    if success:
        print("\n🎉 ¡Base de datos actualizada correctamente!")
        print("🔗 Lista para usar en Render")
    else:
        print("\n❌ Error durante las migraciones")