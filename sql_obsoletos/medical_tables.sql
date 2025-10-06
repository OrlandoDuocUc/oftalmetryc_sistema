-- ==============================================================
-- TABLAS PARA MÓDULO DE EXAMEN OFTALMOLÓGICO - OFTALMETRYC
-- ==============================================================

-- Tabla de Pacientes
CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
    rut VARCHAR(12) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    ocupacion VARCHAR(100),
    contacto_emergencia VARCHAR(100),
    telefono_emergencia VARCHAR(20),
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Consultas Médicas
CREATE TABLE consultas_medicas (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER REFERENCES pacientes(id) ON DELETE CASCADE,
    fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    medico VARCHAR(100),
    motivo_consulta TEXT,
    anamnesis TEXT,
    antecedentes_personales TEXT,
    antecedentes_familiares TEXT,
    medicamentos_actuales TEXT,
    alergias TEXT,
    diagnostico TEXT,
    plan_tratamiento TEXT,
    observaciones_generales TEXT,
    proxima_cita DATE,
    estado VARCHAR(20) DEFAULT 'activa', -- activa, completada, cancelada
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Examen Básico de la Vista
CREATE TABLE examenes_basicos (
    id SERIAL PRIMARY KEY,
    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
    
    -- Agudeza Visual Sin Corrección
    od_sc_lejos VARCHAR(10), -- Ojo derecho sin corrección lejos
    oi_sc_lejos VARCHAR(10), -- Ojo izquierdo sin corrección lejos
    ao_sc_lejos VARCHAR(10), -- Ambos ojos sin corrección lejos
    od_sc_cerca VARCHAR(10),
    oi_sc_cerca VARCHAR(10),
    ao_sc_cerca VARCHAR(10),
    
    -- Agudeza Visual Con Corrección
    od_cc_lejos VARCHAR(10),
    oi_cc_lejos VARCHAR(10),
    ao_cc_lejos VARCHAR(10),
    od_cc_cerca VARCHAR(10),
    oi_cc_cerca VARCHAR(10),
    ao_cc_cerca VARCHAR(10),
    
    -- Refracción Objetiva (Autorrefractómetro)
    od_esfera_obj DECIMAL(4,2),
    od_cilindro_obj DECIMAL(4,2),
    od_eje_obj INTEGER,
    oi_esfera_obj DECIMAL(4,2),
    oi_cilindro_obj DECIMAL(4,2),
    oi_eje_obj INTEGER,
    
    -- Refracción Subjetiva
    od_esfera_subj DECIMAL(4,2),
    od_cilindro_subj DECIMAL(4,2),
    od_eje_subj INTEGER,
    od_add DECIMAL(4,2), -- Adición para presbicia
    oi_esfera_subj DECIMAL(4,2),
    oi_cilindro_subj DECIMAL(4,2),
    oi_eje_subj INTEGER,
    oi_add DECIMAL(4,2),
    
    -- Presión Intraocular
    pio_od INTEGER, -- mmHg
    pio_oi INTEGER,
    metodo_pio VARCHAR(50), -- Goldmann, aire, etc.
    
    -- Evaluación Pupilar
    od_pupila_tamano DECIMAL(3,1), -- mm
    oi_pupila_tamano DECIMAL(3,1),
    od_reaccion_luz VARCHAR(20), -- normal, perezosa, ausente
    oi_reaccion_luz VARCHAR(20),
    defecto_pupilar_aferente BOOLEAN DEFAULT FALSE,
    
    -- Motilidad Ocular
    motilidad_normal BOOLEAN DEFAULT TRUE,
    limitacion_movimientos TEXT,
    nistagmo BOOLEAN DEFAULT FALSE,
    tipo_nistagmo VARCHAR(50),
    
    -- Visión de Colores
    ishihara_resultado VARCHAR(10), -- 21/21, defecto, etc.
    tipo_discromatopsia VARCHAR(30),
    
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Biomicroscopía (Examen del Segmento Anterior)
CREATE TABLE biomicroscopia (
    id SERIAL PRIMARY KEY,
    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
    
    -- Párpados OD
    od_parpados_posicion VARCHAR(20), -- normal, ptosis, retracción
    od_parpados_edema BOOLEAN DEFAULT FALSE,
    od_parpados_lesiones TEXT,
    od_pestanas VARCHAR(20), -- normales, triaquiasis, madarosis
    
    -- Párpados OI
    oi_parpados_posicion VARCHAR(20),
    oi_parpados_edema BOOLEAN DEFAULT FALSE,
    oi_parpados_lesiones TEXT,
    oi_pestanas VARCHAR(20),
    
    -- Conjuntiva OD
    od_conjuntiva_bulbar VARCHAR(30), -- normal, hiperemia, hemorragia
    od_conjuntiva_tarsal VARCHAR(30),
    od_conjuntiva_secrecion VARCHAR(30), -- ausente, mucosa, purulenta
    od_conjuntiva_foliculos BOOLEAN DEFAULT FALSE,
    od_conjuntiva_papilas BOOLEAN DEFAULT FALSE,
    
    -- Conjuntiva OI
    oi_conjuntiva_bulbar VARCHAR(30),
    oi_conjuntiva_tarsal VARCHAR(30),
    oi_conjuntiva_secrecion VARCHAR(30),
    oi_conjuntiva_foliculos BOOLEAN DEFAULT FALSE,
    oi_conjuntiva_papilas BOOLEAN DEFAULT FALSE,
    
    -- Córnea OD
    od_cornea_transparencia VARCHAR(20), -- transparente, opaca, leucoma
    od_cornea_superficie VARCHAR(20), -- lisa, irregular, erosión
    od_cornea_epitelo VARCHAR(20), -- intacto, defecto epitelial
    od_cornea_estroma VARCHAR(30), -- transparente, cicatrices, infiltrados
    od_cornea_endotelio VARCHAR(20), -- normal, precipitados, edema
    od_cornea_fluorenceina VARCHAR(30), -- negativa, positiva (describir)
    
    -- Córnea OI
    oi_cornea_transparencia VARCHAR(20),
    oi_cornea_superficie VARCHAR(20),
    oi_cornea_epitelo VARCHAR(20),
    oi_cornea_estroma VARCHAR(30),
    oi_cornea_endotelio VARCHAR(20),
    oi_cornea_fluorenceina VARCHAR(30),
    
    -- Cámara Anterior OD
    od_camara_profundidad VARCHAR(20), -- normal, superficial, profunda
    od_camara_contenido VARCHAR(30), -- transparente, células, fibrina, sangre
    od_camara_tyndall VARCHAR(10), -- grado 0-4
    
    -- Cámara Anterior OI
    oi_camara_profundidad VARCHAR(20),
    oi_camara_contenido VARCHAR(30),
    oi_camara_tyndall VARCHAR(10),
    
    -- Iris OD
    od_iris_color VARCHAR(20),
    od_iris_patrón VARCHAR(20), -- normal, atrofia, sinequias
    od_iris_lesiones TEXT,
    
    -- Iris OI
    oi_iris_color VARCHAR(20),
    oi_iris_patrón VARCHAR(20),
    oi_iris_lesiones TEXT,
    
    -- Cristalino OD
    od_cristalino_transparencia VARCHAR(30), -- transparente, catarata nuclear/cortical/subcapsular
    od_cristalino_posicion VARCHAR(20), -- normal, subluxación, luxación
    od_cristalino_pseudofaquia BOOLEAN DEFAULT FALSE,
    od_cristalino_lente_tipo VARCHAR(30), -- si es pseudofáquico
    
    -- Cristalino OI
    oi_cristalino_transparencia VARCHAR(30),
    oi_cristalino_posicion VARCHAR(20),
    oi_cristalino_pseudofaquia BOOLEAN DEFAULT FALSE,
    oi_cristalino_lente_tipo VARCHAR(30),
    
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Oftalmoscopía (Examen del Fondo de Ojo)
CREATE TABLE oftalmoscopia (
    id SERIAL PRIMARY KEY,
    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
    
    -- Vítreo OD
    od_vitreo VARCHAR(30), -- transparente, hialosis, hemorragia, opacidades
    od_vitreo_desprendimiento BOOLEAN DEFAULT FALSE,
    
    -- Vítreo OI
    oi_vitreo VARCHAR(30),
    oi_vitreo_desprendimiento BOOLEAN DEFAULT FALSE,
    
    -- Papila Óptica OD
    od_papila_color VARCHAR(20), -- normal, pálida, hiperémico
    od_papila_contornos VARCHAR(20), -- nítidos, borrosos
    od_papila_excavacion DECIMAL(3,2), -- relación copa/disco 0.0-1.0
    od_papila_hemorragias BOOLEAN DEFAULT FALSE,
    od_papila_edema BOOLEAN DEFAULT FALSE,
    
    -- Papila Óptica OI
    oi_papila_color VARCHAR(20),
    oi_papila_contornos VARCHAR(20),
    oi_papila_excavacion DECIMAL(3,2),
    oi_papila_hemorragias BOOLEAN DEFAULT FALSE,
    oi_papila_edema BOOLEAN DEFAULT FALSE,
    
    -- Mácula OD
    od_macula_reflejo VARCHAR(20), -- presente, ausente, alterado
    od_macula_pigmentacion VARCHAR(20), -- normal, hiper/hipopigmentación
    od_macula_exudados BOOLEAN DEFAULT FALSE,
    od_macula_hemorragias BOOLEAN DEFAULT FALSE,
    od_macula_edema BOOLEAN DEFAULT FALSE,
    od_macula_drusen BOOLEAN DEFAULT FALSE,
    
    -- Mácula OI
    oi_macula_reflejo VARCHAR(20),
    oi_macula_pigmentacion VARCHAR(20),
    oi_macula_exudados BOOLEAN DEFAULT FALSE,
    oi_macula_hemorragias BOOLEAN DEFAULT FALSE,
    oi_macula_edema BOOLEAN DEFAULT FALSE,
    oi_macula_drusen BOOLEAN DEFAULT FALSE,
    
    -- Vasos Retinianos OD
    od_arterias VARCHAR(30), -- calibre normal, estrechamiento, esclerosis
    od_venas VARCHAR(30), -- calibre normal, dilatación, tortuosidad
    od_cruces_av VARCHAR(30), -- normales, compresión, escotaduras
    od_hemorragias_retina BOOLEAN DEFAULT FALSE,
    od_exudados_duros BOOLEAN DEFAULT FALSE,
    od_exudados_blandos BOOLEAN DEFAULT FALSE,
    
    -- Vasos Retinianos OI
    oi_arterias VARCHAR(30),
    oi_venas VARCHAR(30),
    oi_cruces_av VARCHAR(30),
    oi_hemorragias_retina BOOLEAN DEFAULT FALSE,
    oi_exudados_duros BOOLEAN DEFAULT FALSE,
    oi_exudados_blandos BOOLEAN DEFAULT FALSE,
    
    -- Periferia Retiniana OD
    od_periferia VARCHAR(30), -- normal, degeneración, roturas
    od_desprendimiento BOOLEAN DEFAULT FALSE,
    
    -- Periferia Retiniana OI
    oi_periferia VARCHAR(30),
    oi_desprendimiento BOOLEAN DEFAULT FALSE,
    
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Diagnósticos (CIE-10 Oftalmológico)
CREATE TABLE diagnosticos (
    id SERIAL PRIMARY KEY,
    codigo_cie10 VARCHAR(10) NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    categoria VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de relación Consulta-Diagnósticos (muchos a muchos)
CREATE TABLE consulta_diagnosticos (
    id SERIAL PRIMARY KEY,
    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
    diagnostico_id INTEGER REFERENCES diagnosticos(id),
    es_principal BOOLEAN DEFAULT FALSE,
    ojo_afectado VARCHAR(10), -- OD, OI, AO
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Recetas Oftalmológicas
CREATE TABLE recetas_oftalmologicas (
    id SERIAL PRIMARY KEY,
    consulta_id INTEGER REFERENCES consultas_medicas(id) ON DELETE CASCADE,
    
    -- Datos del Lente OD
    od_esfera DECIMAL(4,2),
    od_cilindro DECIMAL(4,2),
    od_eje INTEGER,
    od_add DECIMAL(4,2),
    od_prisma DECIMAL(3,1),
    od_base VARCHAR(20),
    od_dp DECIMAL(4,1), -- Distancia pupilar
    
    -- Datos del Lente OI
    oi_esfera DECIMAL(4,2),
    oi_cilindro DECIMAL(4,2),
    oi_eje INTEGER,
    oi_add DECIMAL(4,2),
    oi_prisma DECIMAL(3,1),
    oi_base VARCHAR(20),
    oi_dp DECIMAL(4,1),
    
    -- Información adicional
    tipo_lente VARCHAR(50), -- monofocal, bifocal, progresivo
    material_lente VARCHAR(50), -- orgánico, mineral, policarbonato
    filtros VARCHAR(100), -- UV, antirreflex, fotocromático
    tipo_armazon VARCHAR(50), -- completo, al aire, semi al aire
    
    observaciones_receta TEXT,
    fecha_entrega DATE,
    vendedor_id BIGINT REFERENCES usuario(usuario_id),
    estado VARCHAR(20) DEFAULT 'pendiente', -- pendiente, en_proceso, entregado
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Citas Médicas
CREATE TABLE citas_medicas (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER REFERENCES pacientes(id) ON DELETE CASCADE,
    fecha_cita TIMESTAMP NOT NULL,
    tipo_cita VARCHAR(50) NOT NULL, -- consulta_general, control, urgencia
    medico VARCHAR(100),
    motivo TEXT,
    duracion_minutos INTEGER DEFAULT 30,
    estado VARCHAR(20) DEFAULT 'programada', -- programada, confirmada, completada, cancelada
    recordatorio_enviado BOOLEAN DEFAULT FALSE,
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================
-- INSERTAR DIAGNÓSTICOS OFTALMOLÓGICOS COMUNES (CIE-10)
-- ==============================================================

INSERT INTO diagnosticos (codigo_cie10, descripcion, categoria) VALUES
-- Trastornos del párpado
('H00', 'Orzuelo y calacio', 'Párpados'),
('H01', 'Otras inflamaciones del párpado', 'Párpados'),
('H02.0', 'Entropión y triquiasis del párpado', 'Párpados'),
('H02.1', 'Ectropión del párpado', 'Párpados'),
('H02.4', 'Ptosis del párpado', 'Párpados'),

-- Trastornos de la conjuntiva
('H10.0', 'Conjuntivitis mucopurulenta', 'Conjuntiva'),
('H10.1', 'Conjuntivitis atópica aguda', 'Conjuntiva'),
('H10.9', 'Conjuntivitis no especificada', 'Conjuntiva'),
('H11.0', 'Pterigión', 'Conjuntiva'),

-- Trastornos de la córnea
('H16.0', 'Úlcera corneal', 'Córnea'),
('H16.9', 'Queratitis no especificada', 'Córnea'),
('H17', 'Cicatrices y opacidades corneales', 'Córnea'),
('H18.6', 'Queratocono', 'Córnea'),

-- Trastornos del cristalino
('H25', 'Catarata senil', 'Cristalino'),
('H26', 'Otras cataratas', 'Cristalino'),
('H27.0', 'Afaquia', 'Cristalino'),

-- Trastornos de la retina
('H33', 'Desprendimientos y desgarros de la retina', 'Retina'),
('H35.0', 'Retinopatías de fondo y cambios vasculares de la retina', 'Retina'),
('H35.3', 'Degeneración de la mácula y del polo posterior', 'Retina'),
('H36.0', 'Retinopatía diabética', 'Retina'),

-- Glaucoma
('H40.0', 'Sospecha de glaucoma', 'Glaucoma'),
('H40.1', 'Glaucoma primario de ángulo abierto', 'Glaucoma'),
('H40.2', 'Glaucoma primario de ángulo cerrado', 'Glaucoma'),
('H40.9', 'Glaucoma no especificado', 'Glaucoma'),

-- Trastornos refractivos
('H52.0', 'Hipermetropía', 'Refracción'),
('H52.1', 'Miopía', 'Refracción'),
('H52.2', 'Astigmatismo', 'Refracción'),
('H52.4', 'Presbicia', 'Refracción'),

-- Trastornos de la motilidad ocular
('H50.0', 'Estrabismo convergente concomitante', 'Motilidad'),
('H50.1', 'Estrabismo divergente concomitante', 'Motilidad'),
('H49', 'Estrabismo paralítico', 'Motilidad'),

-- Otros
('H57.0', 'Anomalías de la función pupilar', 'Pupila'),
('H53.0', 'Ambliopía por anopsia', 'Visión'),
('H53.1', 'Trastornos visuales subjetivos', 'Visión'),
('Z01.0', 'Examen de los ojos y de la visión', 'Preventivo');

-- ==============================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ==============================================================

CREATE INDEX idx_pacientes_rut ON pacientes(rut);
CREATE INDEX idx_consultas_paciente ON consultas_medicas(paciente_id);
CREATE INDEX idx_consultas_fecha ON consultas_medicas(fecha_consulta);
CREATE INDEX idx_citas_paciente ON citas_medicas(paciente_id);
CREATE INDEX idx_citas_fecha ON citas_medicas(fecha_cita);
CREATE INDEX idx_recetas_consulta ON recetas_oftalmologicas(consulta_id);

-- ==============================================================
-- FUNCIONES PARA ACTUALIZAR TIMESTAMPS
-- ==============================================================

CREATE OR REPLACE FUNCTION actualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers para actualizar updated_at
CREATE TRIGGER trg_pacientes_updated_at
    BEFORE UPDATE ON pacientes
    FOR EACH ROW EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_consultas_updated_at
    BEFORE UPDATE ON consultas_medicas
    FOR EACH ROW EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_recetas_updated_at
    BEFORE UPDATE ON recetas_oftalmologicas
    FOR EACH ROW EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_citas_updated_at
    BEFORE UPDATE ON citas_medicas
    FOR EACH ROW EXECUTE FUNCTION actualizar_timestamp();

-- ==============================================================
-- COMENTARIOS EN LAS TABLAS
-- ==============================================================

COMMENT ON TABLE pacientes IS 'Información personal y de contacto de los pacientes';
COMMENT ON TABLE consultas_medicas IS 'Registro de consultas oftalmológicas realizadas';
COMMENT ON TABLE examenes_basicos IS 'Examen básico de agudeza visual, refracción y evaluación inicial';
COMMENT ON TABLE biomicroscopia IS 'Examen detallado del segmento anterior del ojo';
COMMENT ON TABLE oftalmoscopia IS 'Examen del fondo de ojo y estructuras posteriores';
COMMENT ON TABLE diagnosticos IS 'Catálogo de diagnósticos oftalmológicos según CIE-10';
COMMENT ON TABLE consulta_diagnosticos IS 'Relación entre consultas y diagnósticos asignados';
COMMENT ON TABLE recetas_oftalmologicas IS 'Prescripciones ópticas para corrección visual';
COMMENT ON TABLE citas_medicas IS 'Programación de citas oftalmológicas';