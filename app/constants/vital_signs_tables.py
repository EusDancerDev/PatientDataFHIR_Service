#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vital Signs Tables module.

This module defines which tables are considered vital signs
for combined data retrieval operations.
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
    PESO,
    TALLA
)

# List of all vital signs tables
VITAL_SIGNS_TABLES = [
    SATURACION_OXIGENO,
    TEMPERATURA,
    PRESION_ARTERIAL,
    FRECUENCIA_CARDIACA,
    FRECUENCIA_RESPIRATORIA,
    CONSTANTES,
    GLUCOSA,
    PESO,
    TALLA
] 