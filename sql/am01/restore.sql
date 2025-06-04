--
-- NOTE:
--
-- File paths need to be edited. Search for $$PATH$$ and
-- replace it with the path to the directory containing
-- the extracted data files.
--
--
-- PostgreSQL database dump
--

-- Dumped from database version 16.6
-- Dumped by pg_dump version 16.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE am01;
--
-- Name: am01; Type: DATABASE; Schema: -; Owner: aitamenni
--

CREATE DATABASE am01 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'es_ES.UTF-8';


ALTER DATABASE am01 OWNER TO aitamenni;

\connect am01

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: am01_sch; Type: SCHEMA; Schema: -; Owner: aitamenni
--

CREATE SCHEMA am01_sch;


ALTER SCHEMA am01_sch OWNER TO aitamenni;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cierre_ulcera; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.cierre_ulcera (
    id_secuencia integer NOT NULL,
    id_paciente character varying(50) NOT NULL,
    fecha timestamp without time zone NOT NULL,
    observaciones character varying(250),
    usuario_graba character varying(150) NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    usuario_modifica character varying(150),
    fecha_modifica timestamp without time zone
);


ALTER TABLE public.cierre_ulcera OWNER TO aitamenni;

--
-- Name: cierre_ulcera_id_secuencia_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.cierre_ulcera_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cierre_ulcera_id_secuencia_seq OWNER TO aitamenni;

--
-- Name: cierre_ulcera_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.cierre_ulcera_id_secuencia_seq OWNED BY public.cierre_ulcera.id_secuencia;


--
-- Name: constantes; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.constantes (
    id_constantes integer NOT NULL,
    id_secuencia_temp integer NOT NULL,
    id_secuencia_pa integer NOT NULL,
    id_secuencia_fc integer NOT NULL,
    id_secuencia_fr integer NOT NULL,
    id_secuencia_so integer NOT NULL,
    id_paciente character varying(50) NOT NULL,
    fecha_medicion timestamp without time zone
);


ALTER TABLE public.constantes OWNER TO aitamenni;

--
-- Name: constantes_id_constantes_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.constantes_id_constantes_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.constantes_id_constantes_seq OWNER TO aitamenni;

--
-- Name: constantes_id_constantes_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.constantes_id_constantes_seq OWNED BY public.constantes.id_constantes;


--
-- Name: constantes_id_secuencia_fc_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.constantes_id_secuencia_fc_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.constantes_id_secuencia_fc_seq OWNER TO aitamenni;

--
-- Name: constantes_id_secuencia_fc_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.constantes_id_secuencia_fc_seq OWNED BY public.constantes.id_secuencia_fc;


--
-- Name: constantes_id_secuencia_fr_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.constantes_id_secuencia_fr_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.constantes_id_secuencia_fr_seq OWNER TO aitamenni;

--
-- Name: constantes_id_secuencia_fr_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.constantes_id_secuencia_fr_seq OWNED BY public.constantes.id_secuencia_fr;


--
-- Name: constantes_id_secuencia_pa_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.constantes_id_secuencia_pa_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.constantes_id_secuencia_pa_seq OWNER TO aitamenni;

--
-- Name: constantes_id_secuencia_pa_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.constantes_id_secuencia_pa_seq OWNED BY public.constantes.id_secuencia_pa;


--
-- Name: constantes_id_secuencia_so_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.constantes_id_secuencia_so_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.constantes_id_secuencia_so_seq OWNER TO aitamenni;

--
-- Name: constantes_id_secuencia_so_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.constantes_id_secuencia_so_seq OWNED BY public.constantes.id_secuencia_so;


--
-- Name: constantes_id_secuencia_temp_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.constantes_id_secuencia_temp_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.constantes_id_secuencia_temp_seq OWNER TO aitamenni;

--
-- Name: constantes_id_secuencia_temp_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.constantes_id_secuencia_temp_seq OWNED BY public.constantes.id_secuencia_temp;


--
-- Name: contencion; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.contencion (
    id_secuencia integer NOT NULL,
    id_paciente character varying(50) NOT NULL,
    tipo_apoyo character varying(50) NOT NULL,
    anyo integer NOT NULL,
    mes character varying(2) NOT NULL,
    motivo character varying(250),
    tipo_contencion character varying(250) NOT NULL,
    numero_puntos character varying(250) NOT NULL,
    fecha_inicio timestamp without time zone NOT NULL,
    hora_inicio integer NOT NULL,
    usuario_registro_inicio character varying(150) NOT NULL,
    fecha_fin timestamp without time zone,
    hora_fin integer NOT NULL,
    usuario_registro_fin character varying(250),
    duracion character varying(10),
    frecuencia_revision character varying(50),
    descripcion character varying(250),
    observaciones character varying(250),
    usuario_graba character varying(150) NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    usuario_modifica character varying(150),
    fecha_modifica timestamp without time zone
);


ALTER TABLE public.contencion OWNER TO aitamenni;

--
-- Name: contencion_anyo_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.contencion_anyo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contencion_anyo_seq OWNER TO aitamenni;

--
-- Name: contencion_anyo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.contencion_anyo_seq OWNED BY public.contencion.anyo;


--
-- Name: contencion_hora_fin_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.contencion_hora_fin_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contencion_hora_fin_seq OWNER TO aitamenni;

--
-- Name: contencion_hora_fin_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.contencion_hora_fin_seq OWNED BY public.contencion.hora_fin;


--
-- Name: contencion_hora_inicio_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.contencion_hora_inicio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contencion_hora_inicio_seq OWNER TO aitamenni;

--
-- Name: contencion_hora_inicio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.contencion_hora_inicio_seq OWNED BY public.contencion.hora_inicio;


--
-- Name: contencion_id_secuencia_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.contencion_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contencion_id_secuencia_seq OWNER TO aitamenni;

--
-- Name: contencion_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.contencion_id_secuencia_seq OWNED BY public.contencion.id_secuencia;


--
-- Name: cuidado_ulcera; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.cuidado_ulcera (
    id_secuencia integer NOT NULL,
    id_paciente character varying(50) NOT NULL,
    anyo character varying(4) NOT NULL,
    mes character varying(2) NOT NULL,
    dia character varying(2) NOT NULL,
    usuario_graba character varying(150) NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    usuario_modifica character varying(150),
    fecha_modifica timestamp without time zone
);


