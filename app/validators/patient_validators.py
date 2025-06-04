#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Patient data validation module.

This module handles all validation logic for patient data requests,
including table name validation, field mapping, and error handling.
"""

# Import modules #
#----------------#  

import json
from typing import Dict, Tuple, Optional

from flask import Response

# Import project modules #
#------------------------#

from app.constants.table_mappings import TABLE_FIELD_MAPPING
from app.utils.form_field_validations import generate_json_validation_response

# Define classes and methods #
#----------------------------#

class PatientDataValidator:
    """Handles validation of patient data requests."""
    
    @staticmethod
    def validate_table_name(table_name: str) -> Optional[Response]:
        """Validate if the table name exists in the mapping."""
        if table_name not in TABLE_FIELD_MAPPING:
            return Response(
                response=json.dumps({
                    'field': 'table_name',
                    'error': f'invalid table name {table_name}. Must be one of: {", ".join(TABLE_FIELD_MAPPING.keys())}'
                }),
                status=400,
                mimetype='application/json'
            )
        return None

    @staticmethod
    def get_field_mappings(table_name: str) -> Tuple[str, str]:
        """Get the ID and date field mappings for a table."""
        table_mapping = TABLE_FIELD_MAPPING[table_name]
        return table_mapping['id_field'], table_mapping['date_field']

    @staticmethod
    def validate_request_data(
        validation_data: Dict,
        id_field: str,
        date_field: str
    ) -> Optional[Response]:
        """Validate the request data and return appropriate error response if needed."""
        validation_results = generate_json_validation_response(validation_data)

        if any(result['error_msg'] for result in validation_results.values()):
            for field, result in validation_results.items():
                if result['error_msg']:
                    swagger_field = PatientDataValidator._map_to_swagger_field(
                        field, id_field, date_field, result['error_msg']
                    )
                    return Response(
                        response=json.dumps({
                            'field': swagger_field,
                            'error': result['error_msg']
                        }),
                        status=400,
                        mimetype='application/json'
                    )
        return None

    @staticmethod
    def _map_to_swagger_field(
        field: str,
        id_field: str,
        date_field: str,
        error_msg: str
    ) -> str:
        """Map internal field names to Swagger field names."""
        if field == id_field:
            return 'id_field'
        elif field == date_field:
            # Check for date format errors
            if 'invalid date format' in error_msg:
                # If both max_date and min_date have errors
                if 'max_date' in error_msg and 'min_date' in error_msg:
                    return 'max_date and min_date'
                # If only max_date has an error
                if 'max_date' in error_msg:
                    return 'max_date'
                # If only min_date has an error
                if 'min_date' in error_msg:
                    return 'min_date'
                # Default to min_date for any other date format error
                return 'min_date'
            # For other date-related errors (like range validation)
            if 'must be less than or equal to' in error_msg:
                return 'min_date'
            return 'min_date'
        return field