#!/usr/bin/env python3
# SCRIPT SIMPLE Y DIRECTO - CREAR BD DESDE CERO
import os
from sqlalchemy import create_engine, text

def get_database_url():
    return os.getenv('DATABASE_URL', "postgresql://postgres:password@localhost:5432/oftalmetryc")

def main():
    print("🏥 CREANDO BASE DE DATOS SIMPLE...")
    
    try:
        engine = create_engine(get_database_url())
        
        # Crear tablas una por una
        with engine.connect() as conn:
            with conn.begin():
                # 1. Tabla ROL
                conn.execute(text("""
                CREATE TABLE IF NOT EXISTS rol (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(50) UNIQUE NOT NULL,
                    descripcion TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """))
                print("✅ Tabla rol creada")
                
                # 2. Tabla USUARIO  
                conn.execute(text("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(100),
                    nombre VARCHAR(100),
                    apellido VARCHAR(100),
                    activo BOOLEAN DEFAULT TRUE,
                    rol_id INTEGER REFERENCES rol(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """))
                print("✅ Tabla usuario creada")
                
                # 3. Tabla PACIENTES COMPLETA
                conn.execute(text("""
                CREATE TABLE IF NOT EXISTS pacientes (
                    id SERIAL PRIMARY KEY,
                    rut VARCHAR(12),
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
                """))
                print("✅ Tabla pacientes creada")
                
                # 4. Tabla CONSULTAS MEDICAS
                conn.execute(text("""
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
                """))
                print("✅ Tabla consultas_medicas creada")
                
                # 5. Tabla EXAMENES BASICOS EXPANDIDA
                conn.execute(text("""
                CREATE TABLE IF NOT EXISTS examenes_basicos (
                    id SERIAL PRIMARY KEY,
                    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
                    
                    -- Agudeza Visual Original
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
                    
                    -- NUEVOS CAMPOS FICHA CLINICA
                    av_distancia_od VARCHAR(10),
                    av_distancia_oi VARCHAR(10),
                    av_c_c_od VARCHAR(10),
                    av_c_c_oi VARCHAR(10),
                    av_s_c_od VARCHAR(10),
                    av_s_c_oi VARCHAR(10),
                    av_ph_od VARCHAR(10),
                    av_ph_oi VARCHAR(10),
                    av_proxima_od VARCHAR(10),
                    av_proxima_oi VARCHAR(10),
                    av_ao_distancia VARCHAR(10),
                    av_ao_proxima VARCHAR(10),
                    dominante_od VARCHAR(10),
                    dominante_oi VARCHAR(10),
                    av_otros TEXT,
                    
                    -- Lensometría
                    lensometria_od VARCHAR(50),
                    lensometria_oi VARCHAR(50),
                    
                    -- Queratometría
                    queratometria_od VARCHAR(50),
                    queratometria_oi VARCHAR(50),
                    
                    -- Autorefractor
                    ar_esf_od VARCHAR(10),
                    ar_cyl_od VARCHAR(10),
                    ar_eje_od VARCHAR(10),
                    ar_av_od VARCHAR(10),
                    ar_esf_oi VARCHAR(10),
                    ar_cyl_oi VARCHAR(10),
                    ar_eje_oi VARCHAR(10),
                    ar_av_oi VARCHAR(10),
                    
                    -- RX Final
                    rx_esf_od VARCHAR(10),
                    rx_cyl_od VARCHAR(10),
                    rx_eje_od VARCHAR(10),
                    rx_avl_od VARCHAR(10),
                    rx_avc_od VARCHAR(10),
                    rx_dp_od VARCHAR(10),
                    rx_np_od VARCHAR(10),
                    rx_add_od VARCHAR(10),
                    rx_alt_od VARCHAR(10),
                    rx_ao_od VARCHAR(10),
                    rx_esf_oi VARCHAR(10),
                    rx_cyl_oi VARCHAR(10),
                    rx_eje_oi VARCHAR(10),
                    rx_avl_oi VARCHAR(10),
                    rx_avc_oi VARCHAR(10),
                    rx_dp_oi VARCHAR(10),
                    rx_np_oi VARCHAR(10),
                    rx_add_oi VARCHAR(10),
                    rx_alt_oi VARCHAR(10),
                    rx_ao_oi VARCHAR(10),
                    
                    -- Lentes de Contacto
                    lc_poder_od VARCHAR(10),
                    lc_curva_base_od VARCHAR(10),
                    lc_diametro_od VARCHAR(10),
                    lc_material_od VARCHAR(50),
                    lc_poder_oi VARCHAR(10),
                    lc_curva_base_oi VARCHAR(10),
                    lc_diametro_oi VARCHAR(10),
                    lc_material_oi VARCHAR(50),
                    
                    -- Test Adicionales
                    test_ishihara VARCHAR(50),
                    presion_intraocular_od VARCHAR(20),
                    presion_intraocular_oi VARCHAR(20),
                    
                    observaciones TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """))
                print("✅ Tabla examenes_basicos expandida creada")
                
                # 6. Insertar datos básicos
                conn.execute(text("""
                INSERT INTO rol (nombre, descripcion) 
                SELECT 'admin', 'Administrador del sistema'
                WHERE NOT EXISTS (SELECT 1 FROM rol WHERE nombre = 'admin');
                """))
                
                conn.execute(text("""
                INSERT INTO usuario (username, password, nombre, ap_pat, rol_id) 
                SELECT 'admin', 'admin123', 'Administrador', 'Sistema', 1
                WHERE NOT EXISTS (SELECT 1 FROM usuario WHERE username = 'admin');
                """))
                
                print("✅ Datos básicos insertados")
                
                # 7. Crear índices
                conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_pacientes_ci ON pacientes(ci);
                CREATE INDEX IF NOT EXISTS idx_pacientes_rut ON pacientes(rut);
                CREATE INDEX IF NOT EXISTS idx_consultas_paciente ON consultas_medicas(paciente_id);
                CREATE INDEX IF NOT EXISTS idx_examenes_consulta ON examenes_basicos(consulta_id);
                """))
                print("✅ Índices creados")
        
        # Verificar creación
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name, 
                       (SELECT count(*) FROM information_schema.columns 
                        WHERE table_name = t.table_name) as column_count
                FROM information_schema.tables t
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """))
            
            tablas = result.fetchall()
            print("\n📊 ESTRUCTURA CREADA:")
            print("=" * 40)
            
            for tabla in tablas:
                print(f"📄 {tabla[0]:20} | {tabla[1]:3} campos")
            
            print("=" * 40)
            print(f"📈 TOTAL: {len(tablas)} tablas")
        
        print("\n🎉 ¡BASE DE DATOS CREADA EXITOSAMENTE!")
        print("✅ Sistema listo para usar")
        print("✅ Usuario: admin | Password: admin123")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
        
    return True

if __name__ == "__main__":
    main()