ALTER TABLE public.cuidado_ulcera OWNER TO aitamenni;

--
-- Name: cuidado_ulcera_id_secuencia_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.cuidado_ulcera_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cuidado_ulcera_id_secuencia_seq OWNER TO aitamenni;

--
-- Name: cuidado_ulcera_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.cuidado_ulcera_id_secuencia_seq OWNED BY public.cuidado_ulcera.id_secuencia;


--
-- Name: deposiciones; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.deposiciones (
    id_secuencia integer NOT NULL,
    id_paciente character varying(50) NOT NULL,
    valor character varying(50) NOT NULL,
    fecha_medicion timestamp without time zone NOT NULL,
    usuario_graba character varying(150) NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    usuario_modifica character varying(150),
    fecha_modifica timestamp without time zone,
    observaciones character varying(250)
);


ALTER TABLE public.deposiciones OWNER TO aitamenni;

--
-- Name: deposiciones_id_secuencia_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.deposiciones_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.deposiciones_id_secuencia_seq OWNER TO aitamenni;

--
-- Name: deposiciones_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.deposiciones_id_secuencia_seq OWNED BY public.deposiciones.id_secuencia;


--
-- Name: diuresis; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.diuresis (
    id_secuencia integer NOT NULL,
    id_paciente character varying(50) NOT NULL,
    valor character varying(50) NOT NULL,
    vaciado_bolsa character varying(50) NOT NULL,
    cambio_bolsa character varying(50) NOT NULL,
    total_diario integer NOT NULL,
    observaciones character varying(250),
    fecha_medicion timestamp without time zone NOT NULL,
    usuario_graba character varying(150) NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    usuario_modifica character varying(150),
    fecha_modifica timestamp without time zone
);


ALTER TABLE public.diuresis OWNER TO aitamenni;

--
-- Name: diuresis_id_secuencia_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.diuresis_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.diuresis_id_secuencia_seq OWNER TO aitamenni;

--
-- Name: diuresis_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.diuresis_id_secuencia_seq OWNED BY public.diuresis.id_secuencia;


--
-- Name: electrocardiograma; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.electrocardiograma (
    id_secuencia integer NOT NULL,
    id_paciente character varying(50),
    unidad character varying(150) NOT NULL,
    fecha_medicion timestamp without time zone NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    idmonitor character varying(150) NOT NULL,
    fecha_modifica timestamp without time zone,
    usuario_modifica character varying(150),
    nombrearchivo character varying(150) NOT NULL
);


ALTER TABLE public.electrocardiograma OWNER TO aitamenni;

--
-- Name: electrocardiograma_id_secuencia_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.electrocardiograma_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.electrocardiograma_id_secuencia_seq OWNER TO aitamenni;

--
-- Name: electrocardiograma_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.electrocardiograma_id_secuencia_seq OWNED BY public.electrocardiograma.id_secuencia;


--
-- Name: fotos_hospwin; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.fotos_hospwin (
    id_paciente character varying(50) NOT NULL,
    f_actual timestamp without time zone,
    tipo character varying(3),
    foto bytea,
    observaciones character varying(250)
);


ALTER TABLE public.fotos_hospwin OWNER TO aitamenni;

--
-- Name: frecuencia_cardiaca; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.frecuencia_cardiaca (
    id_secuencia_fc integer NOT NULL,
    id_paciente_fc character varying(50) NOT NULL,
    valor_fc double precision NOT NULL,
    fecha_medicion_fc timestamp without time zone NOT NULL,
    observaciones_fc character varying(250),
    usuario_graba_fc character varying(150) NOT NULL,
    fecha_registro_fc timestamp without time zone,
    usuario_modifica_fc character varying(150),
    fecha_modifica_fc timestamp without time zone
);


ALTER TABLE public.frecuencia_cardiaca OWNER TO aitamenni;

--
-- Name: frecuencia_cardiaca_id_secuencia_fc_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.frecuencia_cardiaca_id_secuencia_fc_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.frecuencia_cardiaca_id_secuencia_fc_seq OWNER TO aitamenni;

--
-- Name: frecuencia_cardiaca_id_secuencia_fc_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.frecuencia_cardiaca_id_secuencia_fc_seq OWNED BY public.frecuencia_cardiaca.id_secuencia_fc;


--
-- Name: frecuencia_respiratoria; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.frecuencia_respiratoria (
    id_secuencia_fr integer NOT NULL,
    id_paciente_fr character varying(50) NOT NULL,
    valor_fr double precision NOT NULL,
    fecha_medicion_fr timestamp without time zone NOT NULL,
    observaciones_fr character varying(250),
    usuario_graba_fr character varying(150) NOT NULL,
    fecha_registro_fr timestamp without time zone NOT NULL,
    usuario_modifica_fr character varying(150),
    fecha_modifica_fr timestamp without time zone
);


ALTER TABLE public.frecuencia_respiratoria OWNER TO aitamenni;

--
-- Name: frecuencia_respiratoria_id_secuencia_fr_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.frecuencia_respiratoria_id_secuencia_fr_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.frecuencia_respiratoria_id_secuencia_fr_seq OWNER TO aitamenni;

--
-- Name: frecuencia_respiratoria_id_secuencia_fr_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.frecuencia_respiratoria_id_secuencia_fr_seq OWNED BY public.frecuencia_respiratoria.id_secuencia_fr;


--
-- Name: glucosa; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.glucosa (
    id_secuencia integer NOT NULL,
    id_paciente character varying(50) NOT NULL,
    valor double precision NOT NULL,
    escala character varying(250) NOT NULL,
    fecha_medicion timestamp without time zone NOT NULL,
    observaciones character varying(250),
    usuario_graba character varying(150) NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    usuario_modifica character varying(150),
    fecha_modifica timestamp without time zone,
    hemoglob_glucosilada double precision
);


ALTER TABLE public.glucosa OWNER TO aitamenni;

--
-- Name: glucosa_id_secuencia_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.glucosa_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.glucosa_id_secuencia_seq OWNER TO aitamenni;

--
-- Name: glucosa_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.glucosa_id_secuencia_seq OWNED BY public.glucosa.id_secuencia;


--
-- Name: grupousu_hospwin; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.grupousu_hospwin (
    id_usuario character varying(50),
    id_grupo character varying(4) NOT NULL
);


ALTER TABLE public.grupousu_hospwin OWNER TO aitamenni;

