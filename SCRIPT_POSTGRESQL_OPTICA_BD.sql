-- =====================================================================
-- SCRIPT SQL PARA POSTGRESQL - BASE DE DATOS COMPLETA
-- PROYECTO: ÓPTICA MAIPÚ - SISTEMA INTEGRADO
-- BASE DE DATOS: optica_bd
-- FECHA: 03/10/2025
-- MODO: EJECUCIÓN MANUAL
-- =====================================================================

-- PASO 1: CREAR BASE DE DATOS (Ejecutar como superusuario postgres)
-- =====================================================================
-- CREATE DATABASE optica_bd
--     WITH 
--     OWNER = postgres
--     ENCODING = 'UTF8'
--     LC_COLLATE = 'Spanish_Chile.1252'
--     LC_CTYPE = 'Spanish_Chile.1252'
--     TABLESPACE = pg_default
--     CONNECTION LIMIT = -1;

-- =====================================================================
-- PASO 2: CONECTARSE A LA BASE DE DATOS optica_bd
-- =====================================================================
-- \c optica_bd;

-- =====================================================================
-- MÓDULO COMERCIAL - TABLAS BASE (FUNCIONALES)
-- =====================================================================

-- Tabla 1: ROLES
CREATE TABLE roles (
    rol_id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- Tabla 2: USUARIOS
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

-- Tabla 3: CLIENTES
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

-- Tabla 4: PRODUCTOS
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

-- Tabla 5: VENTAS
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

-- Tabla 6: DETALLE VENTAS
CREATE TABLE detalle_ventas (
    detalle_id SERIAL PRIMARY KEY,
    venta_id INTEGER REFERENCES ventas(venta_id),
    producto_id INTEGER REFERENCES productos(producto_id),
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL
);

-- =====================================================================
-- MÓDULO MÉDICO - TABLAS OFTALMOLÓGICAS (NUEVAS)
-- =====================================================================

-- Tabla 7: PACIENTES MÉDICOS
CREATE TABLE pacientes_medicos (
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
CREATE TABLE fichas_clinicas (
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
CREATE TABLE biomicroscopia (
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
CREATE TABLE fondo_ojo (
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
CREATE TABLE presion_intraocular (
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
CREATE TABLE campos_visuales (
    campo_visual_id SERIAL PRIMARY KEY,
    ficha_id INTEGER REFERENCES fichas_clinicas(ficha_id),
    tipo_campo VARCHAR(50),
    resultado_od TEXT,
    resultado_oi TEXT,
    interpretacion TEXT,
    fecha_examen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla 13: DIAGNÓSTICOS
CREATE TABLE diagnosticos (
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
CREATE TABLE tratamientos (
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

-- =====================================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =====================================================================

-- Índices en campos de búsqueda frecuente
CREATE INDEX idx_clientes_rut ON clientes(rut);
CREATE INDEX idx_clientes_nombres ON clientes(nombres, ap_pat);
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_ventas_fecha ON ventas(fecha_venta);
CREATE INDEX idx_fichas_fecha ON fichas_clinicas(fecha_consulta);
CREATE INDEX idx_fichas_numero ON fichas_clinicas(numero_consulta);
CREATE INDEX idx_pacientes_numero_ficha ON pacientes_medicos(numero_ficha);

-- =====================================================================
-- DATOS INICIALES DEL SISTEMA
-- =====================================================================

-- Insertar roles básicos
INSERT INTO roles (nombre, descripcion) VALUES 
('Administrador', 'Acceso total al sistema'),
('Médico Oftalmólogo', 'Acceso al módulo médico y consultas'),
('Vendedor', 'Acceso al módulo comercial y ventas'),
('Recepcionista', 'Registro de pacientes y citas'),
('Supervisor', 'Acceso a reportes y supervisión');

-- Insertar usuario administrador inicial
-- NOTA: Password 'admin123' hasheado con bcrypt
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

-- Insertar categorías de productos básicas
INSERT INTO productos (nombre, descripcion, stock, precio_unitario, categoria, marca, sku) VALUES 
('Lentes de Contacto Diarios', 'Lentes de contacto desechables diarios', 100, 25000, 'Lentes de Contacto', 'Acuvue', 'LC001'),
('Armazón Metálico Clásico', 'Armazón metálico para lentes ópticos', 50, 45000, 'Armazones', 'Ray-Ban', 'ARM001'),
('Lentes Progresivos', 'Lentes progresivos premium', 25, 120000, 'Lentes Ópticos', 'Varilux', 'LP001'),
('Gotas Lubricantes', 'Lágrimas artificiales para ojo seco', 200, 8500, 'Medicamentos', 'Refresh', 'MED001'),
('Limpiador de Lentes', 'Solución limpiadora para lentes', 150, 3500, 'Accesorios', 'OptiClean', 'ACC001');

-- =====================================================================
-- COMENTARIOS IMPORTANTES PARA EL DESARROLLADOR
-- =====================================================================

/*
NOTAS IMPORTANTES:

1. BASE DE DATOS: optica_bd
2. ENCODING: UTF8
3. TODAS LAS TABLAS CREADAS CON CLAVES PRIMARIAS SERIALES
4. RELACIONES FOREIGN KEY ESTABLECIDAS
5. CAMPOS MÉDICOS MAPEADOS SEGÚN HTML EXISTENTES

CAMPOS PRINCIPALES MAPEADOS:
- Agudeza Visual: 8 campos (4 por ojo)
- Refracción: 10 campos (esfera, cilindro, eje, adición)
- Biomicroscopía: 16 campos (8 por ojo)
- Fondo de Ojo: 8 campos (4 por ojo)
- Presión Intraocular: 5 campos
- Campos Visuales: 4 campos
- Diagnósticos: 6 campos
- Tratamientos: 6 campos

CONEXIONES CLAVE:
- clientes.cliente_id ↔ pacientes_medicos.cliente_id (1:1)
- fichas_clinicas.ficha_id → todas las tablas de examen (1:1)
- usuarios.usuario_id → fichas_clinicas.usuario_id (1:N)

PASSWORD DEL ADMIN:
Username: admin
Password: admin123
Email: admin@opticamaipu.cl

DESPUÉS DE EJECUTAR ESTE SCRIPT:
1. Verificar que todas las 14 tablas se crearon
2. Verificar que los 5 roles se insertaron
3. Verificar que el usuario admin se creó
4. Verificar que los productos de ejemplo se insertaron
5. Actualizar config/settings.py con la nueva conexión
*/

-- =====================================================================
-- FIN DEL SCRIPT - TOTAL: 14 TABLAS + DATOS INICIALES
-- =====================================================================