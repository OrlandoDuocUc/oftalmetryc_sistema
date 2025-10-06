-- ===================================================================
-- SCRIPT SQL: TABLA PROVEEDORES
-- Sistema: Óptica Maipú - Gestión de Proveedores
-- Fecha: 2024
-- Descripción: Creación de tabla para gestión completa de proveedores
-- ===================================================================

-- Crear tabla proveedores
CREATE TABLE IF NOT EXISTS proveedores (
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
CREATE INDEX IF NOT EXISTS idx_proveedores_codigo ON proveedores(codigo_proveedor);
CREATE INDEX IF NOT EXISTS idx_proveedores_rut ON proveedores(rut);
CREATE INDEX IF NOT EXISTS idx_proveedores_razon_social ON proveedores(razon_social);
CREATE INDEX IF NOT EXISTS idx_proveedores_estado ON proveedores(estado);
CREATE INDEX IF NOT EXISTS idx_proveedores_fecha_registro ON proveedores(fecha_registro);

-- Crear índice para búsquedas de texto
CREATE INDEX IF NOT EXISTS idx_proveedores_busqueda_texto ON proveedores 
USING gin(to_tsvector('spanish', COALESCE(razon_social, '') || ' ' || 
                                 COALESCE(nombre_comercial, '') || ' ' || 
                                 COALESCE(rut, '')));

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
DROP TRIGGER IF EXISTS trigger_generar_codigo_proveedor ON proveedores;
CREATE TRIGGER trigger_generar_codigo_proveedor
    BEFORE INSERT ON proveedores
    FOR EACH ROW
    EXECUTE FUNCTION generar_codigo_proveedor();

-- Función para actualizar fecha de modificación
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar fecha automáticamente
DROP TRIGGER IF EXISTS trigger_actualizar_fecha_proveedor ON proveedores;
CREATE TRIGGER trigger_actualizar_fecha_proveedor
    BEFORE UPDATE ON proveedores
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

-- Insertar datos de ejemplo (opcional)
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
    'María González',
    '+56 9 8765 4321',
    'maria.gonzalez@optidistrib.cl',
    'Proveedor principal de lentes de contacto'
),
(
    'Cristales y Accesorios S.A.', 
    'CristalAcc', 
    '96.789.123-4', 
    'Calle Comercial 567, Providencia, Santiago', 
    '+56 2 2345 6789', 
    'contacto@cristalacc.cl', 
    'Cristales oftálmicos, Tratamientos, Accesorios',
    'Contado',
    0,
    3.50,
    'Juan Pérez',
    '+56 9 7654 3210',
    'juan.perez@cristalacc.cl',
    'Especialistas en cristales progresivos'
),
(
    'Monturas Premium Chile Ltda.', 
    'MonturasPremium', 
    '77.456.789-0', 
    'Av. Vitacura 2890, Vitacura, Santiago', 
    '+56 2 2456 7890', 
    'ventas@monturaspremium.cl', 
    'Monturas de lujo, Marcas internacionales',
    '60 días',
    60,
    7.50,
    'Ana Rodríguez',
    '+56 9 6543 2109',
    'ana.rodriguez@monturaspremium.cl',
    'Importador exclusivo de marcas europeas'
);

-- Comentarios descriptivos de la tabla
COMMENT ON TABLE proveedores IS 'Tabla para gestión completa de proveedores de la óptica';
COMMENT ON COLUMN proveedores.proveedor_id IS 'Identificador único del proveedor';
COMMENT ON COLUMN proveedores.codigo_proveedor IS 'Código único generado automáticamente (PROV######)';
COMMENT ON COLUMN proveedores.razon_social IS 'Razón social oficial de la empresa proveedora';
COMMENT ON COLUMN proveedores.nombre_comercial IS 'Nombre comercial o marca de fantasía';
COMMENT ON COLUMN proveedores.rut IS 'RUT de la empresa proveedora (formato: XX.XXX.XXX-X)';
COMMENT ON COLUMN proveedores.categoria_productos IS 'Categorías de productos que suministra el proveedor';
COMMENT ON COLUMN proveedores.condiciones_pago IS 'Condiciones de pago (Contado, Crédito, 30 días, etc.)';
COMMENT ON COLUMN proveedores.plazo_pago_dias IS 'Plazo de pago en días';
COMMENT ON COLUMN proveedores.descuento_volumen IS 'Porcentaje de descuento por volumen de compra';
COMMENT ON COLUMN proveedores.representante_nombre IS 'Nombre del representante comercial';
COMMENT ON COLUMN proveedores.estado IS 'Estado del proveedor (TRUE: activo, FALSE: inactivo)';

-- Verificar la creación de la tabla
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'proveedores' 
ORDER BY ordinal_position;

-- Verificar índices creados
SELECT 
    indexname,
    indexdef
FROM pg_indexes 
WHERE tablename = 'proveedores';

PRINT '✅ Tabla proveedores creada exitosamente con todos los índices y triggers';