--
-- Name: medicacion; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.medicacion (
    id_secuencia integer NOT NULL,
    id_paciente character varying(50) NOT NULL,
    medicacion character varying(50) NOT NULL,
    fecha_dispensacion timestamp without time zone NOT NULL,
    hora_dispensacion character varying(4) NOT NULL,
    observaciones character varying(250),
    usuario_graba character varying(150) NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    usuario_modifica character varying(150),
    fecha_modifica timestamp without time zone
);


ALTER TABLE public.medicacion OWNER TO aitamenni;

--
-- Name: medicacion_id_secuencia_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.medicacion_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.medicacion_id_secuencia_seq OWNER TO aitamenni;

--
-- Name: medicacion_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.medicacion_id_secuencia_seq OWNED BY public.medicacion.id_secuencia;


--
-- Name: menstruacion; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.menstruacion (
    id_secuencia integer NOT NULL,
    id_paciente character varying(10) NOT NULL,
    anyo character varying(4) NOT NULL,
    mes character varying(2) NOT NULL,
    fecha_inicio character varying(11) NOT NULL,
    observaciones character varying(250),
    usuario_graba character varying(150) NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    usuario_modifica character varying(150),
    fecha_modifica timestamp without time zone,
    fecha_fin character varying(11)
);


ALTER TABLE public.menstruacion OWNER TO aitamenni;

--
-- Name: menstruacion_id_secuencia_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.menstruacion_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.menstruacion_id_secuencia_seq OWNER TO aitamenni;

--
-- Name: menstruacion_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.menstruacion_id_secuencia_seq OWNED BY public.menstruacion.id_secuencia;


--
-- Name: monitor; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.monitor (
    id_secuencia integer NOT NULL,
    id_monitor character varying(50) NOT NULL,
    descripcion character varying(250),
    fecha_registro timestamp without time zone NOT NULL,
    usuario_graba character varying(50) NOT NULL,
    fecha_modifica timestamp without time zone,
    usuario_modifica character varying(50),
    estado character varying(1) NOT NULL,
    unidad character varying(150)
);


ALTER TABLE public.monitor OWNER TO aitamenni;

--
-- Name: monitores_activos; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.monitores_activos (
    id_monitor character varying(50) NOT NULL,
    id_paciente character varying(50) NOT NULL,
    usuario character varying(250),
    fecha_conexion timestamp without time zone,
    estado character varying(1)
);


ALTER TABLE public.monitores_activos OWNER TO aitamenni;

--
-- Name: pacientes_hospwin; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.pacientes_hospwin (
    id_paciente character varying(50) NOT NULL,
    numehist character varying(10),
    niu character varying(10),
    nombre character varying(50),
    apellido1 character varying(50),
    apellido2 character varying(50),
    fonetica character varying(50),
    situacion character varying(2),
    situhpar character varying(2),
    situcext character varying(2),
    numecama character varying(5),
    unihpar character varying(4),
    unicext character varying(4),
    equipo character varying(4),
    equipohpar character varying(4),
    equipocext character varying(4),
    cuentacontable character varying(12),
    cuentaentidad character varying(12),
    cuentabancaria character varying(20),
    formapago character varying(2),
    sexo character varying(1),
    estacivil character varying(50)
);


ALTER TABLE public.pacientes_hospwin OWNER TO aitamenni;

--
-- Name: peso; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.peso (
    id_secuencia integer NOT NULL,
    id_paciente character varying(50) NOT NULL,
    valor double precision NOT NULL,
    imc double precision NOT NULL,
    escala character varying(250) NOT NULL,
    fecha_medicion timestamp without time zone NOT NULL,
    observaciones character varying(250),
    usuario_graba character varying(150) NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    usuario_modifica character varying(150),
    fecha_modifica timestamp without time zone
);


ALTER TABLE public.peso OWNER TO aitamenni;

--
-- Name: peso_id_secuencia_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.peso_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.peso_id_secuencia_seq OWNER TO aitamenni;

--
-- Name: peso_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.peso_id_secuencia_seq OWNED BY public.peso.id_secuencia;


--
-- Name: presion_arterial; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.presion_arterial (
    id_secuencia_pa integer NOT NULL,
    id_paciente_pa character varying(50) NOT NULL,
    diastolica_pa double precision NOT NULL,
    fecha_medicion_pa timestamp without time zone NOT NULL,
    observaciones_pa character varying(250),
    usuario_graba_pa character varying(150) NOT NULL,
    fecha_registro_pa timestamp without time zone,
    usuario_modifica_pa character varying(150),
    fecha_modifica_pa timestamp without time zone,
    sistolica_pa double precision NOT NULL
);


ALTER TABLE public.presion_arterial OWNER TO aitamenni;

--
-- Name: presion_arterial_id_secuencia_pa_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.presion_arterial_id_secuencia_pa_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.presion_arterial_id_secuencia_pa_seq OWNER TO aitamenni;

--
-- Name: presion_arterial_id_secuencia_pa_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.presion_arterial_id_secuencia_pa_seq OWNED BY public.presion_arterial.id_secuencia_pa;


--
-- Name: saturacion_oxigeno; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.saturacion_oxigeno (
    id_secuencia_so integer NOT NULL,
    id_paciente_so character varying(50) NOT NULL,
    valor_so double precision NOT NULL,
    fecha_medicion_so timestamp without time zone NOT NULL,
    observaciones_so character varying(250),
    usuario_graba_so character varying(150) NOT NULL,
    fecha_registro_so timestamp without time zone,
    usuario_modifica_so character varying(150),
    fecha_modifica_so timestamp without time zone
);


ALTER TABLE public.saturacion_oxigeno OWNER TO aitamenni;

--
-- Name: saturacion_oxigeno_id_secuencia_so_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.saturacion_oxigeno_id_secuencia_so_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.saturacion_oxigeno_id_secuencia_so_seq OWNER TO aitamenni;

--
-- Name: saturacion_oxigeno_id_secuencia_so_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.saturacion_oxigeno_id_secuencia_so_seq OWNED BY public.saturacion_oxigeno.id_secuencia_so;


--
-- Name: talla; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.talla (
    id_secuencia integer NOT NULL,
    id_paciente character varying(50) NOT NULL,
    valor double precision NOT NULL,
    fecha_medicion timestamp without time zone NOT NULL,
    observaciones character varying(250),
    usuario_graba character varying(150) NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    usuario_modifica character varying(150),
    fecha_modifica timestamp without time zone
);


