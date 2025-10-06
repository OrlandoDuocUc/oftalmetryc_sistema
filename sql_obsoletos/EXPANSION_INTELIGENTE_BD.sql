-- ===============================================================================
-- SCRIPT INTELIGENTE - AGREGAR SOLO CAMPOS FALTANTES
-- Sistema: Oftalmetryc - Expansión Ficha Clínica
-- Autor: Orlando Rodriguez
-- Fecha: 2 de octubre de 2025
-- ===============================================================================

-- ESTRATEGIA: Agregar campos faltantes a tablas existentes (MÁS FÁCIL)

BEGIN;

-- ===============================================================================
-- PASO 1: EXPANDIR TABLA PACIENTES (AGREGAR CAMPOS ECUADOR)
-- ===============================================================================

-- Agregar campos que faltan para Ecuador
ALTER TABLE pacientes 
ADD COLUMN IF NOT EXISTS ci VARCHAR(20);  -- Cédula Ecuador (alternativa a RUT)

ALTER TABLE pacientes 
ADD COLUMN IF NOT EXISTS nombres VARCHAR(100);  -- Separar nombres

ALTER TABLE pacientes 
ADD COLUMN IF NOT EXISTS apellidos VARCHAR(100);  -- Separar apellidos

ALTER TABLE pacientes 
ADD COLUMN IF NOT EXISTS edad INTEGER;  -- Edad calculada

ALTER TABLE pacientes 
ADD COLUMN IF NOT EXISTS genero VARCHAR(10);  -- M/F/Otro

ALTER TABLE pacientes 
ADD COLUMN IF NOT EXISTS hobby VARCHAR(200);  -- Hobby del paciente

ALTER TABLE pacientes 
ADD COLUMN IF NOT EXISTS estado VARCHAR(20) DEFAULT 'Activo';  -- Estado del paciente

ALTER TABLE pacientes 
ADD COLUMN IF NOT EXISTS observaciones_generales TEXT;  -- Observaciones generales

-- Actualizar índices
CREATE INDEX IF NOT EXISTS idx_pacientes_ci ON pacientes(ci);
CREATE INDEX IF NOT EXISTS idx_pacientes_nombres ON pacientes(nombres, apellidos);

-- ===============================================================================
-- PASO 2: EXPANDIR TABLA CONSULTAS_MEDICAS (AGREGAR CAMPOS FICHA CLÍNICA)
-- ===============================================================================

-- Agregar campos específicos de ficha clínica
ALTER TABLE consultas_medicas 
ADD COLUMN IF NOT EXISTS ultimo_control_visual DATE;

ALTER TABLE consultas_medicas 
ADD COLUMN IF NOT EXISTS usa_lentes BOOLEAN DEFAULT FALSE;

ALTER TABLE consultas_medicas 
ADD COLUMN IF NOT EXISTS ultimo_cambio_lentes DATE;

ALTER TABLE consultas_medicas 
ADD COLUMN IF NOT EXISTS firma_responsable VARCHAR(100);

ALTER TABLE consultas_medicas 
ADD COLUMN IF NOT EXISTS conforme_evaluado BOOLEAN DEFAULT TRUE;

-- ===============================================================================
-- PASO 3: EXPANDIR TABLA EXAMENES_BASICOS (AGREGAR CAMPOS OFTALMOLÓGICOS)
-- ===============================================================================

-- SECCIÓN: AGUDEZA VISUAL EXPANDIDA
ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS av_distancia_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS av_distancia_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS av_c_c_od VARCHAR(10);  -- Sin corrección

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS av_c_c_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS av_s_c_od VARCHAR(10);  -- Con corrección

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS av_s_c_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS av_ph_od VARCHAR(10);   -- Pin Hole

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS av_ph_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS av_proxima_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS av_proxima_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS av_ao_distancia VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS av_ao_proxima VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS dominante_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS dominante_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS av_otros TEXT;

-- SECCIÓN: LENSOMETRÍA
ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS lensometria_od VARCHAR(50);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS lensometria_oi VARCHAR(50);

-- SECCIÓN: QUERATOMETRÍA
ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS queratometria_od VARCHAR(50);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS queratometria_oi VARCHAR(50);

-- SECCIÓN: AUTOREFRACTOR EXPANDIDO
ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS ar_esf_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS ar_cyl_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS ar_eje_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS ar_av_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS ar_esf_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS ar_cyl_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS ar_eje_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS ar_av_oi VARCHAR(10);

