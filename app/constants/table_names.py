#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Table names module.

This module defines all database table names as constants.
These are the Spanish names used in the database schema.
"""

# Core Vital Signs
SATURACION_OXIGENO = 'saturacion_oxigeno'
TEMPERATURA = 'temperatura'
PRESION_ARTERIAL = 'presion_arterial'
FRECUENCIA_CARDIACA = 'frecuencia_cardiaca'
FRECUENCIA_RESPIRATORIA = 'frecuencia_respiratoria'
CONSTANTES = 'constantes'  # Combined vital signs

# Other Clinical Measurements
GLUCOSA = 'glucosa'
PESO = 'peso'
TALLA = 'talla'
DIURESIS = 'diuresis'
DEPOSICIONES = 'deposiciones'
ELECTROCARDIOGRAMA = 'electrocardiograma'

# Clinical Events/States
MEDICACION = 'medicacion'
CIERRE_ULCERA = 'cierre_ulcera'
TRATAMIENTO_ULCERA = 'tratamiento_ulcera'
ULCERAS = 'ulceras'
CONTENCION = 'contencion'
TIPO_SONDA = 'tipo_sonda'
CUIDADO_ULCERA = 'cuidado_ulcera'
MENSTRUACION = 'menstruacion'

# System Tables
PACIENTES_HOSPWIN = 'pacientes_hospwin'
USUARIO_HOSPWIN = 'usuario_hospwin'
GRUPOUSU_HOSPWIN = 'grupousu_hospwin'
MONITOR = 'monitor'
MONITORES_ACTIVOS = 'monitores_activos'
TARJETA = 'tarjeta'
FOTOS_HOSPWIN = 'fotos_hospwin'

# List of all valid table names
VALID_TABLE_NAMES = [
    # Core Vital Signs
    SATURACION_OXIGENO,
    TEMPERATURA,
    PRESION_ARTERIAL,
    FRECUENCIA_CARDIACA,
    FRECUENCIA_RESPIRATORIA,
    CONSTANTES,
    
    # Other Clinical Measurements
    GLUCOSA,
    PESO,
    TALLA,
    DIURESIS,
    DEPOSICIONES,
    ELECTROCARDIOGRAMA,
    
    # Clinical Events/States
    MEDICACION,
    CIERRE_ULCERA,
    TRATAMIENTO_ULCERA,
    ULCERAS,
    CONTENCION,
    TIPO_SONDA,
    CUIDADO_ULCERA,
    MENSTRUACION,
    
    # System Tables
    PACIENTES_HOSPWIN,
    USUARIO_HOSPWIN,
    GRUPOUSU_HOSPWIN,
    MONITOR,
    MONITORES_ACTIVOS,
    TARJETA,
    FOTOS_HOSPWIN
] 