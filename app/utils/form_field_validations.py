#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Form Field Validation Module

This module provides validation functionality for ID fields and date fields in a Flask application.
It focuses on validating IDs and date ranges.

The module uses regex pattern matching and type checking to ensure format validity.
It returns structured validation responses with specific error messages for invalid inputs.

The fields validated in this module are derived from TABLE_FIELD_MAPPING in app.constants.table_mappings.
Only the fields defined in that mapping are actually used in the validation process.

Currently used date fields (from TABLE_FIELD_MAPPING):
- fecha_registro_so
- fecha_registro_temp
- fecha_registro_pa
- fecha_registro_fc
- fecha_registro_fr
- fecha_registro
- f_actual
- fecha_conexion
- fecha_ultimo_cambio_clave
- fecha_medicion

Currently used ID fields
Patient IDs:
- id_paciente_so
- id_paciente_temp
- id_paciente_pa
- id_paciente_fc
- id_paciente_fr
- id_paciente

Other IDs:
- id_usuario
- id_monitor
- idtarjeta
"""

#------------------------#
# Import project modules #
#------------------------#

from app.constants.error_messages import (
    INVALID_DATE_FORMAT_ERROR,
    INVALID_DATE_RANGE_ERROR,
    INVALID_ID_FORMAT_ERROR,
    INVALID_ID_TYPE_ERROR,
)
from app.constants.fields import DATE_FIELDS, ID_FIELDS
from app.constants.table_mappings import TABLE_FIELD_MAPPING
from app.exceptions import ValidationError
from app.utils.string_handler import find_substring_index
from app.utils.time_formatters import parse_dt_string

#------------------#
# Define functions #
#------------------#

# Specific field validation functions #
#-------------------------------------#

def validate_id_field(value, invalid_val_err_str, empty_val_err_str):
    """
    Validate if the ID follows the required format.

    Parameters
    ----------
    value : str
        The ID value to validate. Can be any of the supported ID fields from TABLE_FIELD_MAPPING:
        Patient IDs:
        - id_paciente_so (saturacion_oxigeno)
        - id_paciente_temp (temperatura)
        - id_paciente_pa (presion_arterial)
        - id_paciente_fc (frecuencia_cardiaca)
        - id_paciente_fr (frecuencia_respiratoria)
        - id_paciente (glucosa, peso, talla, medicacion, deposiciones, diuresis, electrocardiograma, fotos_hospwin, monitores_activos, pacientes_hospwin, cierre_ulcera, constantes, contencion, cuidado_ulcera, menstruacion, tipo_sonda, tratamiento_ulcera, ulceras)
        Other IDs:
        - id_usuario (usuario_hospwin, grupousu_hospwin)
        - id_monitor (monitor)
        - idtarjeta (tarjeta)
    invalid_val_err_str : str
        The error message for invalid ID format.
    empty_val_err_str : str
        The error message for empty ID values.

    Returns
    -------
    dict
        A dictionary with the error message, if any, stored under the key `error_msg` (str).
    """
    try:
        if not isinstance(value, str):
            return {"error_msg": empty_val_err_str}
        
        pattern_match_index = find_substring_index(value, ID_PATTERN, advanced_search=True)
        if pattern_match_index == -1:
            return {"error_msg": invalid_val_err_str}
            
        return {"error_msg": ""}
    except (ValueError, TypeError):
        return {"error_msg": empty_val_err_str}

def validate_date_range(min_date, max_date):
    """
    Validate a date range.
    
    Parameters
    ----------
    min_date: str
        Start date in format YYYY-MM-DD or YYYY-MM-DD HH:MM
    max_date: str
        End date in format YYYY-MM-DD or YYYY-MM-DD HH:MM
        
    Returns
    -------
    Dict
        Dict with error message if validation fails, empty dict if validation passes
    """
    min_date_error = False
    max_date_error = False
    
    # Try parsing with time first
    try:
        min_datetime = parse_dt_string(min_date, '%Y-%m-%d %H:%M')
    except ValueError:
        try:
            # If that fails, try date-only format
            min_datetime = parse_dt_string(min_date, '%Y-%m-%d')
            min_datetime = min_datetime.replace(hour=0, minute=0)
        except ValueError:
            min_date_error = True
    
    try:
        max_datetime = parse_dt_string(max_date, '%Y-%m-%d %H:%M')
    except ValueError:
        try:
            # If that fails, try date-only format
            max_datetime = parse_dt_string(max_date, '%Y-%m-%d')
            max_datetime = max_datetime.replace(hour=23, minute=59)
        except ValueError:
            max_date_error = True
    
    if min_date_error and max_date_error:
        return {"error_msg": f"Invalid date format for min_date and max_date. {INVALID_DATE_FORMAT_ERROR}"}
    elif min_date_error:
        return {"error_msg": f"Invalid date format for min_date. {INVALID_DATE_FORMAT_ERROR}"}
    elif max_date_error:
        return {"error_msg": f"Invalid date format for max_date. {INVALID_DATE_FORMAT_ERROR}"}
    
    if min_datetime > max_datetime:
        return {"error_msg": INVALID_DATE_RANGE_ERROR}
    
    return {"error_msg": ""}

# Response generation functions #
#-------------------------------#

def generate_json_validation_response(json_data):
    """
    Generate validation response for JSON data.
    
    Parameters
    ----------
    json_data: Dict
        Dictionary containing field values to validate
        
    Returns
    -------
    Dict
        Dictionary mapping field names to validation results
    """
    validation_results = {}
    
    # Validate each field in the JSON data
    for field_name, field_value in json_data.items():
        # Skip table_name field
        if field_name == 'table_name':
            continue
            
        # Handle date range validation
        if field_name == 'date_range':
            if not isinstance(field_value, dict):
                validation_results[field_name] = {"error_msg": "Date range filtering requires a dictionary with 'min_date' and 'max_date' keys"}
                continue
                
            min_date = field_value.get('min_date')
            max_date = field_value.get('max_date')
            
            if not min_date or not max_date:
                validation_results[field_name] = {"error_msg": "Both 'min_date' and 'max_date' are required for date range filtering"}
                continue
                
            validation_results[field_name] = validate_date_range(min_date, max_date)
            continue
            
        # Handle ID field validation - check for any field in ID_FIELDS or the standard id_patient
        if field_name == 'id_patient' or field_name in ID_FIELDS:
            validation_results[field_name] = validate_id_field(field_value, INVALID_ID_FORMAT_ERROR, INVALID_ID_TYPE_ERROR)
            continue
            
    return validation_results

def validate_date_field_support(table_name: str, has_date_field: bool) -> None:
    """
    Validate if a table supports date range filtering.
    
    Parameters
    ----------
    table_name: str
        Name of the table to validate
    has_date_field: bool
        Whether the request includes date fields
        
    Raises
    ------
    ValidationError
        If the table doesn't support date filtering and date fields are present
    """
    if table_name:
        table_mapping = TABLE_FIELD_MAPPING.get(table_name)
        if table_mapping and table_mapping['date_field'] is None and has_date_field:
            raise ValidationError(f"Table '{table_name}' does not support date range filtering")

#--------------------------#
# Parameters and constants #
#--------------------------#

# Fields for filtering
FILTERABLE_FIELDS = ID_FIELDS + DATE_FIELDS

# Pretty names for documentation
FIELD_NAME_LIST_PRETTY = ["HL7 v2.X"]

# ID validation regex pattern
ID_PATTERN = r"^[0-9]{10}$"

# Validation mapping
FIELD_VALIDATORS = {field: lambda x: validate_id_field(x, INVALID_ID_FORMAT_ERROR, INVALID_ID_TYPE_ERROR) for field in ID_FIELDS}