-- SECCIÓN: SUBJETIVO EXPANDIDO
ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS sub_esf_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS sub_cyl_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS sub_eje_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS sub_av_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS sub_esf_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS sub_cyl_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS sub_eje_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS sub_av_oi VARCHAR(10);

-- SECCIÓN: RX FINAL COMPLETO
ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_esf_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_cyl_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_eje_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_avl_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_avc_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_dp_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_np_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_add_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_alt_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_ao_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_esf_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_cyl_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_eje_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_avl_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_avc_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_dp_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_np_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_add_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_alt_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS rx_ao_oi VARCHAR(10);

-- SECCIÓN: LENTES DE CONTACTO
ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS lc_poder_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS lc_curva_base_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS lc_diametro_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS lc_adicion_od VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS lc_diseno_od VARCHAR(50);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS lc_material_od VARCHAR(50);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS lc_poder_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS lc_curva_base_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS lc_diametro_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS lc_adicion_oi VARCHAR(10);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS lc_diseno_oi VARCHAR(50);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS lc_material_oi VARCHAR(50);

-- SECCIÓN: TEST ADICIONALES EXPANDIDOS
ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS hirschberg_od INTEGER CHECK (hirschberg_od IN (0, 15, 30, 45));

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS hirschberg_oi INTEGER CHECK (hirschberg_oi IN (0, 15, 30, 45));

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS campimetria_t100_od VARCHAR(20);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS campimetria_n60_od VARCHAR(20);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS campimetria_s60_od VARCHAR(20);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS campimetria_i70_od VARCHAR(20);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS campimetria_t100_oi VARCHAR(20);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS campimetria_n60_oi VARCHAR(20);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS campimetria_s60_oi VARCHAR(20);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS campimetria_i70_oi VARCHAR(20);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS cover_test_pfc VARCHAR(50);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS cover_test_foria VARCHAR(50);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS cover_test_tropia VARCHAR(50);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS cover_test_mag_desviacion VARCHAR(50);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS mov_oculares VARCHAR(100);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS luces_worth_lejos VARCHAR(50);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS luces_worth_cerca VARCHAR(50);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS test_ishihara VARCHAR(50);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS presion_intraocular_od VARCHAR(20);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS presion_intraocular_oi VARCHAR(20);

ALTER TABLE examenes_basicos 
ADD COLUMN IF NOT EXISTS test_adicionales_otros TEXT;

-- ===============================================================================
-- PASO 4: EXPANDIR BIOMICROSCOPÍA (TABLA EXISTENTE)
-- ===============================================================================

-- Verificar si existe la tabla biomicroscopia y expandirla
-- (Basándome en tu estructura existente)

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_cornea_od TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_cornea_oi TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_cristalino_od TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_cristalino_oi TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_pupila_od TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_pupila_oi TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_pestanas_od TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_pestanas_oi TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_conjuntiva_bulbar_od TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_conjuntiva_bulbar_oi TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_conjuntiva_tarsal_od TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_conjuntiva_tarsal_oi TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_esclera_od TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_esclera_oi TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_pliegue_semilunar_od TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_pliegue_semilunar_oi TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_caruncula_od TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_caruncula_oi TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_conductos_lagrimales_od TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_conductos_lagrimales_oi TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_parpado_superior_od TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_parpado_superior_oi TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_camara_anterior_od TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_camara_anterior_oi TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_parpado_inferior_od TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_parpado_inferior_oi TEXT;

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS biomic_otros TEXT;

-- REFLEJOS PUPILARES
ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS reflejo_acomodativo_miosis_od VARCHAR(50);

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS reflejo_acomodativo_convergencia_od VARCHAR(50);

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS reflejo_acomodativo_midriasis_od VARCHAR(50);

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS reflejo_acomodativo_miosis_oi VARCHAR(50);

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS reflejo_acomodativo_convergencia_oi VARCHAR(50);

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS reflejo_acomodativo_midriasis_oi VARCHAR(50);

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS reflejo_fotomotor_miosis_od VARCHAR(50);

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS reflejo_fotomotor_midriasis_od VARCHAR(50);

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS reflejo_consensual_od VARCHAR(50);

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS reflejo_fotomotor_miosis_oi VARCHAR(50);

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS reflejo_fotomotor_midriasis_oi VARCHAR(50);

ALTER TABLE biomicroscopia 
ADD COLUMN IF NOT EXISTS reflejo_consensual_oi VARCHAR(50);

