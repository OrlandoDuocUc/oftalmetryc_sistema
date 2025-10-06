#!/usr/bin/env python3
"""
Script para crear las tablas del módulo médico en PostgreSQL
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import psycopg2
from config.settings import BaseConfig

def create_medical_tables():
    """Crea todas las tablas del módulo médico"""
    print("🏥 CREANDO TABLAS DEL MÓDULO MÉDICO")
    print("=" * 50)
    
    # Obtener configuración de base de datos
    config = BaseConfig()
    db_url = config.DATABASE_URL
    
    # Parsear URL de conexión
    # postgresql://postgres:12345@localhost:5432/optica_bd
    url_parts = db_url.replace('postgresql://', '').split('@')
    user_pass = url_parts[0].split(':')
    host_db = url_parts[1].split('/')
    host_port = host_db[0].split(':')
    
    connection_params = {
        'host': host_port[0],
        'port': int(host_port[1]),
        'database': host_db[1].split('?')[0],
        'user': user_pass[0],
        'password': user_pass[1]
    }
    
    print(f"🔗 Conectando a: {connection_params['host']}:{connection_params['port']}/{connection_params['database']}")
    
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        
        # SQL para crear tablas médicas
        medical_tables_sql = """
        -- Tabla 7: PACIENTES MÉDICOS
        CREATE TABLE IF NOT EXISTS pacientes_medicos (
            paciente_medico_id SERIAL PRIMARY KEY,
            cliente_id INTEGER REFERENCES clientes(cliente_id),
            numero_ficha VARCHAR(20) UNIQUE NOT NULL,
            antecedentes_medicos TEXT,
            antecedentes_oculares TEXT,
            alergias TEXT,
            medicamentos_actuales TEXT,
            contacto_emergencia VARCHAR(100),
            telefono_emergencia VARCHAR(20),
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado BOOLEAN DEFAULT TRUE
        );

        -- Tabla 8: FICHAS CLÍNICAS
        CREATE TABLE IF NOT EXISTS fichas_clinicas (
            ficha_id SERIAL PRIMARY KEY,
            paciente_medico_id INTEGER REFERENCES pacientes_medicos(paciente_medico_id),
            usuario_id INTEGER REFERENCES usuarios(usuario_id),
            numero_consulta VARCHAR(20) UNIQUE NOT NULL,
            fecha_consulta TIMESTAMP NOT NULL,
            motivo_consulta TEXT,
            historia_actual TEXT,
            
            -- AGUDEZA VISUAL OJO DERECHO
            av_od_sc VARCHAR(20),
            av_od_cc VARCHAR(20),
            av_od_ph VARCHAR(20),
            av_od_cerca VARCHAR(20),
            
            -- AGUDEZA VISUAL OJO IZQUIERDO
            av_oi_sc VARCHAR(20),
            av_oi_cc VARCHAR(20),
            av_oi_ph VARCHAR(20),
            av_oi_cerca VARCHAR(20),
            
            -- REFRACCIÓN OJO DERECHO
            esfera_od VARCHAR(10),
            cilindro_od VARCHAR(10),
            eje_od VARCHAR(10),
            adicion_od VARCHAR(10),
            
            -- REFRACCIÓN OJO IZQUIERDO
            esfera_oi VARCHAR(10),
            cilindro_oi VARCHAR(10),
            eje_oi VARCHAR(10),
            adicion_oi VARCHAR(10),
            
            -- DATOS GENERALES REFRACCIÓN
            distancia_pupilar VARCHAR(10),
            tipo_lente VARCHAR(50),
            
            estado VARCHAR(20) DEFAULT 'en_proceso',
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Tabla 9: BIOMICROSCOPÍA
        CREATE TABLE IF NOT EXISTS biomicroscopia (
            biomicroscopia_id SERIAL PRIMARY KEY,
            ficha_id INTEGER REFERENCES fichas_clinicas(ficha_id),
            
            -- OJO DERECHO
            parpados_od TEXT,
            conjuntiva_od TEXT,
            cornea_od TEXT,
            camara_anterior_od TEXT,
            iris_od TEXT,
            pupila_od_mm VARCHAR(10),
            pupila_od_reaccion VARCHAR(20),
            cristalino_od TEXT,
            
            -- OJO IZQUIERDO
            parpados_oi TEXT,
            conjuntiva_oi TEXT,
            cornea_oi TEXT,
            camara_anterior_oi TEXT,
            iris_oi TEXT,
            pupila_oi_mm VARCHAR(10),
            pupila_oi_reaccion VARCHAR(20),
            cristalino_oi TEXT,
            
            observaciones_generales TEXT,
            fecha_examen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Tabla 10: FONDO DE OJO
        CREATE TABLE IF NOT EXISTS fondo_ojo (
            fondo_ojo_id SERIAL PRIMARY KEY,
            ficha_id INTEGER REFERENCES fichas_clinicas(ficha_id),
            
            -- OJO DERECHO
            disco_optico_od TEXT,
            macula_od TEXT,
            vasos_od TEXT,
            retina_periferica_od TEXT,
            
            -- OJO IZQUIERDO
            disco_optico_oi TEXT,
            macula_oi TEXT,
            vasos_oi TEXT,
            retina_periferica_oi TEXT,
            
            observaciones TEXT,
            fecha_examen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Tabla 11: PRESIÓN INTRAOCULAR
        CREATE TABLE IF NOT EXISTS presion_intraocular (
            pio_id SERIAL PRIMARY KEY,
            ficha_id INTEGER REFERENCES fichas_clinicas(ficha_id),
            pio_od VARCHAR(10),
            pio_oi VARCHAR(10),
            metodo_medicion VARCHAR(50),
            hora_medicion TIME,
            observaciones TEXT,
            fecha_medicion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Tabla 12: CAMPOS VISUALES
        CREATE TABLE IF NOT EXISTS campos_visuales (
            campo_visual_id SERIAL PRIMARY KEY,
            ficha_id INTEGER REFERENCES fichas_clinicas(ficha_id),
            tipo_campo VARCHAR(50),
            resultado_od TEXT,
            resultado_oi TEXT,
            interpretacion TEXT,
            fecha_examen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Tabla 13: DIAGNÓSTICOS
        CREATE TABLE IF NOT EXISTS diagnosticos (
            diagnostico_id SERIAL PRIMARY KEY,
            ficha_id INTEGER REFERENCES fichas_clinicas(ficha_id),
            diagnostico_principal TEXT NOT NULL,
            diagnosticos_secundarios TEXT,
            cie_10_principal VARCHAR(10),
            cie_10_secundarios TEXT,
            severidad VARCHAR(20),
            observaciones TEXT,
            fecha_diagnostico TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Tabla 14: TRATAMIENTOS
        CREATE TABLE IF NOT EXISTS tratamientos (
            tratamiento_id SERIAL PRIMARY KEY,
            ficha_id INTEGER REFERENCES fichas_clinicas(ficha_id),
            medicamentos TEXT,
            tratamiento_no_farmacologico TEXT,
            recomendaciones TEXT,
            plan_seguimiento TEXT,
            proxima_cita DATE,
            urgencia_seguimiento VARCHAR(20),
            fecha_tratamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- ÍNDICES PARA OPTIMIZACIÓN
        CREATE INDEX IF NOT EXISTS idx_pacientes_numero_ficha ON pacientes_medicos(numero_ficha);
        CREATE INDEX IF NOT EXISTS idx_fichas_fecha ON fichas_clinicas(fecha_consulta);
        CREATE INDEX IF NOT EXISTS idx_fichas_numero ON fichas_clinicas(numero_consulta);
        """
        
        print("📝 Ejecutando SQL para crear tablas médicas...")
        cursor.execute(medical_tables_sql)
        conn.commit()
        
        print("✅ ¡Tablas médicas creadas exitosamente!")
        
        # Verificar tablas creadas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE '%medico%' 
            OR table_name LIKE '%ficha%' 
            OR table_name LIKE '%bio%'
            OR table_name LIKE '%fondo%'
            OR table_name LIKE '%presion%'
            OR table_name LIKE '%campo%'
            OR table_name LIKE '%diagnostico%'
            OR table_name LIKE '%tratamiento%'
            ORDER BY table_name
        """)
        
        tablas_medicas = cursor.fetchall()
        print(f"\n📊 TABLAS MÉDICAS CREADAS ({len(tablas_medicas)}):")
        for tabla in tablas_medicas:
            print(f"   ✓ {tabla[0]}")
        
        cursor.close()
        conn.close()
        
        print(f"\n🎉 ¡MÓDULO MÉDICO INSTALADO CORRECTAMENTE!")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_medical_tables()