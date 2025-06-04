#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Table mappings module.

This module contains the mapping of table names to their corresponding field names.
"""

# Import project modules #
#------------------------#

from app.constants.table_names import (
    SATURACION_OXIGENO,
    TEMPERATURA,
    PRESION_ARTERIAL,
    FRECUENCIA_CARDIACA,
    FRECUENCIA_RESPIRATORIA,
    CONSTANTES,
    GLUCOSA,
    PESO,
    TALLA,
    DIURESIS,
    DEPOSICIONES,
    ELECTROCARDIOGRAMA,
    MEDICACION,
    CIERRE_ULCERA,
    TRATAMIENTO_ULCERA,
    ULCERAS,
    CONTENCION,
    TIPO_SONDA,
    CUIDADO_ULCERA,
    MENSTRUACION,
    PACIENTES_HOSPWIN,
    USUARIO_HOSPWIN,
    GRUPOUSU_HOSPWIN,
    MONITOR,
    MONITORES_ACTIVOS,
    TARJETA,
    FOTOS_HOSPWIN
)

# Define parameters #
#-------------------#

# Database table field mapping #
TABLE_FIELD_MAPPING = {
    SATURACION_OXIGENO: {
        'id_field': 'id_paciente_so',
        'date_field': 'fecha_registro_so',
        'standard_table_name': 'OXYGEN_SATURATION'
    },
    TEMPERATURA: {
        'id_field': 'id_paciente_temp',
        'date_field': 'fecha_registro_temp',
        'standard_table_name': 'TEMPERATURE'
    },
    PRESION_ARTERIAL: {
        'id_field': 'id_paciente_pa',
        'date_field': 'fecha_registro_pa',
        'standard_table_name': 'BLOOD_PRESSURE'
    },
    FRECUENCIA_CARDIACA: {
        'id_field': 'id_paciente_fc',
        'date_field': 'fecha_registro_fc',
        'standard_table_name': 'HEART_RATE'
    },
    FRECUENCIA_RESPIRATORIA: {
        'id_field': 'id_paciente_fr',
        'date_field': 'fecha_registro_fr',
        'standard_table_name': 'RESPIRATORY_RATE'
    },
    GLUCOSA: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_registro',
        'standard_table_name': 'GLUCOSE'
    },
    PESO: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_registro',
        'standard_table_name': 'WEIGHT'
    },
    TALLA: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_registro',
        'standard_table_name': 'HEIGHT'
    },
    MEDICACION: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_registro',
        'standard_table_name': 'MEDICATION'
    },
    DEPOSICIONES: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_registro',
        'standard_table_name': 'BOWEL_MOVEMENTS'
    },
    DIURESIS: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_registro',
        'standard_table_name': 'URINE_OUTPUT'
    },
    ELECTROCARDIOGRAMA: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_registro',
        'standard_table_name': 'ELECTROCARDIOGRAM'
    },
    FOTOS_HOSPWIN: {
        'id_field': 'id_paciente',
        'date_field': 'f_actual',
        'standard_table_name': 'PATIENT_PHOTOS'
    },
    MONITORES_ACTIVOS: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_conexion',
        'standard_table_name': 'ACTIVE_MONITORS'
    },
    PACIENTES_HOSPWIN: {
        'id_field': 'id_paciente',
        'date_field': None,
        'standard_table_name': 'PATIENTS'
    },
    USUARIO_HOSPWIN: {
        'id_field': 'id_usuario',
        'date_field': 'fecha_ultimo_cambio_clave',
        'standard_table_name': 'USERS'
    },
    CIERRE_ULCERA: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_registro',
        'standard_table_name': 'WOUND_CLOSURE'
    },
    CONSTANTES: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_medicion',
        'standard_table_name': 'VITAL_SIGNS'
    },
    CONTENCION: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_registro',
        'standard_table_name': 'RESTRAINT'
    },
    CUIDADO_ULCERA: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_registro',
        'standard_table_name': 'WOUND_CARE'
    },
    MENSTRUACION: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_registro',
        'standard_table_name': 'MENSTRUATION'
    },
    MONITOR: {
        'id_field': 'id_monitor',
        'date_field': 'fecha_registro',
        'standard_table_name': 'MONITOR'
    },
    TARJETA: {
        'id_field': 'idtarjeta',
        'date_field': None,
        'standard_table_name': 'CARD'
    },
    TIPO_SONDA: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_registro',
        'standard_table_name': 'CATHETER_TYPE'
    },
    TRATAMIENTO_ULCERA: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_registro',
        'standard_table_name': 'WOUND_TREATMENT'
    },
    ULCERAS: {
        'id_field': 'id_paciente',
        'date_field': 'fecha_registro',
        'standard_table_name': 'WOUNDS'
    },
    GRUPOUSU_HOSPWIN: {
        'id_field': 'id_usuario',
        'date_field': None,
        'standard_table_name': 'USER_GROUPS'
    }
} 