-- ===============================================================================
-- PASO 5: EXPANDIR OFTALMOSCOPIA (FONDO DE OJO)
-- ===============================================================================

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_av_temp_sup_od TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_av_temp_inf_od TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_av_nasal_sup_od TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_av_nasal_inf_od TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_retina_od TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_macula_od TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_excavacion_od TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_vasos_od TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_papila_od TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_fijacion_od TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_color_od TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_borde_od TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_av_temp_sup_oi TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_av_temp_inf_oi TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_av_nasal_sup_oi TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_av_nasal_inf_oi TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_retina_oi TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_macula_oi TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_excavacion_oi TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_vasos_oi TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_papila_oi TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_fijacion_oi TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_color_oi TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_borde_oi TEXT;

ALTER TABLE oftalmoscopia 
ADD COLUMN IF NOT EXISTS fondo_ojo_otros TEXT;

-- ===============================================================================
-- PASO 6: AGREGAR CAMPOS MÉDICOS ADICIONALES
-- ===============================================================================

-- Agregar tabla para datos médicos adicionales si no existe
CREATE TABLE IF NOT EXISTS datos_medicos_adicionales (
    id BIGSERIAL PRIMARY KEY,
    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
    presion_arterial_sistolica INTEGER,
    presion_arterial_diastolica INTEGER,
    saturacion_o2 INTEGER,
    glucosa VARCHAR(20),
    trigliceridos VARCHAR(20),
    atp VARCHAR(20),
    colesterol VARCHAR(20),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================================================================
-- PASO 7: CREAR FUNCIÓN PARA CALCULAR EDAD AUTOMÁTICAMENTE
-- ===============================================================================

-- Función para actualizar edad automáticamente
CREATE OR REPLACE FUNCTION actualizar_edad_paciente()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.fecha_nacimiento IS NOT NULL THEN
        NEW.edad = EXTRACT(YEAR FROM age(NEW.fecha_nacimiento));
    END IF;
    
    -- Si se proporciona CI, copiarlo también a nombres/apellidos si están vacíos
    IF NEW.ci IS NOT NULL AND NEW.ci != '' THEN
        -- Lógica adicional para manejar CI Ecuador
        NULL; -- Placeholder para lógica futura
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger para pacientes
DROP TRIGGER IF EXISTS trg_actualizar_edad_paciente ON pacientes;
CREATE TRIGGER trg_actualizar_edad_paciente
    BEFORE INSERT OR UPDATE ON pacientes
    FOR EACH ROW EXECUTE FUNCTION actualizar_edad_paciente();

-- ===============================================================================
-- PASO 8: MIGRAR DATOS EXISTENTES
-- ===============================================================================

-- Migrar nombres y apellidos existentes
UPDATE pacientes 
SET nombres = nombre, apellidos = apellido 
WHERE nombres IS NULL OR apellidos IS NULL;

-- Calcular edad para pacientes existentes
UPDATE pacientes 
SET edad = EXTRACT(YEAR FROM age(fecha_nacimiento))
WHERE edad IS NULL AND fecha_nacimiento IS NOT NULL;

-- Establecer estado por defecto
UPDATE pacientes 
SET estado = 'Activo' 
WHERE estado IS NULL;

-- ===============================================================================
-- PASO 9: OPTIMIZACIÓN - ÍNDICES ADICIONALES
-- ===============================================================================

CREATE INDEX IF NOT EXISTS idx_examenes_basicos_consulta ON examenes_basicos(consulta_id);
CREATE INDEX IF NOT EXISTS idx_biomicroscopia_consulta ON biomicroscopia(consulta_id);
CREATE INDEX IF NOT EXISTS idx_oftalmoscopia_consulta ON oftalmoscopia(consulta_id);
CREATE INDEX IF NOT EXISTS idx_datos_medicos_consulta ON datos_medicos_adicionales(consulta_id);

COMMIT;

-- ===============================================================================
-- VERIFICACIÓN
-- ===============================================================================

-- Verificar que se agregaron los campos
SELECT 'PACIENTES' as tabla, count(*) as total_campos 
FROM information_schema.columns 
WHERE table_name = 'pacientes'
UNION ALL
SELECT 'EXAMENES_BASICOS' as tabla, count(*) as total_campos 
FROM information_schema.columns 
WHERE table_name = 'examenes_basicos'
UNION ALL
SELECT 'BIOMICROSCOPIA' as tabla, count(*) as total_campos 
FROM information_schema.columns 
WHERE table_name = 'biomicroscopia'
UNION ALL
SELECT 'OFTALMOSCOPIA' as tabla, count(*) as total_campos 
FROM information_schema.columns 
WHERE table_name = 'oftalmoscopia';

-- ¡LISTO! Todas las tablas expandidas de manera inteligente