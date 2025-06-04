#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LOINC code mappings module.

This module provides mappings between:
- Spanish table names from our database
- English measurement types
- LOINC codes and their descriptions

The module defines a structured mapping system for medical measurements and observations,
using LOINC (Logical Observation Identifiers Names and Codes) standards for healthcare
terminology.
"""

# Import modules #
#----------------#

from typing import Dict, NamedTuple

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

# Define classes #
#----------------#

class LoincMapping(NamedTuple):
    """
    Structure for LOINC code mapping information.
    
    Attributes
    ----------
    english_name : str
        English name of the measurement or observation
    loinc_code : str
        LOINC code for the measurement
    description : str
        Human-readable description of the measurement
    units : str, optional
        Units of measurement (default is empty string)
    system : str, optional
        Coding system identifier (default is LOINC system)
    """
    english_name: str
    loinc_code: str
    description: str
    units: str = ""
    system: str = "http://loinc.org"


# Define functions #
#------------------#

def get_measurement_type(table_name: str) -> str:
    """
    Get English measurement type for a given table name.
    
    Parameters
    ----------
    table_name : str
        Spanish table name from the database
        
    Returns
    -------
    str
        English measurement type string
        
    Raises
    ------
    KeyError
        If table_name is not found in mappings
    """
    return LOINC_MAPPINGS[table_name].english_name 

# Parameters and constants #
#--------------------------#

# Main mapping dictionary
# Maps Spanish table names to their LOINC information
LOINC_MAPPINGS: Dict[str, LoincMapping] = {
    # Core Vital Signs
    SATURACION_OXIGENO: LoincMapping(
        english_name="OXYGEN_SATURATION",
        loinc_code="59408-5",
        description="Oxygen saturation in Blood",
        units="%"
    ),
    TEMPERATURA: LoincMapping(
        english_name="TEMPERATURE",
        loinc_code="8310-5",
        description="Body temperature",
        units="Cel"  # Celsius
    ),
    PRESION_ARTERIAL: LoincMapping(
        english_name="BLOOD_PRESSURE",
        loinc_code="85354-9",
        description="Blood pressure panel",
        units="mmHg"
    ),
    FRECUENCIA_CARDIACA: LoincMapping(
        english_name="HEART_RATE",
        loinc_code="8867-4",
        description="Heart rate",
        units="/min"
    ),
    FRECUENCIA_RESPIRATORIA: LoincMapping(
        english_name="RESPIRATORY_RATE",
        loinc_code="9279-1",
        description="Respiratory rate",
        units="/min"
    ),
    
    # Other Clinical Measurements
    GLUCOSA: LoincMapping(
        english_name="GLUCOSE",
        loinc_code="2339-0",
        description="Glucose [Mass/volume] in Blood",
        units="mg/dL"
    ),
    PESO: LoincMapping(
        english_name="WEIGHT",
        loinc_code="29463-7",
        description="Body weight",
        units="kg"
    ),
    TALLA: LoincMapping(
        english_name="HEIGHT",
        loinc_code="8302-2",
        description="Body height",
        units="cm"
    ),
    DIURESIS: LoincMapping(
        english_name="URINE_OUTPUT",
        loinc_code="2823-3",
        description="Urine output",
        units="mL"
    ),
    DEPOSICIONES: LoincMapping(
        english_name="BOWEL_MOVEMENT",
        loinc_code="72166-2",
        description="Bowel movement"
    ),
    
    # Clinical Events/States
    MEDICACION: LoincMapping(
        english_name="MEDICATION",
        loinc_code="104792-7",
        description="Medication administration"
    ),
    CIERRE_ULCERA: LoincMapping(
        english_name="WOUND_CLOSURE",
        loinc_code="72166-2",
        description="Wound closure"
    ),
    TRATAMIENTO_ULCERA: LoincMapping(
        english_name="WOUND_TREATMENT",
        loinc_code="72166-2",
        description="Wound treatment"
    ),
    ULCERAS: LoincMapping(
        english_name="WOUND",
        loinc_code="72166-2",
        description="Wound assessment"
    ),
    CONTENCION: LoincMapping(
        english_name="RESTRAINT",
        loinc_code="72166-2",
        description="Restraint use"
    ),
    TIPO_SONDA: LoincMapping(
        english_name="CATHETER_TYPE",
        loinc_code="72166-2",
        description="Catheter type"
    ),
    CONSTANTES: LoincMapping(
        english_name="VITAL_SIGNS",
        loinc_code="34566-0",
        description="Vital signs with method details panel"
    ),
    ELECTROCARDIOGRAMA: LoincMapping(
        english_name="ECG",
        loinc_code="11524-6",
        description="EKG study",
        system="http://loinc.org"
    ),
    MENSTRUACION: LoincMapping(
        english_name="MENSTRUATION",
        loinc_code="49033-4",
        description="Menstrual History",
        system="http://loinc.org"
    ),
    CUIDADO_ULCERA: LoincMapping(
        english_name="WOUND_CARE",
        loinc_code="UNKNOWN",
        description="Wound care procedures and assessments"
    ),
    
    # Administrative Records
    PACIENTES_HOSPWIN: LoincMapping(
        english_name="HOSPITAL_PATIENTS",
        loinc_code="UNKNOWN",
        description="Hospital patient administrative records"
    ),
    USUARIO_HOSPWIN: LoincMapping(
        english_name="HOSPITAL_USERS",
        loinc_code="UNKNOWN",
        description="Hospital system users"
    ),
    GRUPOUSU_HOSPWIN: LoincMapping(
        english_name="USER_GROUPS",
        loinc_code="UNKNOWN",
        description="Hospital system user groups"
    ),
    MONITOR: LoincMapping(
        english_name="MONITOR",
        loinc_code="UNKNOWN",
        description="Monitoring system configuration"
    ),
    MONITORES_ACTIVOS: LoincMapping(
        english_name="ACTIVE_MONITORS",
        loinc_code="UNKNOWN",
        description="Active monitoring systems"
    ),
    TARJETA: LoincMapping(
        english_name="CARD",
        loinc_code="UNKNOWN",
        description="Card-based access or identification"
    ),
    FOTOS_HOSPWIN: LoincMapping(
        english_name="HOSPITAL_PHOTOS",
        loinc_code="UNKNOWN",
        description="Hospital system photographs"
    )
}