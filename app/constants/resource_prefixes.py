#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource Prefixes module.

This module defines ID prefixes for FHIR resources
to ensure consistent and meaningful resource IDs.
"""

# Import project modules #
#------------------------#

# Vital signs table names #
from app.constants.table_names import (
    SATURACION_OXIGENO,
    TEMPERATURA,
    PRESION_ARTERIAL,
    FRECUENCIA_CARDIACA,
    FRECUENCIA_RESPIRATORIA,
    CONSTANTES,
    GLUCOSA,
    PESO
)

# Mapping of vital signs table names to FHIR resource ID prefixes
RESOURCE_ID_PREFIXES = {
    SATURACION_OXIGENO: 'oxsat',
    TEMPERATURA: 'temp',
    PRESION_ARTERIAL: 'bp',
    FRECUENCIA_CARDIACA: 'hr',
    FRECUENCIA_RESPIRATORIA: 'rr',
    CONSTANTES: 'vitals',
    GLUCOSA: 'gluc',
    PESO: 'wt'
} 