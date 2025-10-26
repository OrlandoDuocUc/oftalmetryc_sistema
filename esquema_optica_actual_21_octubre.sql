-- =====================================================================
-- ESQUEMA ACTUALIZADO - OFTALMETRYC (PostgreSQL)
-- Base de datos objetivo: optica_db
-- =====================================================================

-- Nota: este script refleja la estructura vigente (17 tablas) tras las
-- ampliaciones realizadas en el módulo médico. No incluye bloques ALTER,
-- ya que las tablas se definen directamente con su versión final.

-- =====================================================================
-- MÓDULO COMERCIAL
-- =====================================================================

CREATE TABLE roles (
    rol_id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

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

CREATE TABLE detalle_ventas (
    detalle_id SERIAL PRIMARY KEY,
    venta_id INTEGER REFERENCES ventas(venta_id),
    producto_id INTEGER REFERENCES productos(producto_id),
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL
);

-- =====================================================================
-- MÓDULO MÉDICO
-- =====================================================================

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

CREATE TABLE fichas_clinicas (
    ficha_id SERIAL PRIMARY KEY,
    paciente_medico_id INTEGER REFERENCES pacientes_medicos(paciente_medico_id),
    usuario_id INTEGER REFERENCES usuarios(usuario_id),
    numero_consulta VARCHAR(20) UNIQUE NOT NULL,
    fecha_consulta TIMESTAMP NOT NULL,
    motivo_consulta TEXT,
    historia_actual TEXT,
    av_od_sc VARCHAR(20),
    av_od_cc VARCHAR(20),
    av_od_ph VARCHAR(20),
    av_od_cerca VARCHAR(20),
    av_oi_sc VARCHAR(20),
    av_oi_cc VARCHAR(20),
    av_oi_ph VARCHAR(20),
    av_oi_cerca VARCHAR(20),
    esfera_od VARCHAR(10),
    cilindro_od VARCHAR(10),
    eje_od VARCHAR(10),
    adicion_od VARCHAR(10),
    esfera_oi VARCHAR(10),
    cilindro_oi VARCHAR(10),
    eje_oi VARCHAR(10),
    adicion_oi VARCHAR(10),
    distancia_pupilar VARCHAR(10),
    tipo_lente VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'en_proceso',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE biomicroscopia (
    biomicroscopia_id SERIAL PRIMARY KEY,
    ficha_id INTEGER REFERENCES fichas_clinicas(ficha_id) ON DELETE CASCADE,
    parpados_od TEXT,
    conjuntiva_od TEXT,
    cornea_od TEXT,
    camara_anterior_od TEXT,
    iris_od TEXT,
    pupila_od_mm VARCHAR(10),
    pupila_od_reaccion VARCHAR(20),
    cristalino_od TEXT,
    pupila_desc_od TEXT,
    pestanas_od TEXT,
    conjuntiva_bulbar_od TEXT,
    conjuntiva_tarsal_od TEXT,
    orbita_od TEXT,
    pliegue_semilunar_od TEXT,
    caruncula_od TEXT,
    conductos_lagrimales_od TEXT,
    parpado_superior_od TEXT,
    parpado_inferior_od TEXT,
    parpados_oi TEXT,
    conjuntiva_oi TEXT,
    cornea_oi TEXT,
    camara_anterior_oi TEXT,
    iris_oi TEXT,
    pupila_oi_mm VARCHAR(10),
    pupila_oi_reaccion VARCHAR(20),
    cristalino_oi TEXT,
    pupila_desc_oi TEXT,
    pestanas_oi TEXT,
    conjuntiva_bulbar_oi TEXT,
    conjuntiva_tarsal_oi TEXT,
    orbita_oi TEXT,
    pliegue_semilunar_oi TEXT,
    caruncula_oi TEXT,
    conductos_lagrimales_oi TEXT,
    parpado_superior_oi TEXT,
    parpado_inferior_oi TEXT,
    observaciones_generales TEXT,
    otros_detalles TEXT,
    fecha_examen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reflejos_pupilares (
    reflejo_id SERIAL PRIMARY KEY,
    ficha_id INTEGER NOT NULL REFERENCES fichas_clinicas(ficha_id) ON DELETE CASCADE,
    acomodativo_uno TEXT,
    fotomotor_uno TEXT,
    consensual_uno TEXT,
    acomodativo_dos TEXT,
    fotomotor_dos TEXT,
    consensual_dos TEXT,
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_reflejos_pupilares_ficha ON reflejos_pupilares(ficha_id);

CREATE TABLE fondo_ojo (
    fondo_ojo_id SERIAL PRIMARY KEY,
    ficha_id INTEGER REFERENCES fichas_clinicas(ficha_id) ON DELETE CASCADE,
    disco_optico_od TEXT,
    macula_od TEXT,
    vasos_od TEXT,
    retina_periferica_od TEXT,
    av_temp_sup_od TEXT,
    av_temp_inf_od TEXT,
    av_nasal_sup_od TEXT,
    av_nasal_inf_od TEXT,
    retina_od TEXT,
    excavacion_od TEXT,
    papila_detalle_od TEXT,
    fijacion_od TEXT,
    color_od TEXT,
    borde_od TEXT,
    disco_optico_oi TEXT,
    macula_oi TEXT,
    vasos_oi TEXT,
    retina_periferica_oi TEXT,
    av_temp_sup_oi TEXT,
    av_temp_inf_oi TEXT,
    av_nasal_sup_oi TEXT,
    av_nasal_inf_oi TEXT,
    retina_oi TEXT,
    excavacion_oi TEXT,
    papila_detalle_oi TEXT,
    fijacion_oi TEXT,
    color_oi TEXT,
    borde_oi TEXT,
    observaciones TEXT,
    otros_detalles TEXT,
    fecha_examen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE presion_intraocular (
    pio_id SERIAL PRIMARY KEY,
    ficha_id INTEGER REFERENCES fichas_clinicas(ficha_id) ON DELETE CASCADE,
    pio_od VARCHAR(10),
    pio_oi VARCHAR(10),
    metodo_medicion VARCHAR(50),
    hora_medicion TIME,
    observaciones TEXT,
    fecha_medicion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE campos_visuales (
    campo_visual_id SERIAL PRIMARY KEY,
    ficha_id INTEGER REFERENCES fichas_clinicas(ficha_id) ON DELETE CASCADE,
    tipo_campo VARCHAR(50),
    resultado_od TEXT,
    resultado_oi TEXT,
    interpretacion TEXT,
    fecha_examen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE diagnosticos (
    diagnostico_id SERIAL PRIMARY KEY,
    ficha_id INTEGER REFERENCES fichas_clinicas(ficha_id) ON DELETE CASCADE,
    diagnostico_principal TEXT NOT NULL,
    diagnosticos_secundarios TEXT,
    cie_10_principal VARCHAR(10),
    cie_10_secundarios TEXT,
    severidad VARCHAR(20),
    observaciones TEXT,
    fecha_diagnostico TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tratamientos (
    tratamiento_id SERIAL PRIMARY KEY,
    ficha_id INTEGER REFERENCES fichas_clinicas(ficha_id) ON DELETE CASCADE,
    medicamentos TEXT,
    tratamiento_no_farmacologico TEXT,
    recomendaciones TEXT,
    plan_seguimiento TEXT,
    proxima_cita DATE,
    urgencia_seguimiento VARCHAR(20),
    fecha_tratamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE parametros_clinicos (
    parametro_id SERIAL PRIMARY KEY,
    ficha_id INTEGER NOT NULL REFERENCES fichas_clinicas(ficha_id) ON DELETE CASCADE,
    presion_sistolica VARCHAR(10),
    presion_diastolica VARCHAR(10),
    saturacion_o2 VARCHAR(10),
    glucosa VARCHAR(20),
    trigliceridos VARCHAR(20),
    ttp VARCHAR(20),
    atp VARCHAR(20),
    colesterol VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_parametros_clinicos_ficha ON parametros_clinicos(ficha_id);

-- =====================================================================
-- MÓDULO PROVEEDORES
-- =====================================================================

CREATE TABLE proveedores (
    proveedor_id SERIAL PRIMARY KEY,
    codigo_proveedor VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(255) NOT NULL,
    nombre_comercial VARCHAR(255),
    rut VARCHAR(12) UNIQUE NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(100),
    sitio_web VARCHAR(255),
    categoria_productos TEXT,
    condiciones_pago VARCHAR(50) DEFAULT 'Contado',
    plazo_pago_dias INTEGER DEFAULT 0,
    descuento_volumen DECIMAL(5,2) DEFAULT 0.00,
    representante_nombre VARCHAR(255),
    representante_telefono VARCHAR(20),
    representante_email VARCHAR(100),
    observaciones TEXT,
    estado BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_descuento_volumen CHECK (descuento_volumen BETWEEN 0 AND 100),
    CONSTRAINT chk_plazo_pago CHECK (plazo_pago_dias >= 0),
    CONSTRAINT chk_email_formato CHECK (email IS NULL OR email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_representante_email_formato CHECK (representante_email IS NULL OR representante_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_proveedores_codigo ON proveedores(codigo_proveedor);
CREATE INDEX idx_proveedores_rut ON proveedores(rut);
CREATE INDEX idx_proveedores_razon_social ON proveedores(razon_social);
CREATE INDEX idx_proveedores_estado ON proveedores(estado);
CREATE INDEX idx_proveedores_fecha_registro ON proveedores(fecha_registro);

-- =====================================================================
-- ÍNDICES TRANSVERSALES SUGERIDOS
-- =====================================================================

CREATE INDEX idx_clientes_rut           ON clientes(rut);
CREATE INDEX idx_clientes_nombres       ON clientes(nombres, ap_pat);
CREATE INDEX idx_usuarios_username      ON usuarios(username);
CREATE INDEX idx_ventas_fecha           ON ventas(fecha_venta);
CREATE INDEX idx_fichas_fecha           ON fichas_clinicas(fecha_consulta);
CREATE INDEX idx_fichas_numero          ON fichas_clinicas(numero_consulta);
CREATE INDEX idx_pacientes_numero_ficha ON pacientes_medicos(numero_ficha);

-- =====================================================================
-- DATOS SEMILLA OPCIONALES
-- =====================================================================

INSERT INTO roles (nombre, descripcion) VALUES
('Administrador', 'Acceso total al sistema'),
('Médico Oftalmólogo', 'Acceso al módulo médico y consultas'),
('Vendedor', 'Acceso al módulo comercial y ventas'),
('Recepcionista', 'Registro de pacientes y citas'),
('Supervisor', 'Acceso a reportes y supervisión');

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

INSERT INTO productos (nombre, descripcion, stock, precio_unitario, categoria, marca, sku) VALUES
('Lentes de Contacto Diarios', 'Lentes de contacto desechables diarios', 100, 25000, 'Lentes de Contacto', 'Acuvue', 'LC001'),
('Armazón Metálico Clásico', 'Armazón metálico para lentes ópticos', 50, 45000, 'Armazones', 'Ray-Ban', 'ARM001'),
('Lentes Progresivos', 'Lentes progresivos premium', 25, 120000, 'Lentes Ópticos', 'Varilux', 'LP001'),
('Gotas Lubricantes', 'Lágrimas artificiales para ojo seco', 200, 8500, 'Medicamentos', 'Refresh', 'MED001'),
('Limpiador de Lentes', 'Solución limpiadora para lentes', 150, 3500, 'Accesorios', 'OptiClean', 'ACC001');

-- =====================================================================
-- FIN DEL ESQUEMA CONSOLIDADO
-- =====================================================================
