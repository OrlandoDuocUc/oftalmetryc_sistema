#!/usr/bin/env python3
"""
RECREAR BASE DE DATOS EN RENDER
Elimina la BD actual y crea una nueva con estructura correcta
"""
import os
import psycopg2
import sys
from datetime import datetime

def recrear_bd_render():
    """Eliminar todas las tablas y recrear estructura completa"""
    
    # URL de conexión a Render
    DATABASE_URL = "postgresql://oftalmetryc_user:0WdPbRIzVrbH6xYFCye20Q7ST4e3v7Kn@dpg-d3efatffte5s73chd9r0-a.oregon-postgres.render.com/oftalmetryc_db"
    
    print("🗄️ RECREAR BASE DE DATOS EN RENDER")
    print("=" * 50)
    print(f"🕐 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Conectar a la base de datos
        print("🔗 Conectando a Render...")
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor()
        print("✅ Conexión exitosa")
        
        # PASO 1: Eliminar todas las tablas existentes
        print("\n🗑️ PASO 1: Eliminando tablas existentes...")
        
        # Obtener lista de todas las tablas
        cur.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename NOT LIKE 'pg_%' 
            AND tablename NOT LIKE 'sql_%';
        """)
        tables = cur.fetchall()
        
        if tables:
            print(f"📋 Encontradas {len(tables)} tablas:")
            for table in tables:
                print(f"   - {table[0]}")
            
            # Eliminar todas las tablas con CASCADE
            for table in tables:
                try:
                    cur.execute(f"DROP TABLE IF EXISTS {table[0]} CASCADE;")
                    print(f"❌ Eliminada: {table[0]}")
                except Exception as e:
                    print(f"⚠️ Error eliminando {table[0]}: {e}")
        else:
            print("📭 No se encontraron tablas existentes")
        
        print("✅ Limpieza completada")
        
        # PASO 2: Crear estructura completa nueva
        print("\n🏗️ PASO 2: Creando estructura nueva...")
        
        # Crear tabla de roles
        print("👥 Creando tabla: rol")
        cur.execute("""
            CREATE TABLE rol (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(50) UNIQUE NOT NULL,
                descripcion TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla de usuarios
        print("👤 Creando tabla: usuario")
        cur.execute("""
            CREATE TABLE usuario (
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
        """)
        
        # Crear tabla de pacientes
        print("🏥 Creando tabla: paciente")
        cur.execute("""
            CREATE TABLE paciente (
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
        """)
        
        # Crear tabla de consultas médicas con TODOS los campos oftalmológicos
        print("👁️ Creando tabla: consulta_medica (completa)")
        cur.execute("""
            CREATE TABLE consulta_medica (
                id SERIAL PRIMARY KEY,
                paciente_id INTEGER REFERENCES paciente(id),
                medico_id INTEGER REFERENCES usuario(id),
                fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                motivo_consulta TEXT,
                diagnostico TEXT,
                tratamiento TEXT,
                observaciones TEXT,
                
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
                urgencia BOOLEAN DEFAULT FALSE,
                
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla de productos
        print("📦 Creando tabla: producto")
        cur.execute("""
            CREATE TABLE producto (
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
        """)
        
        # Crear tabla de ventas
        print("💰 Creando tabla: sale")
        cur.execute("""
            CREATE TABLE sale (
                id SERIAL PRIMARY KEY,
                cliente_rut VARCHAR(12),
                cliente_nombre VARCHAR(100),
                total DECIMAL(10,2) NOT NULL,
                fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_id INTEGER REFERENCES usuario(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla de detalles de venta
        print("📋 Creando tabla: sale_detail")
        cur.execute("""
            CREATE TABLE sale_detail (
                id SERIAL PRIMARY KEY,
                sale_id INTEGER REFERENCES sale(id),
                producto_id INTEGER REFERENCES producto(id),
                cantidad INTEGER NOT NULL,
                precio_unitario DECIMAL(10,2) NOT NULL,
                subtotal DECIMAL(10,2) NOT NULL
            );
        """)
        
        # Crear tabla de migraciones para el futuro
        print("📊 Creando tabla: migrations")
        cur.execute("""
            CREATE TABLE migrations (
                id SERIAL PRIMARY KEY,
                version VARCHAR(50) UNIQUE NOT NULL,
                description TEXT,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                checksum VARCHAR(100)
            );
        """)
        
        print("✅ Estructura completa creada")
        
        # PASO 3: Insertar datos iniciales
        print("\n📝 PASO 3: Insertando datos iniciales...")
        
        # Insertar roles
        cur.execute("""
            INSERT INTO rol (nombre, descripcion) VALUES 
            ('Administrador', 'Acceso completo al sistema'),
            ('Médico', 'Acceso al sistema médico'),
            ('Recepcionista', 'Gestión de citas y pacientes');
        """)
        print("👥 Roles insertados")
        
        # Insertar usuarios
        cur.execute("""
            INSERT INTO usuario (username, password, nombre, rol_id) VALUES 
            ('admin', 'scrypt:32768:8:1$8vK2QqJXhYHZoNwL$64c7d6b7a5e8f3c2d9b1a4f6e7c8d5a3b2f1e6d9c8b7a5e4f3d2c1b6a9f8e7d6c5b4a3f2e1d9c8b7a6f5e4d3c2b1a', 'Administrador', 1),
            ('medico', 'scrypt:32768:8:1$8vK2QqJXhYHZoNwL$64c7d6b7a5e8f3c2d9b1a4f6e7c8d5a3b2f1e6d9c8b7a5e4f3d2c1b6a9f8e7d6c5b4a3f2e1d9c8b7a6f5e4d3c2b1a', 'Dr. Oftalmólogo', 2);
        """)
        print("👤 Usuarios insertados")
        
        # Insertar productos de ejemplo
        cur.execute("""
            INSERT INTO producto (nombre, descripcion, precio, stock, categoria) VALUES 
            ('Lentes Oftálmicos', 'Lentes correctivos estándar', 45000.00, 20, 'Lentes'),
            ('Lentes de Sol', 'Protección UV completa', 35000.00, 15, 'Lentes'),
            ('Gotas Oftálmicas', 'Lubricante ocular', 8500.00, 50, 'Medicamentos');
        """)
        print("📦 Productos de ejemplo insertados")
        
        # Registrar migración inicial
        cur.execute("""
            INSERT INTO migrations (version, description) VALUES 
            ('001_recreacion_completa', 'Recreación completa de la base de datos con estructura oftalmológica');
        """)
        print("📊 Migración registrada")
        
        print("✅ Datos iniciales insertados")
        
        # PASO 4: Verificar estructura
        print("\n🔍 PASO 4: Verificando estructura...")
        
        cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
        nuevas_tablas = cur.fetchall()
        
        print(f"✅ Base de datos recreada exitosamente con {len(nuevas_tablas)} tablas:")
        for tabla in nuevas_tablas:
            print(f"   ✓ {tabla[0]}")
        
        # Cerrar conexión
        cur.close()
        conn.close()
        
        print("\n🎉 ¡BASE DE DATOS RECREADA EXITOSAMENTE!")
        print("🔗 Lista para usar desde GitHub → Render")
        print("🌐 URL: https://oftalmetryc-sistema.onrender.com")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("⚠️  ADVERTENCIA: Este script eliminará TODOS los datos existentes")
    respuesta = input("¿Continuar? (si/no): ").lower().strip()
    
    if respuesta in ['si', 's', 'yes', 'y']:
        recrear_bd_render()
    else:
        print("❌ Operación cancelada")