ALTER TABLE public.talla OWNER TO aitamenni;

--
-- Name: talla_id_secuencia_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.talla_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.talla_id_secuencia_seq OWNER TO aitamenni;

--
-- Name: talla_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.talla_id_secuencia_seq OWNED BY public.talla.id_secuencia;


--
-- Name: tarjeta; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.tarjeta (
    idtarjeta character varying(50) NOT NULL,
    idusuario character varying(50) NOT NULL
);


ALTER TABLE public.tarjeta OWNER TO aitamenni;

--
-- Name: temperatura; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.temperatura (
    id_secuencia_temp integer NOT NULL,
    id_paciente_temp character varying(50) NOT NULL,
    valor_temp double precision NOT NULL,
    escala_temp character varying(250) NOT NULL,
    fecha_medicion_temp timestamp without time zone NOT NULL,
    observaciones_temp character varying(250),
    usuario_graba_temp character varying(150) NOT NULL,
    fecha_registro_temp timestamp without time zone NOT NULL,
    usuario_modifica_temp character varying(150),
    fecha_modifica_temp timestamp without time zone
);


ALTER TABLE public.temperatura OWNER TO aitamenni;

--
-- Name: temperatura_id_secuencia_temp_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.temperatura_id_secuencia_temp_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.temperatura_id_secuencia_temp_seq OWNER TO aitamenni;

--
-- Name: temperatura_id_secuencia_temp_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.temperatura_id_secuencia_temp_seq OWNED BY public.temperatura.id_secuencia_temp;


--
-- Name: tipo_sonda; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.tipo_sonda (
    id_secuencia integer NOT NULL,
    id_paciente character varying(50) NOT NULL,
    tipo_sonda character varying(50) NOT NULL,
    fecha_colocacion timestamp without time zone NOT NULL,
    usuario_graba character varying(150) NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    usuario_modifica character varying(150),
    fecha_modifica timestamp without time zone
);


ALTER TABLE public.tipo_sonda OWNER TO aitamenni;

--
-- Name: tipo_sonda_id_secuencia_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.tipo_sonda_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tipo_sonda_id_secuencia_seq OWNER TO aitamenni;

--
-- Name: tipo_sonda_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.tipo_sonda_id_secuencia_seq OWNED BY public.tipo_sonda.id_secuencia;


--
-- Name: tratamiento_ulcera; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.tratamiento_ulcera (
    id_secuencia integer NOT NULL,
    id_paciente character varying(50) NOT NULL,
    fecha timestamp without time zone NOT NULL,
    estado character varying(100) NOT NULL,
    fecha_deteccion timestamp without time zone NOT NULL,
    descripccion character varying(250) NOT NULL,
    usuario_graba character varying(150) NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    usuario_modifica character varying(150),
    fecha_modifica timestamp without time zone
);


ALTER TABLE public.tratamiento_ulcera OWNER TO aitamenni;

--
-- Name: tratamiento_ulcera_id_secuencia_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.tratamiento_ulcera_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tratamiento_ulcera_id_secuencia_seq OWNER TO aitamenni;

--
-- Name: tratamiento_ulcera_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.tratamiento_ulcera_id_secuencia_seq OWNED BY public.tratamiento_ulcera.id_secuencia;


--
-- Name: ulceras; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.ulceras (
    id_secuencia integer NOT NULL,
    id_paciente character varying(50) NOT NULL,
    localizacion character varying(100) NOT NULL,
    tipo character varying(50) NOT NULL,
    fecha_deteccion timestamp without time zone NOT NULL,
    procedencia character varying(100) NOT NULL,
    usuario_graba character varying(50) NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    usuario_modifica character varying(50),
    fecha_modifica timestamp without time zone
);


ALTER TABLE public.ulceras OWNER TO aitamenni;

--
-- Name: ulceras_id_secuencia_seq; Type: SEQUENCE; Schema: public; Owner: aitamenni
--

CREATE SEQUENCE public.ulceras_id_secuencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ulceras_id_secuencia_seq OWNER TO aitamenni;

--
-- Name: ulceras_id_secuencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aitamenni
--

ALTER SEQUENCE public.ulceras_id_secuencia_seq OWNED BY public.ulceras.id_secuencia;


--
-- Name: usuario_hospwin; Type: TABLE; Schema: public; Owner: aitamenni
--

CREATE TABLE public.usuario_hospwin (
    id_usuario character varying(150) NOT NULL,
    apellido1 character varying(50),
    apellido2 character varying(50),
    nombre character varying(50),
    clave character varying(20),
    activo character varying(1),
    codigo character varying(10),
    operador character varying(10),
    idpersonal character varying(5),
    consupervision character varying(1),
    claveage character varying(33),
    fecha_ultimo_cambio_clave timestamp without time zone
);


ALTER TABLE public.usuario_hospwin OWNER TO aitamenni;

--
-- Name: cierre_ulcera id_secuencia; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.cierre_ulcera ALTER COLUMN id_secuencia SET DEFAULT nextval('public.cierre_ulcera_id_secuencia_seq'::regclass);


--
-- Name: constantes id_constantes; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.constantes ALTER COLUMN id_constantes SET DEFAULT nextval('public.constantes_id_constantes_seq'::regclass);


--
-- Name: constantes id_secuencia_temp; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.constantes ALTER COLUMN id_secuencia_temp SET DEFAULT nextval('public.constantes_id_secuencia_temp_seq'::regclass);


--
-- Name: constantes id_secuencia_pa; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.constantes ALTER COLUMN id_secuencia_pa SET DEFAULT nextval('public.constantes_id_secuencia_pa_seq'::regclass);


--
-- Name: constantes id_secuencia_fc; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.constantes ALTER COLUMN id_secuencia_fc SET DEFAULT nextval('public.constantes_id_secuencia_fc_seq'::regclass);


--
-- Name: constantes id_secuencia_fr; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.constantes ALTER COLUMN id_secuencia_fr SET DEFAULT nextval('public.constantes_id_secuencia_fr_seq'::regclass);


--
-- Name: constantes id_secuencia_so; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.constantes ALTER COLUMN id_secuencia_so SET DEFAULT nextval('public.constantes_id_secuencia_so_seq'::regclass);


