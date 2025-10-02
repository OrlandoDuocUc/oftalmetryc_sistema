-- ==============================================================
-- ADAPTACIÓN DE TABLAS MÉDICAS PARA ECUADOR - OFTALMETRYC
-- ==============================================================

-- Actualizar tabla de pacientes para Ecuador
ALTER TABLE pacientes 
    RENAME COLUMN rut TO cedula;

-- Cambiar constraint único
ALTER TABLE pacientes 
    DROP CONSTRAINT pacientes_rut_unique;

ALTER TABLE pacientes 
    ADD CONSTRAINT pacientes_cedula_unique UNIQUE (cedula);

-- Actualizar comentarios para Ecuador
ALTER TABLE pacientes 
    ALTER COLUMN cedula TYPE VARCHAR(13); -- Cédula ecuatoriana tiene 10 dígitos

COMMENT ON COLUMN pacientes.cedula IS 'Cédula de ciudadanía ecuatoriana (10 dígitos)';
COMMENT ON COLUMN pacientes.telefono IS 'Número telefónico ecuatoriano (formato: 09XXXXXXXX o 02XXXXXXX)';

-- Actualizar índices
DROP INDEX IF EXISTS idx_pacientes_rut;
CREATE INDEX idx_pacientes_cedula ON pacientes(cedula);

-- Agregar validaciones para Ecuador
ALTER TABLE pacientes 
    ADD CONSTRAINT chk_cedula_ecuador 
    CHECK (cedula ~ '^[0-9]{10}$');

ALTER TABLE pacientes 
    ADD CONSTRAINT chk_telefono_ecuador 
    CHECK (telefono ~ '^(09|02|03|04|05|06|07)[0-9]{7,8}$');

-- Comentarios actualizados para Ecuador
COMMENT ON TABLE pacientes IS 'Información personal y de contacto de pacientes en Ecuador';
COMMENT ON COLUMN pacientes.direccion IS 'Dirección completa en Ecuador (provincia, cantón, parroquia)';
COMMENT ON COLUMN pacientes.contacto_emergencia IS 'Persona de contacto de emergencia en Ecuador';