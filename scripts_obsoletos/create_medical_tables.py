#!/usr/bin/env python3
"""
Script para crear las tablas del módulo médico oftalmológico
Oftalmetryc - Sistema Profesional de Gestión Óptica
"""

from sqlalchemy import create_engine, text
import os
from urllib.parse import quote_plus

def create_medical_tables():
    """Crear todas las tablas del módulo médico oftalmológico"""
    
    try:
        # Configuración de la base de datos usando SQLAlchemy
        DB_USER = 'postgres'
        DB_PASSWORD = 'admin'
        DB_HOST = 'localhost'
        DB_PORT = '5432'
        DB_NAME = 'oftalmetryc_db'
        
        # URL de conexión PostgreSQL
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
        # Crear engine
        engine = create_engine(DATABASE_URL)
        
        print("Creando tablas del módulo médico oftalmológico...")
        
        with engine.connect() as connection:
        # 1. Tabla de Pacientes (ampliación de clientes para datos médicos)
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS pacientes (
                    id SERIAL PRIMARY KEY,
                    cliente_id INTEGER REFERENCES clientes(id) ON DELETE CASCADE,
                    numero_historia VARCHAR(20) UNIQUE NOT NULL,
                    fecha_primera_consulta DATE NOT NULL DEFAULT CURRENT_DATE,
                    ocupacion VARCHAR(100),
                    telefono_emergencia VARCHAR(20),
                    contacto_emergencia VARCHAR(100),
                    alergias TEXT,
                    medicamentos_actuales TEXT,
                    antecedentes_oculares TEXT,
                    antecedentes_familiares TEXT,
                    antecedentes_medicos TEXT,
                    observaciones_generales TEXT,
                    activo BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # 2. Tabla de Consultas Médicas
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS consultas_medicas (
                    id SERIAL PRIMARY KEY,
                    paciente_id INTEGER REFERENCES pacientes(id) ON DELETE CASCADE,
                    numero_consulta VARCHAR(20) UNIQUE NOT NULL,
                    fecha_consulta TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    tipo_consulta VARCHAR(50) NOT NULL DEFAULT 'Control',
                    motivo_consulta TEXT NOT NULL,
                    sintomas_actuales TEXT,
                    tiempo_evolucion VARCHAR(100),
                    tratamiento_previo TEXT,
                    profesional_id INTEGER REFERENCES usuarios(id),
                    estado VARCHAR(20) DEFAULT 'En Proceso',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # 3. Tabla de Examen Básico (Agudeza Visual, etc.)
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS examenes_basicos (
                    id SERIAL PRIMARY KEY,
                    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
                    
                    -- Agudeza Visual Lejana
                    od_sc_lejos VARCHAR(10),
                    od_cc_lejos VARCHAR(10),
                    oi_sc_lejos VARCHAR(10),
                    oi_cc_lejos VARCHAR(10),
                    ao_sc_lejos VARCHAR(10),
                    ao_cc_lejos VARCHAR(10),
                    
                    -- Agudeza Visual Cercana
                    od_sc_cerca VARCHAR(10),
                    od_cc_cerca VARCHAR(10),
                    oi_sc_cerca VARCHAR(10),
                    oi_cc_cerca VARCHAR(10),
                    ao_sc_cerca VARCHAR(10),
                    ao_cc_cerca VARCHAR(10),
                    
                    -- Presión Intraocular
                    pio_od VARCHAR(10),
                    pio_oi VARCHAR(10),
                    metodo_pio VARCHAR(50),
                    hora_pio TIME,
                    
                    -- Cover Test
                    cover_test_lejos VARCHAR(100),
                    cover_test_cerca VARCHAR(100),
                    
                    -- Motilidad Ocular
                    motilidad_od TEXT,
                    motilidad_oi TEXT,
                    convergencia VARCHAR(50),
                    
                    -- Reflejos Pupilares
                    reflejo_fotomotor_od VARCHAR(50),
                    reflejo_fotomotor_oi VARCHAR(50),
                    reflejo_consensual_od VARCHAR(50),
                    reflejo_consensual_oi VARCHAR(50),
                    defecto_pupilar_aferente VARCHAR(100),
                    
                    observaciones_examen_basico TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # 4. Tabla de Refracción
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS refracciones (
                    id SERIAL PRIMARY KEY,
                    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
                    tipo_refraccion VARCHAR(20) NOT NULL DEFAULT 'Subjetiva',
                    
                    -- Ojo Derecho
                    od_esfera DECIMAL(4,2),
                    od_cilindro DECIMAL(4,2),
                    od_eje INTEGER,
                    od_prisma DECIMAL(3,2),
                    od_base VARCHAR(10),
                    od_add DECIMAL(3,2),
                    od_dip DECIMAL(4,1),
                    
                    -- Ojo Izquierdo
                    oi_esfera DECIMAL(4,2),
                    oi_cilindro DECIMAL(4,2),
                    oi_eje INTEGER,
                    oi_prisma DECIMAL(3,2),
                    oi_base VARCHAR(10),
                    oi_add DECIMAL(3,2),
                    oi_dip DECIMAL(4,1),
                    
                    -- Datos adicionales
                    distancia_pupilar DECIMAL(4,1),
                    altura_pupilar DECIMAL(4,1),
                    tipo_lente VARCHAR(50),
                    observaciones_refraccion TEXT,
                    recomendaciones TEXT,
                    
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # 5. Tabla de Biomicroscopía
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS biomicroscopias (
                    id SERIAL PRIMARY KEY,
                    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
                    
                    -- Párpados y Pestañas OD
                    parpados_od TEXT,
                    pestanas_od TEXT,
                    glandulas_meibomio_od TEXT,
                    
                    -- Párpados y Pestañas OI
                    parpados_oi TEXT,
                    pestanas_oi TEXT,
                    glandulas_meibomio_oi TEXT,
                    
                    -- Conjuntiva OD
                    conjuntiva_bulbar_od TEXT,
                    conjuntiva_tarsal_od TEXT,
                    conjuntiva_fondo_saco_od TEXT,
                    
                    -- Conjuntiva OI
                    conjuntiva_bulbar_oi TEXT,
                    conjuntiva_tarsal_oi TEXT,
                    conjuntiva_fondo_saco_oi TEXT,
                    
                    -- Córnea OD
                    cornea_epitelio_od TEXT,
                    cornea_estroma_od TEXT,
                    cornea_endotelio_od TEXT,
                    
                    -- Córnea OI
                    cornea_epitelio_oi TEXT,
                    cornea_estroma_oi TEXT,
                    cornea_endotelio_oi TEXT,
                    
                    -- Cámara Anterior OD
                    camara_anterior_od TEXT,
                    profundidad_camara_od VARCHAR(20),
                    humor_acuoso_od TEXT,
                    
                    -- Cámara Anterior OI
                    camara_anterior_oi TEXT,
                    profundidad_camara_oi VARCHAR(20),
                    humor_acuoso_oi TEXT,
                    
                    -- Iris OD
                    iris_od TEXT,
                    pupilas_od TEXT,
                    
                    -- Iris OI
                    iris_oi TEXT,
                    pupilas_oi TEXT,
                    
                    -- Cristalino OD
                    cristalino_od TEXT,
                    opacidades_od TEXT,
                    
                    -- Cristalino OI
                    cristalino_oi TEXT,
                    opacidades_oi TEXT,
                    
                    observaciones_biomicroscopia TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # 6. Tabla de Fondo de Ojo
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS fondos_ojo (
                    id SERIAL PRIMARY KEY,
                    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
                    metodo_examen VARCHAR(50) DEFAULT 'Oftalmoscopía Directa',
                    midriasis_aplicada BOOLEAN DEFAULT FALSE,
                    
                    -- Papila OD
                    papila_od_forma VARCHAR(50),
                    papila_od_color VARCHAR(50),
                    papila_od_bordes VARCHAR(100),
                    papila_od_excavacion VARCHAR(20),
                    papila_od_vascularizacion TEXT,
                    
                    -- Papila OI
                    papila_oi_forma VARCHAR(50),
                    papila_oi_color VARCHAR(50),
                    papila_oi_bordes VARCHAR(100),
                    papila_oi_excavacion VARCHAR(20),
                    papila_oi_vascularizacion TEXT,
                    
                    -- Mácula OD
                    macula_od_aspecto TEXT,
                    macula_od_reflejo_foveal VARCHAR(50),
                    macula_od_pigmentacion TEXT,
                    
                    -- Mácula OI
                    macula_oi_aspecto TEXT,
                    macula_oi_reflejo_foveal VARCHAR(50),
                    macula_oi_pigmentacion TEXT,
                    
                    -- Retina Periférica OD
                    retina_periferia_od TEXT,
                    vasos_od TEXT,
                    
                    -- Retina Periférica OI
                    retina_periferia_oi TEXT,
                    vasos_oi TEXT,
                    
                    -- Vítreo
                    vitreo_od TEXT,
                    vitreo_oi TEXT,
                    
                    observaciones_fondo_ojo TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # 7. Tabla de Diagnósticos
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS diagnosticos (
                    id SERIAL PRIMARY KEY,
                    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
                    ojo VARCHAR(10) NOT NULL, -- 'OD', 'OI', 'AO'
                    codigo_cie10 VARCHAR(10),
                    descripcion_diagnostico TEXT NOT NULL,
                    tipo_diagnostico VARCHAR(20) DEFAULT 'Principal', -- Principal, Secundario, Diferencial
                    severidad VARCHAR(20),
                    observaciones TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # 8. Tabla de Tratamientos
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS tratamientos (
                    id SERIAL PRIMARY KEY,
                    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
                    tipo_tratamiento VARCHAR(50) NOT NULL, -- Farmacológico, Óptico, Quirúrgico, Observación
                    descripcion TEXT NOT NULL,
                    medicamento VARCHAR(100),
                    dosis VARCHAR(50),
                    frecuencia VARCHAR(50),
                    duracion VARCHAR(50),
                    via_administracion VARCHAR(30),
                    instrucciones TEXT,
                    fecha_inicio DATE DEFAULT CURRENT_DATE,
                    fecha_fin DATE,
                    activo BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # 9. Tabla de Seguimientos
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS seguimientos (
                    id SERIAL PRIMARY KEY,
                    paciente_id INTEGER REFERENCES pacientes(id) ON DELETE CASCADE,
                    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
                    fecha_seguimiento DATE NOT NULL,
                    tipo_seguimiento VARCHAR(50), -- Control, Urgencia, Revisión
                    motivo TEXT,
                    evolucion TEXT,
                    cumplimiento_tratamiento VARCHAR(50),
                    efectos_adversos TEXT,
                    modificaciones_tratamiento TEXT,
                    proxima_cita DATE,
                    observaciones TEXT,
                    profesional_id INTEGER REFERENCES usuarios(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # 10. Tabla de Archivos Adjuntos (para imágenes, estudios, etc.)
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS archivos_medicos (
                    id SERIAL PRIMARY KEY,
                    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
                    nombre_archivo VARCHAR(255) NOT NULL,
                    tipo_archivo VARCHAR(50), -- Imagen, PDF, Estudio, Laboratorio
                    ruta_archivo VARCHAR(500) NOT NULL,
                    descripcion TEXT,
                    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usuario_id INTEGER REFERENCES usuarios(id)
                );
            """))
            
            # Crear índices para optimizar consultas
            print("Creando índices...")
            
            indices = [
                "CREATE INDEX IF NOT EXISTS idx_pacientes_cliente ON pacientes(cliente_id);",
                "CREATE INDEX IF NOT EXISTS idx_pacientes_historia ON pacientes(numero_historia);",
                "CREATE INDEX IF NOT EXISTS idx_consultas_paciente ON consultas_medicas(paciente_id);",
                "CREATE INDEX IF NOT EXISTS idx_consultas_fecha ON consultas_medicas(fecha_consulta);",
                "CREATE INDEX IF NOT EXISTS idx_examenes_consulta ON examenes_basicos(consulta_id);",
                "CREATE INDEX IF NOT EXISTS idx_refracciones_consulta ON refracciones(consulta_id);",
                "CREATE INDEX IF NOT EXISTS idx_biomicroscopias_consulta ON biomicroscopias(consulta_id);",
                "CREATE INDEX IF NOT EXISTS idx_fondos_consulta ON fondos_ojo(consulta_id);",
                "CREATE INDEX IF NOT EXISTS idx_diagnosticos_consulta ON diagnosticos(consulta_id);",
                "CREATE INDEX IF NOT EXISTS idx_tratamientos_consulta ON tratamientos(consulta_id);",
                "CREATE INDEX IF NOT EXISTS idx_seguimientos_paciente ON seguimientos(paciente_id);",
                "CREATE INDEX IF NOT EXISTS idx_archivos_consulta ON archivos_medicos(consulta_id);"
            ]
            
            for indice in indices:
                connection.execute(text(indice))
            
            # Crear secuencias para números de historia y consulta
            connection.execute(text("""
                CREATE SEQUENCE IF NOT EXISTS seq_numero_historia 
                START 1000 INCREMENT 1;
            """))
            
            connection.execute(text("""
                CREATE SEQUENCE IF NOT EXISTS seq_numero_consulta 
                START 100000 INCREMENT 1;
            """))
            
            # Crear función para generar número de historia automático
            connection.execute(text("""
                CREATE OR REPLACE FUNCTION generar_numero_historia()
                RETURNS TEXT AS $$
                BEGIN
                    RETURN 'HC-' || LPAD(nextval('seq_numero_historia')::TEXT, 6, '0');
                END;
                $$ LANGUAGE plpgsql;
            """))
            
            # Crear función para generar número de consulta automático
            connection.execute(text("""
                CREATE OR REPLACE FUNCTION generar_numero_consulta()
                RETURNS TEXT AS $$
                BEGIN
                    RETURN 'CON-' || TO_CHAR(CURRENT_DATE, 'YYYY') || '-' || LPAD(nextval('seq_numero_consulta')::TEXT, 6, '0');
                END;
                $$ LANGUAGE plpgsql;
            """))
            
            # Crear triggers para actualizar updated_at
            trigger_sql = """
                CREATE OR REPLACE FUNCTION update_updated_at_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """
            connection.execute(text(trigger_sql))
            
            # Aplicar trigger a las tablas que lo necesiten
            tablas_con_updated_at = ['pacientes', 'consultas_medicas']
            for tabla in tablas_con_updated_at:
                connection.execute(text(f"""
                    DROP TRIGGER IF EXISTS trigger_updated_at_{tabla} ON {tabla};
                    CREATE TRIGGER trigger_updated_at_{tabla}
                        BEFORE UPDATE ON {tabla}
                        FOR EACH ROW
                        EXECUTE FUNCTION update_updated_at_column();
                """))
            
            connection.commit()
        
        print("✅ Todas las tablas del módulo médico han sido creadas exitosamente!")
        print("\nTablas creadas:")
        print("- pacientes (datos médicos del cliente)")
        print("- consultas_medicas (registro de consultas)")
        print("- examenes_basicos (agudeza visual, PIO, etc.)")
        print("- refracciones (prescripciones ópticas)")
        print("- biomicroscopias (examen segmento anterior)")
        print("- fondos_ojo (examen segmento posterior)")
        print("- diagnosticos (diagnósticos por consulta)")
        print("- tratamientos (prescripciones médicas)")
        print("- seguimientos (evolución del paciente)")
        print("- archivos_medicos (documentos adjuntos)")
        print("\n✅ Funciones y triggers creados para numeración automática")
        
    except Exception as e:
        print(f"❌ Error al crear las tablas: {e}")
        raise e

if __name__ == "__main__":
    create_medical_tables()