--
-- Name: contencion id_secuencia; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.contencion ALTER COLUMN id_secuencia SET DEFAULT nextval('public.contencion_id_secuencia_seq'::regclass);


--
-- Name: contencion anyo; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.contencion ALTER COLUMN anyo SET DEFAULT nextval('public.contencion_anyo_seq'::regclass);


--
-- Name: contencion hora_inicio; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.contencion ALTER COLUMN hora_inicio SET DEFAULT nextval('public.contencion_hora_inicio_seq'::regclass);


--
-- Name: contencion hora_fin; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.contencion ALTER COLUMN hora_fin SET DEFAULT nextval('public.contencion_hora_fin_seq'::regclass);


--
-- Name: cuidado_ulcera id_secuencia; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.cuidado_ulcera ALTER COLUMN id_secuencia SET DEFAULT nextval('public.cuidado_ulcera_id_secuencia_seq'::regclass);


--
-- Name: deposiciones id_secuencia; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.deposiciones ALTER COLUMN id_secuencia SET DEFAULT nextval('public.deposiciones_id_secuencia_seq'::regclass);


--
-- Name: diuresis id_secuencia; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.diuresis ALTER COLUMN id_secuencia SET DEFAULT nextval('public.diuresis_id_secuencia_seq'::regclass);


--
-- Name: electrocardiograma id_secuencia; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.electrocardiograma ALTER COLUMN id_secuencia SET DEFAULT nextval('public.electrocardiograma_id_secuencia_seq'::regclass);


--
-- Name: frecuencia_cardiaca id_secuencia_fc; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.frecuencia_cardiaca ALTER COLUMN id_secuencia_fc SET DEFAULT nextval('public.frecuencia_cardiaca_id_secuencia_fc_seq'::regclass);


--
-- Name: frecuencia_respiratoria id_secuencia_fr; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.frecuencia_respiratoria ALTER COLUMN id_secuencia_fr SET DEFAULT nextval('public.frecuencia_respiratoria_id_secuencia_fr_seq'::regclass);


--
-- Name: glucosa id_secuencia; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.glucosa ALTER COLUMN id_secuencia SET DEFAULT nextval('public.glucosa_id_secuencia_seq'::regclass);


--
-- Name: medicacion id_secuencia; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.medicacion ALTER COLUMN id_secuencia SET DEFAULT nextval('public.medicacion_id_secuencia_seq'::regclass);


--
-- Name: menstruacion id_secuencia; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.menstruacion ALTER COLUMN id_secuencia SET DEFAULT nextval('public.menstruacion_id_secuencia_seq'::regclass);


--
-- Name: peso id_secuencia; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.peso ALTER COLUMN id_secuencia SET DEFAULT nextval('public.peso_id_secuencia_seq'::regclass);


--
-- Name: presion_arterial id_secuencia_pa; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.presion_arterial ALTER COLUMN id_secuencia_pa SET DEFAULT nextval('public.presion_arterial_id_secuencia_pa_seq'::regclass);


--
-- Name: saturacion_oxigeno id_secuencia_so; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.saturacion_oxigeno ALTER COLUMN id_secuencia_so SET DEFAULT nextval('public.saturacion_oxigeno_id_secuencia_so_seq'::regclass);


--
-- Name: talla id_secuencia; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.talla ALTER COLUMN id_secuencia SET DEFAULT nextval('public.talla_id_secuencia_seq'::regclass);


--
-- Name: temperatura id_secuencia_temp; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.temperatura ALTER COLUMN id_secuencia_temp SET DEFAULT nextval('public.temperatura_id_secuencia_temp_seq'::regclass);


--
-- Name: tipo_sonda id_secuencia; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.tipo_sonda ALTER COLUMN id_secuencia SET DEFAULT nextval('public.tipo_sonda_id_secuencia_seq'::regclass);


--
-- Name: tratamiento_ulcera id_secuencia; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.tratamiento_ulcera ALTER COLUMN id_secuencia SET DEFAULT nextval('public.tratamiento_ulcera_id_secuencia_seq'::regclass);


--
-- Name: ulceras id_secuencia; Type: DEFAULT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.ulceras ALTER COLUMN id_secuencia SET DEFAULT nextval('public.ulceras_id_secuencia_seq'::regclass);


