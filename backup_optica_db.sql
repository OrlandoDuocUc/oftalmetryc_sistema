--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: actualizar_fecha_modificacion_proveedor(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.actualizar_fecha_modificacion_proveedor() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.fecha_actualizacion := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.actualizar_fecha_modificacion_proveedor() OWNER TO postgres;

--
-- Name: generar_codigo_proveedor(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.generar_codigo_proveedor() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.codigo_proveedor IS NULL OR NEW.codigo_proveedor = '' THEN
        NEW.codigo_proveedor := 'PROV' || LPAD(NEW.proveedor_id::text, 6, '0');
    END IF;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.generar_codigo_proveedor() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: biomicroscopia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.biomicroscopia (
    biomicroscopia_id integer NOT NULL,
    ficha_id integer,
    parpados_od text,
    conjuntiva_od text,
    cornea_od text,
    camara_anterior_od text,
    iris_od text,
    pupila_od_mm character varying(10),
    pupila_od_reaccion character varying(20),
    cristalino_od text,
    parpados_oi text,
    conjuntiva_oi text,
    cornea_oi text,
    camara_anterior_oi text,
    iris_oi text,
    pupila_oi_mm character varying(10),
    pupila_oi_reaccion character varying(20),
    cristalino_oi text,
    observaciones_generales text,
    fecha_examen timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    pupila_desc_od text,
    pestanas_od text,
    conjuntiva_bulbar_od text,
    conjuntiva_tarsal_od text,
    orbita_od text,
    pliegue_semilunar_od text,
    caruncula_od text,
    conductos_lagrimales_od text,
    parpado_superior_od text,
    parpado_inferior_od text,
    pupila_desc_oi text,
    pestanas_oi text,
    conjuntiva_bulbar_oi text,
    conjuntiva_tarsal_oi text,
    orbita_oi text,
    pliegue_semilunar_oi text,
    caruncula_oi text,
    conductos_lagrimales_oi text,
    parpado_superior_oi text,
    parpado_inferior_oi text,
    otros_detalles text
);


ALTER TABLE public.biomicroscopia OWNER TO postgres;

--
-- Name: biomicroscopia_biomicroscopia_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.biomicroscopia_biomicroscopia_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.biomicroscopia_biomicroscopia_id_seq OWNER TO postgres;

--
-- Name: biomicroscopia_biomicroscopia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.biomicroscopia_biomicroscopia_id_seq OWNED BY public.biomicroscopia.biomicroscopia_id;


--
-- Name: campos_visuales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.campos_visuales (
    campo_visual_id integer NOT NULL,
    ficha_id integer,
    tipo_campo character varying(50),
    resultado_od text,
    resultado_oi text,
    interpretacion text,
    fecha_examen timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.campos_visuales OWNER TO postgres;

--
-- Name: campos_visuales_campo_visual_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.campos_visuales_campo_visual_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.campos_visuales_campo_visual_id_seq OWNER TO postgres;

--
-- Name: campos_visuales_campo_visual_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.campos_visuales_campo_visual_id_seq OWNED BY public.campos_visuales.campo_visual_id;


--
-- Name: clientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clientes (
    cliente_id integer NOT NULL,
    nombres character varying(100) NOT NULL,
    ap_pat character varying(100) NOT NULL,
    ap_mat character varying(100),
    rut character varying(20) NOT NULL,
    email character varying(120),
    telefono character varying(20),
    direccion text,
    fecha_nacimiento date,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    estado boolean DEFAULT true
);


ALTER TABLE public.clientes OWNER TO postgres;

--
-- Name: clientes_cliente_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clientes_cliente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clientes_cliente_id_seq OWNER TO postgres;

--
-- Name: clientes_cliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clientes_cliente_id_seq OWNED BY public.clientes.cliente_id;


--
-- Name: detalle_ventas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.detalle_ventas (
    detalle_id integer NOT NULL,
    venta_id integer,
    producto_id integer,
    cantidad integer NOT NULL,
    precio_unitario numeric(10,2) NOT NULL,
    subtotal numeric(10,2) NOT NULL
);


ALTER TABLE public.detalle_ventas OWNER TO postgres;

--
-- Name: detalle_ventas_detalle_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.detalle_ventas_detalle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.detalle_ventas_detalle_id_seq OWNER TO postgres;

--
-- Name: detalle_ventas_detalle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.detalle_ventas_detalle_id_seq OWNED BY public.detalle_ventas.detalle_id;


--
-- Name: diagnosticos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.diagnosticos (
    diagnostico_id integer NOT NULL,
    ficha_id integer,
    diagnostico_principal text NOT NULL,
    diagnosticos_secundarios text,
    cie_10_principal character varying(10),
    cie_10_secundarios text,
    severidad character varying(20),
    observaciones text,
    fecha_diagnostico timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.diagnosticos OWNER TO postgres;

--
-- Name: diagnosticos_diagnostico_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.diagnosticos_diagnostico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.diagnosticos_diagnostico_id_seq OWNER TO postgres;

--
-- Name: diagnosticos_diagnostico_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.diagnosticos_diagnostico_id_seq OWNED BY public.diagnosticos.diagnostico_id;


--
-- Name: fichas_clinicas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fichas_clinicas (
    ficha_id integer NOT NULL,
    paciente_medico_id integer,
    usuario_id integer,
    numero_consulta character varying(20) NOT NULL,
    fecha_consulta timestamp without time zone NOT NULL,
    motivo_consulta text,
    historia_actual text,
    av_od_sc character varying(20),
    av_od_cc character varying(20),
    av_od_ph character varying(20),
    av_od_cerca character varying(20),
    av_oi_sc character varying(20),
    av_oi_cc character varying(20),
    av_oi_ph character varying(20),
    av_oi_cerca character varying(20),
    esfera_od character varying(10),
    cilindro_od character varying(10),
    eje_od character varying(10),
    adicion_od character varying(10),
    esfera_oi character varying(10),
    cilindro_oi character varying(10),
    eje_oi character varying(10),
    adicion_oi character varying(10),
    distancia_pupilar character varying(10),
    tipo_lente character varying(50),
    estado character varying(20) DEFAULT 'en_proceso'::character varying,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.fichas_clinicas OWNER TO postgres;

--
-- Name: fichas_clinicas_ficha_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fichas_clinicas_ficha_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.fichas_clinicas_ficha_id_seq OWNER TO postgres;

--
-- Name: fichas_clinicas_ficha_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fichas_clinicas_ficha_id_seq OWNED BY public.fichas_clinicas.ficha_id;


--
-- Name: fondo_ojo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fondo_ojo (
    fondo_ojo_id integer NOT NULL,
    ficha_id integer,
    disco_optico_od text,
    macula_od text,
    vasos_od text,
    retina_periferica_od text,
    disco_optico_oi text,
    macula_oi text,
    vasos_oi text,
    retina_periferica_oi text,
    observaciones text,
    fecha_examen timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    av_temp_sup_od text,
    av_temp_inf_od text,
    av_nasal_sup_od text,
    av_nasal_inf_od text,
    retina_od text,
    excavacion_od text,
    papila_detalle_od text,
    fijacion_od text,
    color_od text,
    borde_od text,
    av_temp_sup_oi text,
    av_temp_inf_oi text,
    av_nasal_sup_oi text,
    av_nasal_inf_oi text,
    retina_oi text,
    excavacion_oi text,
    papila_detalle_oi text,
    fijacion_oi text,
    color_oi text,
    borde_oi text,
    otros_detalles text
);


ALTER TABLE public.fondo_ojo OWNER TO postgres;

--
-- Name: fondo_ojo_fondo_ojo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fondo_ojo_fondo_ojo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.fondo_ojo_fondo_ojo_id_seq OWNER TO postgres;

--
-- Name: fondo_ojo_fondo_ojo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fondo_ojo_fondo_ojo_id_seq OWNED BY public.fondo_ojo.fondo_ojo_id;


--
-- Name: pacientes_medicos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pacientes_medicos (
    paciente_medico_id integer NOT NULL,
    cliente_id integer,
    numero_ficha character varying(20) NOT NULL,
    antecedentes_medicos text,
    antecedentes_oculares text,
    alergias text,
    medicamentos_actuales text,
    contacto_emergencia character varying(100),
    telefono_emergencia character varying(20),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    estado boolean DEFAULT true
);


ALTER TABLE public.pacientes_medicos OWNER TO postgres;

--
-- Name: pacientes_medicos_paciente_medico_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pacientes_medicos_paciente_medico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pacientes_medicos_paciente_medico_id_seq OWNER TO postgres;

--
-- Name: pacientes_medicos_paciente_medico_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pacientes_medicos_paciente_medico_id_seq OWNED BY public.pacientes_medicos.paciente_medico_id;


--
-- Name: parametros_clinicos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parametros_clinicos (
    parametro_id integer NOT NULL,
    ficha_id integer NOT NULL,
    presion_sistolica character varying(10),
    presion_diastolica character varying(10),
    saturacion_o2 character varying(10),
    glucosa character varying(20),
    trigliceridos character varying(20),
    ttp character varying(20),
    atp character varying(20),
    colesterol character varying(20),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.parametros_clinicos OWNER TO postgres;

--
-- Name: parametros_clinicos_parametro_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.parametros_clinicos_parametro_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.parametros_clinicos_parametro_id_seq OWNER TO postgres;

--
-- Name: parametros_clinicos_parametro_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.parametros_clinicos_parametro_id_seq OWNED BY public.parametros_clinicos.parametro_id;


--
-- Name: presion_intraocular; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.presion_intraocular (
    pio_id integer NOT NULL,
    ficha_id integer,
    pio_od character varying(10),
    pio_oi character varying(10),
    metodo_medicion character varying(50),
    hora_medicion time without time zone,
    observaciones text,
    fecha_medicion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.presion_intraocular OWNER TO postgres;

--
-- Name: presion_intraocular_pio_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.presion_intraocular_pio_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.presion_intraocular_pio_id_seq OWNER TO postgres;

--
-- Name: presion_intraocular_pio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.presion_intraocular_pio_id_seq OWNED BY public.presion_intraocular.pio_id;


--
-- Name: productos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.productos (
    producto_id integer NOT NULL,
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    nombre character varying(200) NOT NULL,
    distribuidor character varying(200),
    marca character varying(100),
    material character varying(100),
    tipo_armazon character varying(100),
    codigo character varying(50),
    diametro_1 character varying(50),
    diametro_2 character varying(50),
    color character varying(100),
    cantidad integer DEFAULT 0,
    costo_unitario numeric(10,2) NOT NULL,
    costo_total numeric(10,2),
    costo_venta_1 numeric(10,2),
    costo_venta_2 numeric(10,2),
    descripcion text,
    estado boolean DEFAULT true,
    CONSTRAINT ck_productos_cantidad_non_negative CHECK (cantidad >= 0),
    CONSTRAINT ck_productos_costo_unitario_positive CHECK (costo_unitario >= 0)
);


ALTER TABLE public.productos OWNER TO postgres;

--
-- Name: productos_producto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.productos_producto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.productos_producto_id_seq OWNER TO postgres;

--
-- Name: productos_producto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.productos_producto_id_seq OWNED BY public.productos.producto_id;


--
-- Name: proveedores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.proveedores (
    proveedor_id integer NOT NULL,
    codigo_proveedor character varying(20) NOT NULL,
    razon_social character varying(255) NOT NULL,
    nombre_comercial character varying(255),
    rut character varying(12) NOT NULL,
    direccion text,
    telefono character varying(20),
    email character varying(100),
    sitio_web character varying(255),
    categoria_productos text,
    condiciones_pago character varying(50) DEFAULT 'Contado'::character varying,
    plazo_pago_dias integer DEFAULT 0,
    descuento_volumen numeric(5,2) DEFAULT 0.00,
    representante_nombre character varying(255),
    representante_telefono character varying(20),
    representante_email character varying(100),
    observaciones text,
    estado boolean DEFAULT true,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_descuento_volumen CHECK (((descuento_volumen >= (0)::numeric) AND (descuento_volumen <= (100)::numeric))),
    CONSTRAINT chk_email_formato CHECK (((email IS NULL) OR ((email)::text ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'::text))),
    CONSTRAINT chk_plazo_pago CHECK ((plazo_pago_dias >= 0)),
    CONSTRAINT chk_representante_email_formato CHECK (((representante_email IS NULL) OR ((representante_email)::text ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'::text)))
);


ALTER TABLE public.proveedores OWNER TO postgres;

--
-- Name: proveedores_proveedor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.proveedores_proveedor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.proveedores_proveedor_id_seq OWNER TO postgres;

--
-- Name: proveedores_proveedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.proveedores_proveedor_id_seq OWNED BY public.proveedores.proveedor_id;


--
-- Name: reflejos_pupilares; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reflejos_pupilares (
    reflejo_id integer NOT NULL,
    ficha_id integer NOT NULL,
    acomodativo_uno text,
    fotomotor_uno text,
    consensual_uno text,
    acomodativo_dos text,
    fotomotor_dos text,
    consensual_dos text,
    observaciones text,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.reflejos_pupilares OWNER TO postgres;

--
-- Name: reflejos_pupilares_reflejo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reflejos_pupilares_reflejo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reflejos_pupilares_reflejo_id_seq OWNER TO postgres;

--
-- Name: reflejos_pupilares_reflejo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reflejos_pupilares_reflejo_id_seq OWNED BY public.reflejos_pupilares.reflejo_id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    rol_id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    descripcion text,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    estado boolean DEFAULT true
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: roles_rol_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_rol_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_rol_id_seq OWNER TO postgres;

--
-- Name: roles_rol_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_rol_id_seq OWNED BY public.roles.rol_id;


--
-- Name: tratamientos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tratamientos (
    tratamiento_id integer NOT NULL,
    ficha_id integer,
    medicamentos text,
    tratamiento_no_farmacologico text,
    recomendaciones text,
    plan_seguimiento text,
    proxima_cita date,
    urgencia_seguimiento character varying(20),
    fecha_tratamiento timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.tratamientos OWNER TO postgres;

--
-- Name: tratamientos_tratamiento_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tratamientos_tratamiento_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tratamientos_tratamiento_id_seq OWNER TO postgres;

--
-- Name: tratamientos_tratamiento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tratamientos_tratamiento_id_seq OWNED BY public.tratamientos.tratamiento_id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    usuario_id integer NOT NULL,
    rol_id integer,
    username character varying(80) NOT NULL,
    password character varying(255) NOT NULL,
    nombre character varying(100) NOT NULL,
    ap_pat character varying(100) NOT NULL,
    ap_mat character varying(100),
    email character varying(120) NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    estado boolean DEFAULT true
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_usuario_id_seq OWNER TO postgres;

--
-- Name: usuarios_usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_usuario_id_seq OWNED BY public.usuarios.usuario_id;


--
-- Name: ventas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ventas (
    venta_id integer NOT NULL,
    cliente_id integer,
    usuario_id integer,
    fecha_venta timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    total numeric(10,2) NOT NULL,
    descuento numeric(5,2) DEFAULT 0,
    metodo_pago character varying(50),
    observaciones text,
    estado character varying(20) DEFAULT 'completada'::character varying
);


ALTER TABLE public.ventas OWNER TO postgres;

--
-- Name: ventas_venta_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ventas_venta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ventas_venta_id_seq OWNER TO postgres;

--
-- Name: ventas_venta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ventas_venta_id_seq OWNED BY public.ventas.venta_id;


--
-- Name: biomicroscopia biomicroscopia_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.biomicroscopia ALTER COLUMN biomicroscopia_id SET DEFAULT nextval('public.biomicroscopia_biomicroscopia_id_seq'::regclass);


--
-- Name: campos_visuales campo_visual_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campos_visuales ALTER COLUMN campo_visual_id SET DEFAULT nextval('public.campos_visuales_campo_visual_id_seq'::regclass);


--
-- Name: clientes cliente_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes ALTER COLUMN cliente_id SET DEFAULT nextval('public.clientes_cliente_id_seq'::regclass);


--
-- Name: detalle_ventas detalle_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_ventas ALTER COLUMN detalle_id SET DEFAULT nextval('public.detalle_ventas_detalle_id_seq'::regclass);


--
-- Name: diagnosticos diagnostico_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diagnosticos ALTER COLUMN diagnostico_id SET DEFAULT nextval('public.diagnosticos_diagnostico_id_seq'::regclass);


--
-- Name: fichas_clinicas ficha_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fichas_clinicas ALTER COLUMN ficha_id SET DEFAULT nextval('public.fichas_clinicas_ficha_id_seq'::regclass);


--
-- Name: fondo_ojo fondo_ojo_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fondo_ojo ALTER COLUMN fondo_ojo_id SET DEFAULT nextval('public.fondo_ojo_fondo_ojo_id_seq'::regclass);


--
-- Name: pacientes_medicos paciente_medico_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes_medicos ALTER COLUMN paciente_medico_id SET DEFAULT nextval('public.pacientes_medicos_paciente_medico_id_seq'::regclass);


--
-- Name: parametros_clinicos parametro_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_clinicos ALTER COLUMN parametro_id SET DEFAULT nextval('public.parametros_clinicos_parametro_id_seq'::regclass);


--
-- Name: presion_intraocular pio_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.presion_intraocular ALTER COLUMN pio_id SET DEFAULT nextval('public.presion_intraocular_pio_id_seq'::regclass);


--
-- Name: productos producto_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos ALTER COLUMN producto_id SET DEFAULT nextval('public.productos_producto_id_seq'::regclass);


--
-- Name: proveedores proveedor_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedores ALTER COLUMN proveedor_id SET DEFAULT nextval('public.proveedores_proveedor_id_seq'::regclass);


--
-- Name: reflejos_pupilares reflejo_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reflejos_pupilares ALTER COLUMN reflejo_id SET DEFAULT nextval('public.reflejos_pupilares_reflejo_id_seq'::regclass);


--
-- Name: roles rol_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN rol_id SET DEFAULT nextval('public.roles_rol_id_seq'::regclass);


--
-- Name: tratamientos tratamiento_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tratamientos ALTER COLUMN tratamiento_id SET DEFAULT nextval('public.tratamientos_tratamiento_id_seq'::regclass);


--
-- Name: usuarios usuario_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN usuario_id SET DEFAULT nextval('public.usuarios_usuario_id_seq'::regclass);


--
-- Name: ventas venta_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ventas ALTER COLUMN venta_id SET DEFAULT nextval('public.ventas_venta_id_seq'::regclass);


--
-- Data for Name: biomicroscopia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.biomicroscopia (biomicroscopia_id, ficha_id, parpados_od, conjuntiva_od, cornea_od, camara_anterior_od, iris_od, pupila_od_mm, pupila_od_reaccion, cristalino_od, parpados_oi, conjuntiva_oi, cornea_oi, camara_anterior_oi, iris_oi, pupila_oi_mm, pupila_oi_reaccion, cristalino_oi, observaciones_generales, fecha_examen, pupila_desc_od, pestanas_od, conjuntiva_bulbar_od, conjuntiva_tarsal_od, orbita_od, pliegue_semilunar_od, caruncula_od, conductos_lagrimales_od, parpado_superior_od, parpado_inferior_od, pupila_desc_oi, pestanas_oi, conjuntiva_bulbar_oi, conjuntiva_tarsal_oi, orbita_oi, pliegue_semilunar_oi, caruncula_oi, conductos_lagrimales_oi, parpado_superior_oi, parpado_inferior_oi, otros_detalles) FROM stdin;
\.


--
-- Data for Name: campos_visuales; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.campos_visuales (campo_visual_id, ficha_id, tipo_campo, resultado_od, resultado_oi, interpretacion, fecha_examen) FROM stdin;
\.


--
-- Data for Name: clientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clientes (cliente_id, nombres, ap_pat, ap_mat, rut, email, telefono, direccion, fecha_nacimiento, fecha_creacion, estado) FROM stdin;
1	Juan	Pérez	González	12.345.678-9	juan@test.com	+56912345678	\N	\N	2025-10-05 00:20:40.071838	t
2	jacinto	Gutierrez	Ramirez	18.222.933-3	jc@gmail.com	987689898	guayaquil 2025	1991-03-04	2025-10-05 00:36:15.318328	t
5	clorofilo	milano	cepeda	11.414.112-3	clorofilo@gmail.com	931891202	las nieves 3131	1987-06-09	2025-10-09 20:12:35.700403	t
6	ignacio	gutierrez	ramirez	12.341.234-1	ig@gmail.com	213152451	san mateo 1255	1977-11-10	2025-10-11 01:28:21.104831	t
7	orlando	rodriguez	modler	0321323313001	ro@gmail.com	+59345454545	\N	1979-08-13	2025-10-13 22:25:46.130442	t
11	primario	primer	prime	9999999-1	primer@gmail.com	213021412	primero 5656	\N	2025-10-14 05:11:37.083973	t
12	raul	rojas	moreno	21324654-8	raul@gmail.com	9899812392	santiago 4545	\N	2025-10-14 05:21:55.278177	t
13	paco	paco	paco	11123123-5	paco@gmail.com	9898983498	villa almena 2332	\N	2025-10-14 05:30:07.014127	t
14	adriana	perez	locoma	0100000009	adriana@gmail.com	0989878987	las rosas 356	\N	2025-10-14 08:26:43.293261	t
\.


--
-- Data for Name: detalle_ventas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.detalle_ventas (detalle_id, venta_id, producto_id, cantidad, precio_unitario, subtotal) FROM stdin;
1	1	4	1	8500.00	8500.00
2	2	6	1	70.00	70.00
3	3	5	1	3500.00	3500.00
4	4	1	1	25000.00	25000.00
\.


--
-- Data for Name: diagnosticos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.diagnosticos (diagnostico_id, ficha_id, diagnostico_principal, diagnosticos_secundarios, cie_10_principal, cie_10_secundarios, severidad, observaciones, fecha_diagnostico) FROM stdin;
\.


--
-- Data for Name: fichas_clinicas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fichas_clinicas (ficha_id, paciente_medico_id, usuario_id, numero_consulta, fecha_consulta, motivo_consulta, historia_actual, av_od_sc, av_od_cc, av_od_ph, av_od_cerca, av_oi_sc, av_oi_cc, av_oi_ph, av_oi_cerca, esfera_od, cilindro_od, eje_od, adicion_od, esfera_oi, cilindro_oi, eje_oi, adicion_oi, distancia_pupilar, tipo_lente, estado, fecha_creacion) FROM stdin;
1	2	1	CONS-1759624884327	2025-10-04 21:41:00	dolor de ojo 	dolor en el ojo izquierdo con irritacion 																			en_proceso	2025-10-04 21:42:39.226874
2	3	1	CONS-1760045042816	2025-10-09 23:24:00	dolor de ojo DERECHO	paciente refiere dolor de ojo																			en_proceso	2025-10-09 18:26:09.36954
3	4	1	CONS-1760305930889	2025-10-12 18:52:00	ARDOR DE OJOS	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	en_proceso	2025-10-12 19:08:25.854684
4	1	1	CONS-1760381614740	2025-10-13 15:53:00	MIOPIA Y FATIGA VISUAL	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	en_proceso	2025-10-13 15:54:40.875561
6	6	1	CONS-251014-3859	2025-10-14 06:16:00	dolor ojo izquierdo	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	en_proceso	2025-10-14 06:17:18.073253
7	6	1	CONS-251020-2515	2025-10-20 00:53:00	DOLOR PUPILA IZQUIERDA E INCHAZON		20	20	20	j1	20	20	15	j1	2.00								50 mm	Bifocal	Completada	2025-10-20 00:54:21.434985
5	4	1	CONS-1760393600845	2025-10-13 19:13:00	CEGUERA TEMPORAL																				Pendiente	2025-10-13 19:13:48.54877
8	4	1	CONS-251026-6403	2025-10-26 04:20:00	DOLOR EN LAS PUPILAS	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	completada	2025-10-26 04:22:10.502629
\.


--
-- Data for Name: fondo_ojo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fondo_ojo (fondo_ojo_id, ficha_id, disco_optico_od, macula_od, vasos_od, retina_periferica_od, disco_optico_oi, macula_oi, vasos_oi, retina_periferica_oi, observaciones, fecha_examen, av_temp_sup_od, av_temp_inf_od, av_nasal_sup_od, av_nasal_inf_od, retina_od, excavacion_od, papila_detalle_od, fijacion_od, color_od, borde_od, av_temp_sup_oi, av_temp_inf_oi, av_nasal_sup_oi, av_nasal_inf_oi, retina_oi, excavacion_oi, papila_detalle_oi, fijacion_oi, color_oi, borde_oi, otros_detalles) FROM stdin;
\.


--
-- Data for Name: pacientes_medicos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pacientes_medicos (paciente_medico_id, cliente_id, numero_ficha, antecedentes_medicos, antecedentes_oculares, alergias, medicamentos_actuales, contacto_emergencia, telefono_emergencia, fecha_registro, estado) FROM stdin;
1	1	FM-TEST-001	Test	\N	\N	\N	\N	\N	2025-10-04 21:20:40.075605	t
2	2	FM-20251004213615	diabetes	cataratas	polvo	amoxicilina	marcela	+56 2 131 23435	2025-10-04 21:36:15.321102	t
3	5	FM-20251009171235	paciente con ceguera parcial 	cirugias oculares	cafeina	aspirina	raul 	+56 2 131 23435	2025-10-09 17:12:35.716368	t
4	6	FM-20251010222821	diabetes	cirugia ocular	alergico a las pastas	amoxicilina	elias gutierrez	3941379123	2025-10-10 22:28:21.122091	t
5	7	FM-20251013192546	hipertenso	cataratas	al polen 	paracetamol	joaquin jr	+593 78787878	2025-10-13 19:25:46.133362	t
6	14	FM-202510-577211	diabetes	glaucoma 	al sol	amoxicilina	jesus	593766786785	2025-10-14 05:54:06.022494	t
\.


--
-- Data for Name: parametros_clinicos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.parametros_clinicos (parametro_id, ficha_id, presion_sistolica, presion_diastolica, saturacion_o2, glucosa, trigliceridos, ttp, atp, colesterol, fecha_registro) FROM stdin;
\.


--
-- Data for Name: presion_intraocular; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.presion_intraocular (pio_id, ficha_id, pio_od, pio_oi, metodo_medicion, hora_medicion, observaciones, fecha_medicion) FROM stdin;
\.


--
-- Data for Name: productos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.productos (producto_id, nombre, descripcion, stock, precio_unitario, categoria, marca, sku, fecha_creacion, estado) FROM stdin;
2	Armazón Metálico Clásico	Armazón metálico para lentes ópticos	50	45000.00	Armazones	Ray-Ban	ARM001	2025-10-03 04:06:14.890247	t
3	Lentes Progresivos	Lentes progresivos premium	25	120000.00	Lentes Ópticos	Varilux	LP001	2025-10-03 04:06:14.890247	t
4	Gotas Lubricantes	Lágrimas artificiales para ojo seco	199	8500.00	Medicamentos	Refresh	MED001	2025-10-03 04:06:14.890247	t
6	Lentes de sol Oackley	Lentes de sol azules	99	70.00	\N	\N	\N	2025-10-05 01:09:09.410597	t
5	Limpiador de Lentes	Solución limpiadora para lentes	149	3500.00	Accesorios	OptiClean	ACC001	2025-10-03 04:06:14.890247	t
1	Lentes de Contacto Diarios	Lentes de contacto desechables diarios	99	25000.00	Lentes de Contacto	Acuvue	LC001	2025-10-03 04:06:14.890247	t
\.


--
-- Data for Name: proveedores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.proveedores (proveedor_id, codigo_proveedor, razon_social, nombre_comercial, rut, direccion, telefono, email, sitio_web, categoria_productos, condiciones_pago, plazo_pago_dias, descuento_volumen, representante_nombre, representante_telefono, representante_email, observaciones, estado, fecha_registro, fecha_actualizacion) FROM stdin;
2	PROV000002	Cristales y Accesorios S.A.	CristalAcc	96.789.123-4	Calle Comercial 567, Providencia, Santiago	+56 2 2345 6789	contacto@cristalacc.cl	\N	Cristales oftálmicos, Tratamientos antirreflex, Accesorios	Contado	0	3.50	Juan Carlos Pérez	+56 9 7654 3210	juan.perez@cristalacc.cl	Especialistas en cristales progresivos y tratamientos de alta gama.	t	2025-10-05 03:50:43.879202	2025-10-05 03:50:43.879202
3	PROV000003	Monturas Premium Chile Ltda.	MonturasPremium	77.456.789-0	Av. Vitacura 2890, Vitacura, Santiago	+56 2 2456 7890	ventas@monturaspremium.cl	\N	Monturas de lujo, Marcas internacionales, Colecciones exclusivas	60 días	60	7.50	Ana María Rodríguez	+56 9 6543 2109	ana.rodriguez@monturaspremium.cl	Importador exclusivo de marcas europeas premium. Excelente servicio post-venta.	t	2025-10-05 03:50:43.879202	2025-10-05 03:50:43.879202
4	PROV000004	Lentes de Contacto Express S.A.	LentExpress	78.654.321-9	Av. Apoquindo 4500, Las Condes, Santiago	+56 2 2567 8901	pedidos@lentexpress.cl	\N	Lentes de contacto diarios, Lentes tóricas, Soluciones	Crédito	45	4.25	Carlos Alberto Silva	+56 9 5432 1098	carlos.silva@lentexpress.cl	Entrega rápida de lentes de contacto. Stock permanente de las principales marcas.	t	2025-10-05 03:50:43.879202	2025-10-05 03:50:43.879202
5	PROV000005	Accesorios Ópticos del Sur Ltda.	AccesoriosÓpticos	79.987.654-3	Av. Irarrázaval 1234, Ñuñoa, Santiago	+56 2 2678 9012	ventas@accesoriosopticos.cl	\N	Estuches, Paños de limpieza, Cordones, Accesorios	Contado	0	2.00	Patricia Morales López	+56 9 4321 0987	patricia.morales@accesoriosopticos.cl	Amplia variedad de accesorios para ópticas. Precios competitivos.	t	2025-10-05 03:50:43.879202	2025-10-05 03:50:43.879202
1	PROV000001	Óptica Distribuidora Ltda.	OptiDistrib	76.123.456-K	Av. Las Condes 1234, Las Condes, Santiago	+56 2 2234 5678	ventas@optidistrib.cl	\N	Lentes de contacto, Monturas, Cristales	Crédito	30	5.00	María González Pérez	+56 9 8765 4321	maria.gonzalez@optidistrib.cl	Proveedor principal de lentes de contacto. Descuentos especiales por volumen.	f	2025-10-05 03:50:43.879202	2025-10-09 02:42:00.726424
\.


--
-- Data for Name: reflejos_pupilares; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reflejos_pupilares (reflejo_id, ficha_id, acomodativo_uno, fotomotor_uno, consensual_uno, acomodativo_dos, fotomotor_dos, consensual_dos, observaciones, fecha_registro) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (rol_id, nombre, descripcion, fecha_creacion, estado) FROM stdin;
1	Administrador	Acceso total al sistema	2025-10-03 04:06:14.890247	t
2	Médico Oftalmólogo	Acceso al módulo médico y consultas	2025-10-03 04:06:14.890247	t
3	Vendedor	Acceso al módulo comercial y ventas	2025-10-03 04:06:14.890247	t
4	Recepcionista	Registro de pacientes y citas	2025-10-03 04:06:14.890247	t
5	Supervisor	Acceso a reportes y supervisión	2025-10-03 04:06:14.890247	t
\.


--
-- Data for Name: tratamientos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tratamientos (tratamiento_id, ficha_id, medicamentos, tratamiento_no_farmacologico, recomendaciones, plan_seguimiento, proxima_cita, urgencia_seguimiento, fecha_tratamiento) FROM stdin;
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (usuario_id, rol_id, username, password, nombre, ap_pat, ap_mat, email, fecha_creacion, estado) FROM stdin;
1	1	admin	scrypt:32768:8:1$KQH7MubpMbHgSXhm$3d1e428fba9992274eb71c4f916a235c182cbc3f1c82c8fb06f4c9c88c58d3bdfcaba29d143fd34ffaf1505cc941857e73717c1d94c504bb493d3280ee6aaa8f	Administrador	Sistema		admin@opticamaipu.cl	2025-10-03 04:06:14.890247	t
2	1	orl	scrypt:32768:8:1$uAoJh87hfSA4DxED$6d85763f76b547ac54d5449b8c407c83d5e7416c66dde352e66cea3d852a4f3bc731544a49a1ad1fb42186c95c40f65104ad85b42441bbde8bf91507dacb2b10	orl	orl	orl	orl@gmail.com	2025-10-05 00:27:56.31118	t
\.


--
-- Data for Name: ventas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ventas (venta_id, cliente_id, usuario_id, fecha_venta, total, descuento, metodo_pago, observaciones, estado) FROM stdin;
1	11	1	2025-10-14 05:11:37.097987	8500.00	0.00	efectivo	\N	completada
2	12	1	2025-10-14 05:21:55.301116	70.00	0.00	efectivo	\N	completada
3	13	1	2025-10-14 05:30:07.037132	3500.00	0.00	efectivo	\N	completada
4	14	1	2025-10-14 08:26:43.322262	25000.00	0.00	efectivo	\N	completada
\.


--
-- Name: biomicroscopia_biomicroscopia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.biomicroscopia_biomicroscopia_id_seq', 1, false);


--
-- Name: campos_visuales_campo_visual_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.campos_visuales_campo_visual_id_seq', 1, false);


--
-- Name: clientes_cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clientes_cliente_id_seq', 14, true);


--
-- Name: detalle_ventas_detalle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.detalle_ventas_detalle_id_seq', 4, true);


--
-- Name: diagnosticos_diagnostico_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.diagnosticos_diagnostico_id_seq', 1, false);


--
-- Name: fichas_clinicas_ficha_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fichas_clinicas_ficha_id_seq', 8, true);


--
-- Name: fondo_ojo_fondo_ojo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fondo_ojo_fondo_ojo_id_seq', 1, false);


--
-- Name: pacientes_medicos_paciente_medico_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pacientes_medicos_paciente_medico_id_seq', 6, true);


--
-- Name: parametros_clinicos_parametro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.parametros_clinicos_parametro_id_seq', 1, false);


--
-- Name: presion_intraocular_pio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.presion_intraocular_pio_id_seq', 1, false);


--
-- Name: productos_producto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.productos_producto_id_seq', 6, true);


--
-- Name: proveedores_proveedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.proveedores_proveedor_id_seq', 5, true);


--
-- Name: reflejos_pupilares_reflejo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reflejos_pupilares_reflejo_id_seq', 1, false);


--
-- Name: roles_rol_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_rol_id_seq', 5, true);


--
-- Name: tratamientos_tratamiento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tratamientos_tratamiento_id_seq', 1, false);


--
-- Name: usuarios_usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_usuario_id_seq', 2, true);


--
-- Name: ventas_venta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ventas_venta_id_seq', 4, true);


--
-- Name: biomicroscopia biomicroscopia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.biomicroscopia
    ADD CONSTRAINT biomicroscopia_pkey PRIMARY KEY (biomicroscopia_id);


--
-- Name: campos_visuales campos_visuales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campos_visuales
    ADD CONSTRAINT campos_visuales_pkey PRIMARY KEY (campo_visual_id);


--
-- Name: clientes clientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY (cliente_id);


--
-- Name: clientes clientes_rut_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_rut_key UNIQUE (rut);


--
-- Name: detalle_ventas detalle_ventas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_ventas
    ADD CONSTRAINT detalle_ventas_pkey PRIMARY KEY (detalle_id);


--
-- Name: diagnosticos diagnosticos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diagnosticos
    ADD CONSTRAINT diagnosticos_pkey PRIMARY KEY (diagnostico_id);


--
-- Name: fichas_clinicas fichas_clinicas_numero_consulta_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fichas_clinicas
    ADD CONSTRAINT fichas_clinicas_numero_consulta_key UNIQUE (numero_consulta);


--
-- Name: fichas_clinicas fichas_clinicas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fichas_clinicas
    ADD CONSTRAINT fichas_clinicas_pkey PRIMARY KEY (ficha_id);


--
-- Name: fondo_ojo fondo_ojo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fondo_ojo
    ADD CONSTRAINT fondo_ojo_pkey PRIMARY KEY (fondo_ojo_id);


--
-- Name: pacientes_medicos pacientes_medicos_numero_ficha_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes_medicos
    ADD CONSTRAINT pacientes_medicos_numero_ficha_key UNIQUE (numero_ficha);


--
-- Name: pacientes_medicos pacientes_medicos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes_medicos
    ADD CONSTRAINT pacientes_medicos_pkey PRIMARY KEY (paciente_medico_id);


--
-- Name: parametros_clinicos parametros_clinicos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_clinicos
    ADD CONSTRAINT parametros_clinicos_pkey PRIMARY KEY (parametro_id);


--
-- Name: presion_intraocular presion_intraocular_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.presion_intraocular
    ADD CONSTRAINT presion_intraocular_pkey PRIMARY KEY (pio_id);


--
-- Name: productos productos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_pkey PRIMARY KEY (producto_id);


--
-- Name: productos productos_sku_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_sku_key UNIQUE (sku);


--
-- Name: proveedores proveedores_codigo_proveedor_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedores
    ADD CONSTRAINT proveedores_codigo_proveedor_key UNIQUE (codigo_proveedor);


--
-- Name: proveedores proveedores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedores
    ADD CONSTRAINT proveedores_pkey PRIMARY KEY (proveedor_id);


--
-- Name: proveedores proveedores_rut_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedores
    ADD CONSTRAINT proveedores_rut_key UNIQUE (rut);


--
-- Name: reflejos_pupilares reflejos_pupilares_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reflejos_pupilares
    ADD CONSTRAINT reflejos_pupilares_pkey PRIMARY KEY (reflejo_id);


--
-- Name: roles roles_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_nombre_key UNIQUE (nombre);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (rol_id);


--
-- Name: tratamientos tratamientos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tratamientos
    ADD CONSTRAINT tratamientos_pkey PRIMARY KEY (tratamiento_id);


--
-- Name: usuarios usuarios_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (usuario_id);


--
-- Name: usuarios usuarios_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_username_key UNIQUE (username);


--
-- Name: ventas ventas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_pkey PRIMARY KEY (venta_id);


--
-- Name: idx_clientes_nombres; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_clientes_nombres ON public.clientes USING btree (nombres, ap_pat);


--
-- Name: idx_clientes_rut; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_clientes_rut ON public.clientes USING btree (rut);


--
-- Name: idx_fichas_fecha; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fichas_fecha ON public.fichas_clinicas USING btree (fecha_consulta);


--
-- Name: idx_fichas_numero; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fichas_numero ON public.fichas_clinicas USING btree (numero_consulta);


--
-- Name: idx_pacientes_numero_ficha; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_pacientes_numero_ficha ON public.pacientes_medicos USING btree (numero_ficha);


--
-- Name: idx_parametros_clinicos_ficha; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_parametros_clinicos_ficha ON public.parametros_clinicos USING btree (ficha_id);


--
-- Name: idx_proveedores_codigo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_proveedores_codigo ON public.proveedores USING btree (codigo_proveedor);


--
-- Name: idx_proveedores_estado; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_proveedores_estado ON public.proveedores USING btree (estado);


--
-- Name: idx_proveedores_fecha_registro; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_proveedores_fecha_registro ON public.proveedores USING btree (fecha_registro);


--
-- Name: idx_proveedores_razon_social; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_proveedores_razon_social ON public.proveedores USING btree (razon_social);


--
-- Name: idx_proveedores_rut; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_proveedores_rut ON public.proveedores USING btree (rut);


--
-- Name: idx_reflejos_pupilares_ficha; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reflejos_pupilares_ficha ON public.reflejos_pupilares USING btree (ficha_id);


--
-- Name: idx_usuarios_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_usuarios_username ON public.usuarios USING btree (username);


--
-- Name: idx_ventas_fecha; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ventas_fecha ON public.ventas USING btree (fecha_venta);


--
-- Name: proveedores trigger_actualizar_fecha_proveedor; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_actualizar_fecha_proveedor BEFORE UPDATE ON public.proveedores FOR EACH ROW EXECUTE FUNCTION public.actualizar_fecha_modificacion_proveedor();


--
-- Name: proveedores trigger_generar_codigo_proveedor; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_generar_codigo_proveedor BEFORE INSERT ON public.proveedores FOR EACH ROW EXECUTE FUNCTION public.generar_codigo_proveedor();


--
-- Name: biomicroscopia biomicroscopia_ficha_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.biomicroscopia
    ADD CONSTRAINT biomicroscopia_ficha_id_fkey FOREIGN KEY (ficha_id) REFERENCES public.fichas_clinicas(ficha_id);


--
-- Name: campos_visuales campos_visuales_ficha_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campos_visuales
    ADD CONSTRAINT campos_visuales_ficha_id_fkey FOREIGN KEY (ficha_id) REFERENCES public.fichas_clinicas(ficha_id);


--
-- Name: detalle_ventas detalle_ventas_producto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_ventas
    ADD CONSTRAINT detalle_ventas_producto_id_fkey FOREIGN KEY (producto_id) REFERENCES public.productos(producto_id);


--
-- Name: detalle_ventas detalle_ventas_venta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_ventas
    ADD CONSTRAINT detalle_ventas_venta_id_fkey FOREIGN KEY (venta_id) REFERENCES public.ventas(venta_id);


--
-- Name: diagnosticos diagnosticos_ficha_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diagnosticos
    ADD CONSTRAINT diagnosticos_ficha_id_fkey FOREIGN KEY (ficha_id) REFERENCES public.fichas_clinicas(ficha_id);


--
-- Name: fichas_clinicas fichas_clinicas_paciente_medico_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fichas_clinicas
    ADD CONSTRAINT fichas_clinicas_paciente_medico_id_fkey FOREIGN KEY (paciente_medico_id) REFERENCES public.pacientes_medicos(paciente_medico_id);


--
-- Name: fichas_clinicas fichas_clinicas_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fichas_clinicas
    ADD CONSTRAINT fichas_clinicas_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(usuario_id);


--
-- Name: fondo_ojo fondo_ojo_ficha_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fondo_ojo
    ADD CONSTRAINT fondo_ojo_ficha_id_fkey FOREIGN KEY (ficha_id) REFERENCES public.fichas_clinicas(ficha_id);


--
-- Name: pacientes_medicos pacientes_medicos_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes_medicos
    ADD CONSTRAINT pacientes_medicos_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.clientes(cliente_id);


--
-- Name: parametros_clinicos parametros_clinicos_ficha_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parametros_clinicos
    ADD CONSTRAINT parametros_clinicos_ficha_id_fkey FOREIGN KEY (ficha_id) REFERENCES public.fichas_clinicas(ficha_id) ON DELETE CASCADE;


--
-- Name: presion_intraocular presion_intraocular_ficha_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.presion_intraocular
    ADD CONSTRAINT presion_intraocular_ficha_id_fkey FOREIGN KEY (ficha_id) REFERENCES public.fichas_clinicas(ficha_id);


--
-- Name: reflejos_pupilares reflejos_pupilares_ficha_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reflejos_pupilares
    ADD CONSTRAINT reflejos_pupilares_ficha_id_fkey FOREIGN KEY (ficha_id) REFERENCES public.fichas_clinicas(ficha_id) ON DELETE CASCADE;


--
-- Name: tratamientos tratamientos_ficha_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tratamientos
    ADD CONSTRAINT tratamientos_ficha_id_fkey FOREIGN KEY (ficha_id) REFERENCES public.fichas_clinicas(ficha_id);


--
-- Name: usuarios usuarios_rol_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_rol_id_fkey FOREIGN KEY (rol_id) REFERENCES public.roles(rol_id);


--
-- Name: ventas ventas_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.clientes(cliente_id);


--
-- Name: ventas ventas_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(usuario_id);


--
-- PostgreSQL database dump complete
--

