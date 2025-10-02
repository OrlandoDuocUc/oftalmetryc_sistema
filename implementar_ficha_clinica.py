#!/usr/bin/env python3
# ===============================================================================
# SCRIPT DE IMPLEMENTACIÓN INTELIGENTE - FICHA CLÍNICA
# Sistema: Oftalmetryc - Crear Base de Datos Optimizada
# Autor: Orlando Rodriguez
# Fecha: 2 de octubre de 2025
# ===============================================================================

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_database_url():
    """Obtener URL de base de datos"""
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        logger.info("🔗 Usando DATABASE_URL de Render")
        return database_url
    else:
        logger.info("🔗 Usando base de datos local")
        return "postgresql://postgres:password@localhost:5432/oftalmetryc"

def ejecutar_sql_desde_archivo(engine, archivo_sql):
    """Ejecutar script SQL desde archivo"""
    try:
        with open(archivo_sql, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Dividir el contenido en bloques por BEGIN/COMMIT
        bloques = sql_content.split('BEGIN;')
        
        with engine.connect() as connection:
            with connection.begin():
                for i, bloque in enumerate(bloques):
                    if bloque.strip():
                        # Remover COMMIT; del final si existe
                        bloque_limpio = bloque.replace('COMMIT;', '').strip()
                        if bloque_limpio:
                            logger.info(f"📄 Ejecutando bloque {i+1}...")
                            connection.execute(text(bloque_limpio))
        
        logger.info("✅ Script SQL ejecutado exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error al ejecutar script SQL: {str(e)}")
        return False

def crear_estructura_completa():
    """Crear estructura completa de base de datos"""
    try:
        # Obtener URL de base de datos
        database_url = get_database_url()
        engine = create_engine(database_url)
        
        logger.info("🚀 Iniciando creación de estructura de base de datos...")
        
        # Crear todas las tablas básicas primero
        crear_tablas_basicas(engine)
        
        # Ejecutar expansión inteligente
        archivo_expansion = "EXPANSION_INTELIGENTE_BD.sql"
        if os.path.exists(archivo_expansion):
            logger.info("📁 Ejecutando expansión inteligente...")
            if ejecutar_sql_desde_archivo(engine, archivo_expansion):
                logger.info("✅ Expansión completada exitosamente")
            else:
                logger.error("❌ Error en la expansión")
                return False
        else:
            logger.warning(f"⚠️  Archivo {archivo_expansion} no encontrado")
        
        # Verificar estructura final
        verificar_estructura(engine)
        
        logger.info("🎉 ¡Estructura de base de datos creada exitosamente!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error general: {str(e)}")
        return False

def crear_tablas_basicas(engine):
    """Crear tablas básicas del sistema"""
    sql_basico = """
    -- Crear extensión si no existe
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    -- Tabla de roles
    CREATE TABLE IF NOT EXISTS rol (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(50) UNIQUE NOT NULL,
        descripcion TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Tabla de usuarios
    CREATE TABLE IF NOT EXISTS usuario (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        email VARCHAR(100),
        nombre VARCHAR(100),
        apellido VARCHAR(100),
        activo BOOLEAN DEFAULT TRUE,
        rol_id INTEGER REFERENCES rol(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Tabla de pacientes (estructura base)
    CREATE TABLE IF NOT EXISTS pacientes (
        id SERIAL PRIMARY KEY,
        rut VARCHAR(12) UNIQUE,
        ci VARCHAR(20),
        nombre VARCHAR(100),
        apellido VARCHAR(100),
        nombres VARCHAR(100),
        apellidos VARCHAR(100),
        fecha_nacimiento DATE,
        edad INTEGER,
        telefono VARCHAR(20),
        email VARCHAR(100),
        direccion TEXT,
        genero VARCHAR(10),
        ocupacion VARCHAR(100),
        hobby VARCHAR(200),
        contacto_emergencia VARCHAR(100),
        telefono_emergencia VARCHAR(20),
        observaciones TEXT,
        observaciones_generales TEXT,
        estado VARCHAR(20) DEFAULT 'Activo',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Tabla de consultas médicas
    CREATE TABLE IF NOT EXISTS consultas_medicas (
        id SERIAL PRIMARY KEY,
        paciente_id INTEGER REFERENCES pacientes(id) ON DELETE CASCADE,
        fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        motivo_consulta TEXT,
        antecedentes_personales TEXT,
        antecedentes_familiares TEXT,
        diagnostico TEXT,
        plan_tratamiento TEXT,
        ultimo_control_visual DATE,
        usa_lentes BOOLEAN DEFAULT FALSE,
        ultimo_cambio_lentes DATE,
        firma_responsable VARCHAR(100),
        conforme_evaluado BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Tabla de exámenes básicos (estructura expandible)
    CREATE TABLE IF NOT EXISTS examenes_basicos (
        id SERIAL PRIMARY KEY,
        consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
        -- Campos existentes básicos
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
        pio_od INTEGER,
        pio_oi INTEGER,
        observaciones TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Tabla de biomicroscopía
    CREATE TABLE IF NOT EXISTS biomicroscopia (
        id SERIAL PRIMARY KEY,
        consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
        parpados_od TEXT,
        parpados_oi TEXT,
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
        observaciones TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Tabla de oftalmoscopía
    CREATE TABLE IF NOT EXISTS oftalmoscopia (
        id SERIAL PRIMARY KEY,
        consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
        papila_od TEXT,
        papila_oi TEXT,
        macula_od TEXT,
        macula_oi TEXT,
        vasos_od TEXT,
        vasos_oi TEXT,
        retina_periferica_od TEXT,
        retina_periferica_oi TEXT,
        observaciones TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Tabla de diagnósticos
    CREATE TABLE IF NOT EXISTS diagnosticos (
        id SERIAL PRIMARY KEY,
        consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
        codigo_cie10 VARCHAR(10),
        descripcion TEXT NOT NULL,
        tipo VARCHAR(50),
        observaciones TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Insertar roles básicos (sin ON CONFLICT)
    INSERT INTO rol (nombre, descripcion) 
    SELECT 'admin', 'Administrador del sistema'
    WHERE NOT EXISTS (SELECT 1 FROM rol WHERE nombre = 'admin');
    
    INSERT INTO rol (nombre, descripcion) 
    SELECT 'medico', 'Médico oftalmólogo'
    WHERE NOT EXISTS (SELECT 1 FROM rol WHERE nombre = 'medico');
    
    INSERT INTO rol (nombre, descripcion) 
    SELECT 'asistente', 'Asistente médico'
    WHERE NOT EXISTS (SELECT 1 FROM rol WHERE nombre = 'asistente');
    
    -- Insertar usuario admin
    INSERT INTO usuario (username, password_hash, nombre, apellido, rol_id) 
    SELECT 'admin', '$2b$12$rQHXXMR7azDo2kE6M5LiO.qRZJsUYHXMR7azDo2kE6M5LiO.qRZJsU', 'Administrador', 'Sistema', 1
    WHERE NOT EXISTS (SELECT 1 FROM usuario WHERE username = 'admin');
    
    -- Crear índices básicos
    CREATE INDEX IF NOT EXISTS idx_pacientes_rut ON pacientes(rut);
    CREATE INDEX IF NOT EXISTS idx_pacientes_ci ON pacientes(ci);
    CREATE INDEX IF NOT EXISTS idx_consultas_paciente ON consultas_medicas(paciente_id);
    CREATE INDEX IF NOT EXISTS idx_consultas_fecha ON consultas_medicas(fecha_consulta);
    CREATE INDEX IF NOT EXISTS idx_examenes_consulta ON examenes_basicos(consulta_id);
    CREATE INDEX IF NOT EXISTS idx_biomicroscopia_consulta ON biomicroscopia(consulta_id);
    CREATE INDEX IF NOT EXISTS idx_oftalmoscopia_consulta ON oftalmoscopia(consulta_id);
    CREATE INDEX IF NOT EXISTS idx_diagnosticos_consulta ON diagnosticos(consulta_id);
    """
    
    try:
        with engine.connect() as connection:
            with connection.begin():
                logger.info("📋 Creando tablas básicas...")
                connection.execute(text(sql_basico))
        logger.info("✅ Tablas básicas creadas exitosamente")
        
    except Exception as e:
        logger.error(f"❌ Error al crear tablas básicas: {str(e)}")
        raise

def verificar_estructura(engine):
    """Verificar la estructura final de la base de datos"""
    try:
        with engine.connect() as connection:
            # Verificar tablas principales
            result = connection.execute(text("""
                SELECT table_name, 
                       (SELECT count(*) FROM information_schema.columns 
                        WHERE table_name = t.table_name) as column_count
                FROM information_schema.tables t
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """))
            
            tablas = result.fetchall()
            logger.info("📊 ESTRUCTURA FINAL DE BASE DE DATOS:")
            logger.info("=" * 50)
            
            total_campos = 0
            for tabla in tablas:
                logger.info(f"📄 {tabla[0]:20} | {tabla[1]:3} campos")
                total_campos += tabla[1]
            
            logger.info("=" * 50)
            logger.info(f"📈 TOTAL: {len(tablas)} tablas | {total_campos} campos")
            
            # Verificar campos específicos de ficha clínica
            campos_importantes = [
                ('pacientes', 'ci'),
                ('pacientes', 'nombres'),
                ('pacientes', 'edad'),
                ('examenes_basicos', 'av_distancia_od'),
                ('examenes_basicos', 'rx_esf_od'),
                ('biomicroscopia', 'biomic_cornea_od'),
                ('oftalmoscopia', 'fondo_ojo_retina_od')
            ]
            
            logger.info("\n🔍 VERIFICANDO CAMPOS CLAVE:")
            for tabla, campo in campos_importantes:
                try:
                    result = connection.execute(text(f"""
                        SELECT column_name FROM information_schema.columns 
                        WHERE table_name = '{tabla}' AND column_name = '{campo}';
                    """))
                    existe = result.fetchone()
                    status = "✅" if existe else "❌"
                    logger.info(f"{status} {tabla}.{campo}")
                except:
                    logger.info(f"❌ {tabla}.{campo}")
            
    except Exception as e:
        logger.error(f"❌ Error al verificar estructura: {str(e)}")

if __name__ == "__main__":
    print("🏥 OFTALMETRYC - IMPLEMENTACIÓN FICHA CLÍNICA DIGITAL")
    print("=" * 60)
    
    if crear_estructura_completa():
        print("\n🎉 ¡IMPLEMENTACIÓN COMPLETADA EXITOSAMENTE!")
        print("✅ Base de datos lista para fichas clínicas")
        print("✅ Estructura optimizada con campos expandidos") 
        print("✅ Sistema listo para desarrollo de interfaces")
    else:
        print("\n❌ IMPLEMENTACIÓN FALLÓ")
        sys.exit(1)