--
-- Data for Name: cierre_ulcera; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.cierre_ulcera (id_secuencia, id_paciente, fecha, observaciones, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM stdin;
\.
COPY public.cierre_ulcera (id_secuencia, id_paciente, fecha, observaciones, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM '$$PATH$$/4522.dat';

--
-- Data for Name: constantes; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.constantes (id_constantes, id_secuencia_temp, id_secuencia_pa, id_secuencia_fc, id_secuencia_fr, id_secuencia_so, id_paciente, fecha_medicion) FROM stdin;
\.
COPY public.constantes (id_constantes, id_secuencia_temp, id_secuencia_pa, id_secuencia_fc, id_secuencia_fr, id_secuencia_so, id_paciente, fecha_medicion) FROM '$$PATH$$/4546.dat';

--
-- Data for Name: contencion; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.contencion (id_secuencia, id_paciente, tipo_apoyo, anyo, mes, motivo, tipo_contencion, numero_puntos, fecha_inicio, hora_inicio, usuario_registro_inicio, fecha_fin, hora_fin, usuario_registro_fin, duracion, frecuencia_revision, descripcion, observaciones, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM stdin;
\.
COPY public.contencion (id_secuencia, id_paciente, tipo_apoyo, anyo, mes, motivo, tipo_contencion, numero_puntos, fecha_inicio, hora_inicio, usuario_registro_inicio, fecha_fin, hora_fin, usuario_registro_fin, duracion, frecuencia_revision, descripcion, observaciones, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM '$$PATH$$/4514.dat';

--
-- Data for Name: cuidado_ulcera; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.cuidado_ulcera (id_secuencia, id_paciente, anyo, mes, dia, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM stdin;
\.
COPY public.cuidado_ulcera (id_secuencia, id_paciente, anyo, mes, dia, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM '$$PATH$$/4520.dat';

--
-- Data for Name: deposiciones; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.deposiciones (id_secuencia, id_paciente, valor, fecha_medicion, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica, observaciones) FROM stdin;
\.
COPY public.deposiciones (id_secuencia, id_paciente, valor, fecha_medicion, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica, observaciones) FROM '$$PATH$$/4501.dat';

--
-- Data for Name: diuresis; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.diuresis (id_secuencia, id_paciente, valor, vaciado_bolsa, cambio_bolsa, total_diario, observaciones, fecha_medicion, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM stdin;
\.
COPY public.diuresis (id_secuencia, id_paciente, valor, vaciado_bolsa, cambio_bolsa, total_diario, observaciones, fecha_medicion, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM '$$PATH$$/4503.dat';

--
-- Data for Name: electrocardiograma; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.electrocardiograma (id_secuencia, id_paciente, unidad, fecha_medicion, fecha_registro, idmonitor, fecha_modifica, usuario_modifica, nombrearchivo) FROM stdin;
\.
COPY public.electrocardiograma (id_secuencia, id_paciente, unidad, fecha_medicion, fecha_registro, idmonitor, fecha_modifica, usuario_modifica, nombrearchivo) FROM '$$PATH$$/4532.dat';

--
-- Data for Name: fotos_hospwin; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.fotos_hospwin (id_paciente, f_actual, tipo, foto, observaciones) FROM stdin;
\.
COPY public.fotos_hospwin (id_paciente, f_actual, tipo, foto, observaciones) FROM '$$PATH$$/4534.dat';

--
-- Data for Name: frecuencia_cardiaca; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.frecuencia_cardiaca (id_secuencia_fc, id_paciente_fc, valor_fc, fecha_medicion_fc, observaciones_fc, usuario_graba_fc, fecha_registro_fc, usuario_modifica_fc, fecha_modifica_fc) FROM stdin;
\.
COPY public.frecuencia_cardiaca (id_secuencia_fc, id_paciente_fc, valor_fc, fecha_medicion_fc, observaciones_fc, usuario_graba_fc, fecha_registro_fc, usuario_modifica_fc, fecha_modifica_fc) FROM '$$PATH$$/4530.dat';

--
-- Data for Name: frecuencia_respiratoria; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.frecuencia_respiratoria (id_secuencia_fr, id_paciente_fr, valor_fr, fecha_medicion_fr, observaciones_fr, usuario_graba_fr, fecha_registro_fr, usuario_modifica_fr, fecha_modifica_fr) FROM stdin;
\.
COPY public.frecuencia_respiratoria (id_secuencia_fr, id_paciente_fr, valor_fr, fecha_medicion_fr, observaciones_fr, usuario_graba_fr, fecha_registro_fr, usuario_modifica_fr, fecha_modifica_fr) FROM '$$PATH$$/4524.dat';

--
-- Data for Name: glucosa; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.glucosa (id_secuencia, id_paciente, valor, escala, fecha_medicion, observaciones, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica, hemoglob_glucosilada) FROM stdin;
\.
COPY public.glucosa (id_secuencia, id_paciente, valor, escala, fecha_medicion, observaciones, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica, hemoglob_glucosilada) FROM '$$PATH$$/4497.dat';

--
-- Data for Name: grupousu_hospwin; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.grupousu_hospwin (id_usuario, id_grupo) FROM stdin;
\.
COPY public.grupousu_hospwin (id_usuario, id_grupo) FROM '$$PATH$$/4535.dat';

--
-- Data for Name: medicacion; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.medicacion (id_secuencia, id_paciente, medicacion, fecha_dispensacion, hora_dispensacion, observaciones, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM stdin;
\.
COPY public.medicacion (id_secuencia, id_paciente, medicacion, fecha_dispensacion, hora_dispensacion, observaciones, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM '$$PATH$$/4509.dat';

--
-- Data for Name: menstruacion; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.menstruacion (id_secuencia, id_paciente, anyo, mes, fecha_inicio, observaciones, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica, fecha_fin) FROM stdin;
\.
COPY public.menstruacion (id_secuencia, id_paciente, anyo, mes, fecha_inicio, observaciones, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica, fecha_fin) FROM '$$PATH$$/4507.dat';

--
-- Data for Name: monitor; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.monitor (id_secuencia, id_monitor, descripcion, fecha_registro, usuario_graba, fecha_modifica, usuario_modifica, estado, unidad) FROM stdin;
\.
COPY public.monitor (id_secuencia, id_monitor, descripcion, fecha_registro, usuario_graba, fecha_modifica, usuario_modifica, estado, unidad) FROM '$$PATH$$/4539.dat';

--
-- Data for Name: monitores_activos; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.monitores_activos (id_monitor, id_paciente, usuario, fecha_conexion, estado) FROM stdin;
\.
COPY public.monitores_activos (id_monitor, id_paciente, usuario, fecha_conexion, estado) FROM '$$PATH$$/4537.dat';

--
-- Data for Name: pacientes_hospwin; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.pacientes_hospwin (id_paciente, numehist, niu, nombre, apellido1, apellido2, fonetica, situacion, situhpar, situcext, numecama, unihpar, unicext, equipo, equipohpar, equipocext, cuentacontable, cuentaentidad, cuentabancaria, formapago, sexo, estacivil) FROM stdin;
\.
COPY public.pacientes_hospwin (id_paciente, numehist, niu, nombre, apellido1, apellido2, fonetica, situacion, situhpar, situcext, numecama, unihpar, unicext, equipo, equipohpar, equipocext, cuentacontable, cuentaentidad, cuentabancaria, formapago, sexo, estacivil) FROM '$$PATH$$/4536.dat';

--
-- Data for Name: peso; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.peso (id_secuencia, id_paciente, valor, imc, escala, fecha_medicion, observaciones, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM stdin;
\.
COPY public.peso (id_secuencia, id_paciente, valor, imc, escala, fecha_medicion, observaciones, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM '$$PATH$$/4495.dat';

--
-- Data for Name: presion_arterial; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.presion_arterial (id_secuencia_pa, id_paciente_pa, diastolica_pa, fecha_medicion_pa, observaciones_pa, usuario_graba_pa, fecha_registro_pa, usuario_modifica_pa, fecha_modifica_pa, sistolica_pa) FROM stdin;
\.
COPY public.presion_arterial (id_secuencia_pa, id_paciente_pa, diastolica_pa, fecha_medicion_pa, observaciones_pa, usuario_graba_pa, fecha_registro_pa, usuario_modifica_pa, fecha_modifica_pa, sistolica_pa) FROM '$$PATH$$/4526.dat';

--
-- Data for Name: saturacion_oxigeno; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.saturacion_oxigeno (id_secuencia_so, id_paciente_so, valor_so, fecha_medicion_so, observaciones_so, usuario_graba_so, fecha_registro_so, usuario_modifica_so, fecha_modifica_so) FROM stdin;
\.
COPY public.saturacion_oxigeno (id_secuencia_so, id_paciente_so, valor_so, fecha_medicion_so, observaciones_so, usuario_graba_so, fecha_registro_so, usuario_modifica_so, fecha_modifica_so) FROM '$$PATH$$/4528.dat';

--
-- Data for Name: talla; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.talla (id_secuencia, id_paciente, valor, fecha_medicion, observaciones, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM stdin;
\.
COPY public.talla (id_secuencia, id_paciente, valor, fecha_medicion, observaciones, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM '$$PATH$$/4499.dat';

--
-- Data for Name: tarjeta; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.tarjeta (idtarjeta, idusuario) FROM stdin;
\.
COPY public.tarjeta (idtarjeta, idusuario) FROM '$$PATH$$/4538.dat';

--
-- Data for Name: temperatura; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.temperatura (id_secuencia_temp, id_paciente_temp, valor_temp, escala_temp, fecha_medicion_temp, observaciones_temp, usuario_graba_temp, fecha_registro_temp, usuario_modifica_temp, fecha_modifica_temp) FROM stdin;
\.
COPY public.temperatura (id_secuencia_temp, id_paciente_temp, valor_temp, escala_temp, fecha_medicion_temp, observaciones_temp, usuario_graba_temp, fecha_registro_temp, usuario_modifica_temp, fecha_modifica_temp) FROM '$$PATH$$/4493.dat';

--
-- Data for Name: tipo_sonda; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.tipo_sonda (id_secuencia, id_paciente, tipo_sonda, fecha_colocacion, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM stdin;
\.
COPY public.tipo_sonda (id_secuencia, id_paciente, tipo_sonda, fecha_colocacion, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM '$$PATH$$/4505.dat';

--
-- Data for Name: tratamiento_ulcera; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.tratamiento_ulcera (id_secuencia, id_paciente, fecha, estado, fecha_deteccion, descripccion, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM stdin;
\.
COPY public.tratamiento_ulcera (id_secuencia, id_paciente, fecha, estado, fecha_deteccion, descripccion, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM '$$PATH$$/4518.dat';

--
-- Data for Name: ulceras; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.ulceras (id_secuencia, id_paciente, localizacion, tipo, fecha_deteccion, procedencia, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM stdin;
\.
COPY public.ulceras (id_secuencia, id_paciente, localizacion, tipo, fecha_deteccion, procedencia, usuario_graba, fecha_registro, usuario_modifica, fecha_modifica) FROM '$$PATH$$/4516.dat';

--
-- Data for Name: usuario_hospwin; Type: TABLE DATA; Schema: public; Owner: aitamenni
--

COPY public.usuario_hospwin (id_usuario, apellido1, apellido2, nombre, clave, activo, codigo, operador, idpersonal, consupervision, claveage, fecha_ultimo_cambio_clave) FROM stdin;
\.
COPY public.usuario_hospwin (id_usuario, apellido1, apellido2, nombre, clave, activo, codigo, operador, idpersonal, consupervision, claveage, fecha_ultimo_cambio_clave) FROM '$$PATH$$/4533.dat';

--
-- Name: cierre_ulcera_id_secuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.cierre_ulcera_id_secuencia_seq', 1, false);


--
-- Name: constantes_id_constantes_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.constantes_id_constantes_seq', 1, false);


--
-- Name: constantes_id_secuencia_fc_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.constantes_id_secuencia_fc_seq', 1, false);


--
-- Name: constantes_id_secuencia_fr_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.constantes_id_secuencia_fr_seq', 1, false);


--
-- Name: constantes_id_secuencia_pa_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.constantes_id_secuencia_pa_seq', 1, false);


--
-- Name: constantes_id_secuencia_so_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.constantes_id_secuencia_so_seq', 1, false);


--
-- Name: constantes_id_secuencia_temp_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.constantes_id_secuencia_temp_seq', 1, false);


--
-- Name: contencion_anyo_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.contencion_anyo_seq', 1, false);


--
-- Name: contencion_hora_fin_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.contencion_hora_fin_seq', 1, false);


--
-- Name: contencion_hora_inicio_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.contencion_hora_inicio_seq', 1, false);


--
-- Name: contencion_id_secuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.contencion_id_secuencia_seq', 5, true);


--
-- Name: cuidado_ulcera_id_secuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.cuidado_ulcera_id_secuencia_seq', 1, false);


--
-- Name: deposiciones_id_secuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.deposiciones_id_secuencia_seq', 11, true);


--
-- Name: diuresis_id_secuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.diuresis_id_secuencia_seq', 16, true);


--
-- Name: electrocardiograma_id_secuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.electrocardiograma_id_secuencia_seq', 42, true);


--
-- Name: frecuencia_cardiaca_id_secuencia_fc_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.frecuencia_cardiaca_id_secuencia_fc_seq', 15, true);


--
-- Name: frecuencia_respiratoria_id_secuencia_fr_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.frecuencia_respiratoria_id_secuencia_fr_seq', 31, true);


--
-- Name: glucosa_id_secuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.glucosa_id_secuencia_seq', 8, true);


--
-- Name: medicacion_id_secuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.medicacion_id_secuencia_seq', 5, true);


--
-- Name: menstruacion_id_secuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.menstruacion_id_secuencia_seq', 29, true);


--
-- Name: peso_id_secuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.peso_id_secuencia_seq', 14, true);


--
-- Name: presion_arterial_id_secuencia_pa_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.presion_arterial_id_secuencia_pa_seq', 14, true);


--
-- Name: saturacion_oxigeno_id_secuencia_so_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.saturacion_oxigeno_id_secuencia_so_seq', 96, true);


--
-- Name: talla_id_secuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.talla_id_secuencia_seq', 2, true);


--
-- Name: temperatura_id_secuencia_temp_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.temperatura_id_secuencia_temp_seq', 17, true);


--
-- Name: tipo_sonda_id_secuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.tipo_sonda_id_secuencia_seq', 1, false);


--
-- Name: tratamiento_ulcera_id_secuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.tratamiento_ulcera_id_secuencia_seq', 1, false);


--
-- Name: ulceras_id_secuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: aitamenni
--

SELECT pg_catalog.setval('public.ulceras_id_secuencia_seq', 1, false);


--
-- Name: cierre_ulcera cierre_ulcera_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.cierre_ulcera
    ADD CONSTRAINT cierre_ulcera_pkey PRIMARY KEY (id_secuencia);


--
-- Name: constantes constantes_id_secuencia_fc_key; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.constantes
    ADD CONSTRAINT constantes_id_secuencia_fc_key UNIQUE (id_secuencia_fc);


--
-- Name: constantes constantes_id_secuencia_fr_key; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.constantes
    ADD CONSTRAINT constantes_id_secuencia_fr_key UNIQUE (id_secuencia_fr);


--
-- Name: constantes constantes_id_secuencia_pa_key; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.constantes
    ADD CONSTRAINT constantes_id_secuencia_pa_key UNIQUE (id_secuencia_pa);


--
-- Name: constantes constantes_id_secuencia_so_key; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.constantes
    ADD CONSTRAINT constantes_id_secuencia_so_key UNIQUE (id_secuencia_so);


--
-- Name: constantes constantes_id_secuencia_temp_key; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.constantes
    ADD CONSTRAINT constantes_id_secuencia_temp_key UNIQUE (id_secuencia_temp);


--
-- Name: constantes constantes_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.constantes
    ADD CONSTRAINT constantes_pkey PRIMARY KEY (id_constantes);


--
-- Name: contencion contencion_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.contencion
    ADD CONSTRAINT contencion_pkey PRIMARY KEY (id_secuencia);


--
-- Name: cuidado_ulcera cuidado_ulcera_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.cuidado_ulcera
    ADD CONSTRAINT cuidado_ulcera_pkey PRIMARY KEY (id_secuencia);


--
-- Name: deposiciones deposiciones_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.deposiciones
    ADD CONSTRAINT deposiciones_pkey PRIMARY KEY (id_secuencia);


--
-- Name: diuresis diuresis_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.diuresis
    ADD CONSTRAINT diuresis_pkey PRIMARY KEY (id_secuencia);


--
-- Name: electrocardiograma electrocardiograma_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.electrocardiograma
    ADD CONSTRAINT electrocardiograma_pkey PRIMARY KEY (id_secuencia);


--
-- Name: fotos_hospwin fotos_hospwin_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.fotos_hospwin
    ADD CONSTRAINT fotos_hospwin_pkey PRIMARY KEY (id_paciente);


--
-- Name: frecuencia_cardiaca frecuencia_cardiaca_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.frecuencia_cardiaca
    ADD CONSTRAINT frecuencia_cardiaca_pkey PRIMARY KEY (id_secuencia_fc);


--
-- Name: frecuencia_respiratoria frecuencia_respiratoria_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.frecuencia_respiratoria
    ADD CONSTRAINT frecuencia_respiratoria_pkey PRIMARY KEY (id_secuencia_fr);


--
-- Name: glucosa glucosa_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.glucosa
    ADD CONSTRAINT glucosa_pkey PRIMARY KEY (id_secuencia);


--
-- Name: grupousu_hospwin grupousu_hospwin_id_usuario_key; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.grupousu_hospwin
    ADD CONSTRAINT grupousu_hospwin_id_usuario_key UNIQUE (id_usuario);


--
-- Name: grupousu_hospwin grupousu_hospwin_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.grupousu_hospwin
    ADD CONSTRAINT grupousu_hospwin_pkey PRIMARY KEY (id_grupo);


--
-- Name: medicacion medicacion_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.medicacion
    ADD CONSTRAINT medicacion_pkey PRIMARY KEY (id_secuencia);


--
-- Name: menstruacion menstruacion_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.menstruacion
    ADD CONSTRAINT menstruacion_pkey PRIMARY KEY (id_secuencia);


--
-- Name: monitor monitor_id_monitor_key; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.monitor
    ADD CONSTRAINT monitor_id_monitor_key UNIQUE (id_monitor);


--
-- Name: monitor monitor_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.monitor
    ADD CONSTRAINT monitor_pkey PRIMARY KEY (id_secuencia);


--
-- Name: pacientes_hospwin pacientes_hospwin_numehist_key; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.pacientes_hospwin
    ADD CONSTRAINT pacientes_hospwin_numehist_key UNIQUE (numehist);


--
-- Name: pacientes_hospwin pacientes_hospwin_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.pacientes_hospwin
    ADD CONSTRAINT pacientes_hospwin_pkey PRIMARY KEY (id_paciente);


--
-- Name: peso peso_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.peso
    ADD CONSTRAINT peso_pkey PRIMARY KEY (id_secuencia);


--
-- Name: presion_arterial presion_arterial_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.presion_arterial
    ADD CONSTRAINT presion_arterial_pkey PRIMARY KEY (id_secuencia_pa);


--
-- Name: saturacion_oxigeno saturacion_oxigeno_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.saturacion_oxigeno
    ADD CONSTRAINT saturacion_oxigeno_pkey PRIMARY KEY (id_secuencia_so);


--
-- Name: talla talla_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.talla
    ADD CONSTRAINT talla_pkey PRIMARY KEY (id_secuencia);


--
-- Name: temperatura temperatura_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.temperatura
    ADD CONSTRAINT temperatura_pkey PRIMARY KEY (id_secuencia_temp);


--
-- Name: tipo_sonda tipo_sonda_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.tipo_sonda
    ADD CONSTRAINT tipo_sonda_pkey PRIMARY KEY (id_secuencia);


--
-- Name: tratamiento_ulcera tratamiento_ulcera_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.tratamiento_ulcera
    ADD CONSTRAINT tratamiento_ulcera_pkey PRIMARY KEY (id_secuencia);


--
-- Name: ulceras ulceras_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.ulceras
    ADD CONSTRAINT ulceras_pkey PRIMARY KEY (id_secuencia);


--
-- Name: usuario_hospwin usuario_hospwin_clave_key; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.usuario_hospwin
    ADD CONSTRAINT usuario_hospwin_clave_key UNIQUE (clave);


--
-- Name: usuario_hospwin usuario_hospwin_pkey; Type: CONSTRAINT; Schema: public; Owner: aitamenni
--

ALTER TABLE ONLY public.usuario_hospwin
    ADD CONSTRAINT usuario_hospwin_pkey PRIMARY KEY (id_usuario);


--
-- PostgreSQL database dump complete
--

