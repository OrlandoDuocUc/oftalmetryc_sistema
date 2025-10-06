-- ===================================================================
-- SCRIPT SQL: TABLA PROVEEDORES - ÓPTICA OFTALMETRIK
-- Base de Datos: PostgreSQL
-- Fecha: Octubre 2024
-- Descripción: Creación de tabla para gestión completa de proveedores
-- ===================================================================

-- Crear tabla proveedores
CREATE TABLE proveedores (
    -- Identificación única
    proveedor_id SERIAL PRIMARY KEY,
    codigo_proveedor VARCHAR(20) UNIQUE NOT NULL,
    
    -- Información de la empresa
    razon_social VARCHAR(255) NOT NULL,
    nombre_comercial VARCHAR(255),
    rut VARCHAR(12) UNIQUE NOT NULL,
    
    -- Información de contacto
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(100),
    sitio_web VARCHAR(255),
    
    -- Información comercial
    categoria_productos TEXT,
    condiciones_pago VARCHAR(50) DEFAULT 'Contado',
    plazo_pago_dias INTEGER DEFAULT 0,
    descuento_volumen DECIMAL(5,2) DEFAULT 0.00,
    
    -- Representante comercial
    representante_nombre VARCHAR(255),
    representante_telefono VARCHAR(20),
    representante_email VARCHAR(100),
    
    -- Información adicional
    observaciones TEXT,
    
    -- Control de estado y fechas
    estado BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Validaciones
    CONSTRAINT chk_descuento_volumen CHECK (descuento_volumen >= 0 AND descuento_volumen <= 100),
    CONSTRAINT chk_plazo_pago CHECK (plazo_pago_dias >= 0),
    CONSTRAINT chk_email_formato CHECK (email IS NULL OR email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_representante_email_formato CHECK (representante_email IS NULL OR representante_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Crear índices para optimizar consultas
CREATE INDEX idx_proveedores_codigo ON proveedores(codigo_proveedor);
CREATE INDEX idx_proveedores_rut ON proveedores(rut);
CREATE INDEX idx_proveedores_razon_social ON proveedores(razon_social);
CREATE INDEX idx_proveedores_estado ON proveedores(estado);
CREATE INDEX idx_proveedores_fecha_registro ON proveedores(fecha_registro);

-- Función para generar código de proveedor automáticamente
CREATE OR REPLACE FUNCTION generar_codigo_proveedor() 
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.codigo_proveedor IS NULL OR NEW.codigo_proveedor = '' THEN
        NEW.codigo_proveedor := 'PROV' || LPAD(NEW.proveedor_id::text, 6, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para generar código automáticamente
CREATE TRIGGER trigger_generar_codigo_proveedor
    BEFORE INSERT ON proveedores
    FOR EACH ROW
    EXECUTE FUNCTION generar_codigo_proveedor();

-- Función para actualizar fecha de modificación
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion_proveedor() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar fecha automáticamente
CREATE TRIGGER trigger_actualizar_fecha_proveedor
    BEFORE UPDATE ON proveedores
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion_proveedor();

-- Insertar proveedores de ejemplo
INSERT INTO proveedores (
    razon_social, 
    nombre_comercial, 
    rut, 
    direccion, 
    telefono, 
    email, 
    categoria_productos,
    condiciones_pago,
    plazo_pago_dias,
    descuento_volumen,
    representante_nombre,
    representante_telefono,
    representante_email,
    observaciones
) VALUES 
-- Proveedor 1: Distribuidora principal
(
    'Óptica Distribuidora Ltda.', 
    'OptiDistrib', 
    '76.123.456-K', 
    'Av. Las Condes 1234, Las Condes, Santiago', 
    '+56 2 2234 5678', 
    'ventas@optidistrib.cl', 
    'Lentes de contacto, Monturas, Cristales',
    'Crédito',
    30,
    5.00,
    'María González Pérez',
    '+56 9 8765 4321',
    'maria.gonzalez@optidistrib.cl',
    'Proveedor principal de lentes de contacto. Descuentos especiales por volumen.'
),
-- Proveedor 2: Especialista en cristales
(
    'Cristales y Accesorios S.A.', 
    'CristalAcc', 
    '96.789.123-4', 
    'Calle Comercial 567, Providencia, Santiago', 
    '+56 2 2345 6789', 
    'contacto@cristalacc.cl', 
    'Cristales oftálmicos, Tratamientos antirreflex, Accesorios',
    'Contado',
    0,
    3.50,
    'Juan Carlos Pérez',
    '+56 9 7654 3210',
    'juan.perez@cristalacc.cl',
    'Especialistas en cristales progresivos y tratamientos de alta gama.'
),
-- Proveedor 3: Monturas premium
(
    'Monturas Premium Chile Ltda.', 
    'MonturasPremium', 
    '77.456.789-0', 
    'Av. Vitacura 2890, Vitacura, Santiago', 
    '+56 2 2456 7890', 
    'ventas@monturaspremium.cl', 
    'Monturas de lujo, Marcas internacionales, Colecciones exclusivas',
    '60 días',
    60,
    7.50,
    'Ana María Rodríguez',
    '+56 9 6543 2109',
    'ana.rodriguez@monturaspremium.cl',
    'Importador exclusivo de marcas europeas premium. Excelente servicio post-venta.'
),
-- Proveedor 4: Lentes de contacto
(
    'Lentes de Contacto Express S.A.', 
    'LentExpress', 
    '78.654.321-9', 
    'Av. Apoquindo 4500, Las Condes, Santiago', 
    '+56 2 2567 8901', 
    'pedidos@lentexpress.cl', 
    'Lentes de contacto diarios, Lentes tóricas, Soluciones',
    'Crédito',
    45,
    4.25,
    'Carlos Alberto Silva',
    '+56 9 5432 1098',
    'carlos.silva@lentexpress.cl',
    'Entrega rápida de lentes de contacto. Stock permanente de las principales marcas.'
),
-- Proveedor 5: Accesorios y estuches
(
    'Accesorios Ópticos del Sur Ltda.', 
    'AccesoriosÓpticos', 
    '79.987.654-3', 
    'Av. Irarrázaval 1234, Ñuñoa, Santiago', 
    '+56 2 2678 9012', 
    'ventas@accesoriosopticos.cl', 
    'Estuches, Paños de limpieza, Cordones, Accesorios',
    'Contado',
    0,
    2.00,
    'Patricia Morales López',
    '+56 9 4321 0987',
    'patricia.morales@accesoriosopticos.cl',
    'Amplia variedad de accesorios para ópticas. Precios competitivos.'
);

-- Verificar que la tabla se creó correctamente
SELECT COUNT(*) as total_proveedores FROM proveedores;

-- Mostrar algunos proveedores de ejemplo
SELECT 
    codigo_proveedor,
    razon_social,
    nombre_comercial,
    rut,
    email,
    condiciones_pago,
    estado
FROM proveedores 
ORDER BY fecha_registro 
LIMIT 3;

-- Verificar estructura de la tabla con SQL estándar
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'proveedores' 
ORDER BY ordinal_position;

-- Comentario final
SELECT 'Tabla proveedores creada exitosamente en base de datos optica_db' as resultado;