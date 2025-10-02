-- ===============================================================================
-- SCRIPT DE MIGRACIÓN - MÓDULO FICHA CLÍNICA DIGITAL
-- Sistema: Oftalmetryc - Ficha Clínica Completa
-- Autor: Orlando Rodriguez
-- Fecha: 2 de octubre de 2025
-- ===============================================================================

-- ESTRATEGIA: Evolución gradual manteniendo compatibilidad

-- ===============================================================================
-- PASO 1: CREAR NUEVAS TABLAS (EVOLUCIÓN)
-- ===============================================================================

-- TABLA EVOLUCIONADA: pacientes_v2 (basada en tu Paciente)
CREATE TABLE IF NOT EXISTS pacientes_v2 (
    id BIGSERIAL PRIMARY KEY,
    ci VARCHAR(20) UNIQUE NOT NULL,           -- Cédula Ecuador (era 'rut')
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    fecha_nacimiento DATE,
    edad INTEGER,                             -- NUEVO: calculable
    genero VARCHAR(10),                       -- NUEVO: M/F/Otro
    ocupacion VARCHAR(100),                   -- NUEVO
    hobby VARCHAR(200),                       -- NUEVO
    observaciones_generales TEXT,             -- NUEVO
    estado VARCHAR(20) DEFAULT 'Activo',     -- Mejorado
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLA EVOLUCIONADA: fichas_clinicas (basada en tu Ficha_Clinica)
CREATE TABLE IF NOT EXISTS fichas_clinicas (
    id BIGSERIAL PRIMARY KEY,
    paciente_id BIGINT REFERENCES pacientes_v2(id) ON DELETE CASCADE,
    fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo_consulta TEXT,
    ultimo_control_visual DATE,               -- NUEVO
    usa_lentes BOOLEAN DEFAULT FALSE,         -- NUEVO
    ultimo_cambio_lentes DATE,               -- NUEVO
    antecedentes_personales TEXT,
    antecedentes_familiares TEXT,
    diagnostico_general TEXT,
    tratamiento_general TEXT,
    firma_responsable VARCHAR(100),          -- NUEVO
    conforme_evaluado BOOLEAN DEFAULT TRUE,  -- NUEVO
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLA NUEVA: examenes_oftalmologicos_completos
CREATE TABLE IF NOT EXISTS examenes_oftalmologicos_completos (
    id BIGSERIAL PRIMARY KEY,
    ficha_clinica_id BIGINT UNIQUE REFERENCES fichas_clinicas(id) ON DELETE CASCADE,
    
    -- ===== SECCIÓN 1: AGUDEZA VISUAL =====
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
    
    -- ===== SECCIÓN 2: LENSOMETRÍA =====
    lensometria_od VARCHAR(50),
    lensometria_oi VARCHAR(50),
    
    -- ===== SECCIÓN 3: QUERATOMETRÍA =====
    queratometria_od VARCHAR(50),
    queratometria_oi VARCHAR(50),
    
    -- ===== SECCIÓN 4: AUTOREFRACTOR =====
    ar_esf_od VARCHAR(10),
    ar_cyl_od VARCHAR(10),
    ar_eje_od VARCHAR(10),
    ar_av_od VARCHAR(10),
    ar_esf_oi VARCHAR(10),
    ar_cyl_oi VARCHAR(10),
    ar_eje_oi VARCHAR(10),
    ar_av_oi VARCHAR(10),
    
    -- ===== SECCIÓN 5: SUBJETIVO =====
    sub_esf_od VARCHAR(10),
    sub_cyl_od VARCHAR(10),
    sub_eje_od VARCHAR(10),
    sub_av_od VARCHAR(10),
    sub_esf_oi VARCHAR(10),
    sub_cyl_oi VARCHAR(10),
    sub_eje_oi VARCHAR(10),
    sub_av_oi VARCHAR(10),
    
    -- ===== SECCIÓN 6: RX FINAL =====
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
    
    -- ===== SECCIÓN 7: LENTES DE CONTACTO =====
    lc_poder_od VARCHAR(10),
    lc_curva_base_od VARCHAR(10),
    lc_diametro_od VARCHAR(10),
    lc_adicion_od VARCHAR(10),
    lc_diseno_od VARCHAR(50),
    lc_material_od VARCHAR(50),
    lc_poder_oi VARCHAR(10),
    lc_curva_base_oi VARCHAR(10),
    lc_diametro_oi VARCHAR(10),
    lc_adicion_oi VARCHAR(10),
    lc_diseno_oi VARCHAR(50),
    lc_material_oi VARCHAR(50),
    
    -- ===== SECCIÓN 8: TEST ADICIONALES =====
    hirschberg_od INTEGER CHECK (hirschberg_od IN (0, 15, 30, 45)),
    hirschberg_oi INTEGER CHECK (hirschberg_oi IN (0, 15, 30, 45)),
    campimetria_t100_od VARCHAR(20),
    campimetria_n60_od VARCHAR(20),
    campimetria_s60_od VARCHAR(20),
    campimetria_i70_od VARCHAR(20),
    campimetria_t100_oi VARCHAR(20),
    campimetria_n60_oi VARCHAR(20),
    campimetria_s60_oi VARCHAR(20),
    campimetria_i70_oi VARCHAR(20),
    cover_test_pfc VARCHAR(50),
    cover_test_foria VARCHAR(50),
    cover_test_tropia VARCHAR(50),
    cover_test_mag_desviacion VARCHAR(50),
    mov_oculares VARCHAR(100),
    luces_worth_lejos VARCHAR(50),
    luces_worth_cerca VARCHAR(50),
    test_ishihara VARCHAR(50),
    presion_intraocular_od VARCHAR(20),
    presion_intraocular_oi VARCHAR(20),
    test_adicionales_otros TEXT,
    
    -- ===== SECCIÓN 9: BIOMICROSCOPÍA =====
    biomic_cornea_od TEXT,
    biomic_cornea_oi TEXT,
    biomic_cristalino_od TEXT,
    biomic_cristalino_oi TEXT,
    biomic_pupila_od TEXT,
    biomic_pupila_oi TEXT,
    biomic_pestanas_od TEXT,
    biomic_pestanas_oi TEXT,
    biomic_conjuntiva_bulbar_od TEXT,
    biomic_conjuntiva_bulbar_oi TEXT,
    biomic_conjuntiva_tarsal_od TEXT,
    biomic_conjuntiva_tarsal_oi TEXT,
    biomic_esclera_od TEXT,
    biomic_esclera_oi TEXT,
    biomic_pliegue_semilunar_od TEXT,
    biomic_pliegue_semilunar_oi TEXT,
    biomic_caruncula_od TEXT,
    biomic_caruncula_oi TEXT,
    biomic_conductos_lagrimales_od TEXT,
    biomic_conductos_lagrimales_oi TEXT,
    biomic_parpado_superior_od TEXT,
    biomic_parpado_superior_oi TEXT,
    biomic_camara_anterior_od TEXT,
    biomic_camara_anterior_oi TEXT,
    biomic_parpado_inferior_od TEXT,
    biomic_parpado_inferior_oi TEXT,
    biomic_otros TEXT,
    
    -- ===== SECCIÓN 10: REFLEJOS PUPILARES =====
    reflejo_acomodativo_miosis_od VARCHAR(50),
    reflejo_acomodativo_convergencia_od VARCHAR(50),
    reflejo_acomodativo_midriasis_od VARCHAR(50),
    reflejo_acomodativo_miosis_oi VARCHAR(50),
    reflejo_acomodativo_convergencia_oi VARCHAR(50),
    reflejo_acomodativo_midriasis_oi VARCHAR(50),
    reflejo_fotomotor_miosis_od VARCHAR(50),
    reflejo_fotomotor_midriasis_od VARCHAR(50),
    reflejo_consensual_od VARCHAR(50),
    reflejo_fotomotor_miosis_oi VARCHAR(50),
    reflejo_fotomotor_midriasis_oi VARCHAR(50),
    reflejo_consensual_oi VARCHAR(50),
    
    -- ===== SECCIÓN 11: FONDO DE OJO =====
    fondo_ojo_av_temp_sup_od TEXT,
    fondo_ojo_av_temp_inf_od TEXT,
    fondo_ojo_av_nasal_sup_od TEXT,
    fondo_ojo_av_nasal_inf_od TEXT,
    fondo_ojo_retina_od TEXT,
    fondo_ojo_macula_od TEXT,
    fondo_ojo_excavacion_od TEXT,
    fondo_ojo_vasos_od TEXT,
    fondo_ojo_papila_od TEXT,
    fondo_ojo_fijacion_od TEXT,
    fondo_ojo_color_od TEXT,
    fondo_ojo_borde_od TEXT,
    fondo_ojo_av_temp_sup_oi TEXT,
    fondo_ojo_av_temp_inf_oi TEXT,
    fondo_ojo_av_nasal_sup_oi TEXT,
    fondo_ojo_av_nasal_inf_oi TEXT,
    fondo_ojo_retina_oi TEXT,
    fondo_ojo_macula_oi TEXT,
    fondo_ojo_excavacion_oi TEXT,
    fondo_ojo_vasos_oi TEXT,
    fondo_ojo_papila_oi TEXT,
    fondo_ojo_fijacion_oi TEXT,
    fondo_ojo_color_oi TEXT,
    fondo_ojo_borde_oi TEXT,
    fondo_ojo_otros TEXT,
    
    -- ===== SECCIÓN 12: OTROS DATOS MÉDICOS =====
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
-- PASO 2: CREAR ÍNDICES PARA OPTIMIZACIÓN
-- ===============================================================================

CREATE INDEX IF NOT EXISTS idx_pacientes_v2_ci ON pacientes_v2(ci);
CREATE INDEX IF NOT EXISTS idx_pacientes_v2_nombres ON pacientes_v2(nombres, apellidos);
CREATE INDEX IF NOT EXISTS idx_fichas_clinicas_paciente ON fichas_clinicas(paciente_id);
CREATE INDEX IF NOT EXISTS idx_fichas_clinicas_fecha ON fichas_clinicas(fecha_consulta);
CREATE INDEX IF NOT EXISTS idx_examenes_ficha ON examenes_oftalmologicos_completos(ficha_clinica_id);

-- ===============================================================================
-- PASO 3: CREAR TRIGGERS PARA TIMESTAMPS
-- ===============================================================================

-- Trigger para pacientes_v2
CREATE OR REPLACE FUNCTION actualizar_timestamp_pacientes_v2()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    -- Calcular edad automáticamente
    IF NEW.fecha_nacimiento IS NOT NULL THEN
        NEW.edad = EXTRACT(YEAR FROM age(NEW.fecha_nacimiento));
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_pacientes_v2_updated_at ON pacientes_v2;
CREATE TRIGGER trg_pacientes_v2_updated_at
    BEFORE UPDATE ON pacientes_v2
    FOR EACH ROW EXECUTE FUNCTION actualizar_timestamp_pacientes_v2();

-- Trigger para fichas_clinicas
DROP TRIGGER IF EXISTS trg_fichas_clinicas_updated_at ON fichas_clinicas;
CREATE TRIGGER trg_fichas_clinicas_updated_at
    BEFORE UPDATE ON fichas_clinicas
    FOR EACH ROW EXECUTE FUNCTION actualizar_timestamp();

-- ===============================================================================
-- PASO 4: MIGRACIÓN DE DATOS EXISTENTES
-- ===============================================================================

-- Migrar pacientes existentes
INSERT INTO pacientes_v2 (
    ci, nombres, apellidos, telefono, email, direccion, 
    fecha_nacimiento, ocupacion, observaciones_generales, 
    fecha_creacion
)
SELECT 
    rut as ci,
    nombre as nombres,
    apellido as apellidos,
    telefono,
    email,
    direccion,
    fecha_nacimiento,
    ocupacion,
    observaciones as observaciones_generales,
    created_at as fecha_creacion
FROM pacientes
ON CONFLICT (ci) DO NOTHING;

-- Migrar consultas existentes
INSERT INTO fichas_clinicas (
    paciente_id, fecha_consulta, motivo_consulta,
    antecedentes_personales, antecedentes_familiares,
    diagnostico_general, tratamiento_general
)
SELECT 
    p2.id as paciente_id,
    c.fecha_consulta,
    c.motivo_consulta,
    c.antecedentes_personales,
    c.antecedentes_familiares,
    c.diagnostico as diagnostico_general,
    c.plan_tratamiento as tratamiento_general
FROM consultas_medicas c
JOIN pacientes p1 ON c.paciente_id = p1.id
JOIN pacientes_v2 p2 ON p1.rut = p2.ci;

-- ===============================================================================
-- PASO 5: CREAR VISTAS DE COMPATIBILIDAD
-- ===============================================================================

-- Vista para mantener compatibilidad con código existente
CREATE OR REPLACE VIEW pacientes_compatibilidad AS
SELECT 
    id,
    ci as rut,
    nombres as nombre,
    apellidos as apellido,
    telefono,
    email,
    direccion,
    fecha_nacimiento,
    ocupacion,
    observaciones_generales as observaciones,
    fecha_creacion as created_at,
    fecha_actualizacion as updated_at
FROM pacientes_v2;

COMMIT;