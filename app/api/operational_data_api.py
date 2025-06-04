#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from flask import request
from flask_restx import Resource, fields, Namespace

#------------------------#
# Import project modules #
#------------------------#

from app.config import DATABASE_CREDENTIALS
from app.constants.operational_tables import OPERATIONAL_TABLES
from app.db import init_db
from app.exceptions import ValidationError
from app.services.patient_service import PatientService
from app.utils.auth_decorators import token_required
from app.validators.patient_validators import PatientDataValidator

#------------#
# Operations #
#------------#

# Define namespaces #
#-------------------#

api = Namespace(
    'operational_data',
    description='Operational data retrieval operations (admin only).'
)

# Request model
operational_query_model = api.model('OperationalQuery', {
    'id_patient': fields.String(required=True, description='ID value for the patient', example='0000021561'),
    'date_range': fields.Nested(api.model('DateRange', {
        'min_date': fields.String(description='Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM)', example='2025-02-13 10:00'),
        'max_date': fields.String(description='End date (YYYY-MM-DD or YYYY-MM-DD HH:MM)', example='2025-02-13 10:50')
    }), required=True)
})

# Response model (generic, as columns vary)
operational_response_model = api.model('OperationalResponse', {
    'resourceType': fields.String(description='Resource type', example='Bundle'),
    'type': fields.String(description='Bundle type', example='searchset'),
    'total': fields.Integer(description='Total number of resources', example=1),
    'entry': fields.List(fields.Raw, description='List of resources')
})

# Define models for responses #
#-----------------------------#

operational_success_response_model = api.model('OperationalSuccessResponse', {
    'resourceType': fields.String(description='Resource type', example='Bundle'),
    'type': fields.String(description='Bundle type', example='searchset'),
    'total': fields.Integer(description='Total number of resources', example=1),
    'entry': fields.List(fields.Raw, description='List of resources', example=[{
        "resourceType": "Observation",
        "id": "example-id",
        "status": "final",
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "12345-6",
                    "display": "Operational data example"
                }
            ]
        },
        "subject": {"reference": "Patient/0000021561"},
        "effectiveDateTime": "2025-02-13T10:00:00Z",
        "valueString": "Sample operational data value"
    }])
})

operational_validation_error_model = api.model('OperationalValidationError', {
    'field': fields.String(description='Field with error', example='id_patient'),
    'error': fields.String(description='Error message', example='Missing ID value for the patient')
})

operational_forbidden_model = api.model('OperationalForbidden', {
    'message': fields.String(description='Error message', example='Insufficient permissions. Only admins can access operational data.')
})

operational_server_error_model = api.model('OperationalServerError', {
    'field': fields.String(description='Field with error', example='server'),
    'error': fields.String(description='Error message', example='An unexpected error occurred')
})

# Define routes #
#---------------#

# Operational Data Endpoint (/operational_data/<id_value>/<min_date>/<max_date>)
"""
Purpose: Retrieves operational data for a patient within a date range
Access: Administrators only (requires authentication)
Response: FHIR Bundle containing operational data observations
"""
@api.route('/<id_value>/<min_date>/<max_date>')
@api.param('id_value', 'ID value for the patient')
@api.param('min_date', 'Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM). If only date is provided, time defaults to 00:00')
@api.param('max_date', 'End date (YYYY-MM-DD or YYYY-MM-DD HH:MM). If only date is provided, time defaults to 23:59')
class OperationalData(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _, Session = init_db(DATABASE_CREDENTIALS)
        session = Session()
        self.service = PatientService(session)

    @api.doc('get_operational_data')
    @api.response(200, 'Success', operational_success_response_model, example={
        "resourceType": "Bundle",
        "type": "searchset",
        "total": 1,
        "entry": [
            {
                "resourceType": "Observation",
                "id": "example-id",
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "12345-6",
                            "display": "Operational data example"
                        }
                    ]
                },
                "subject": {"reference": "Patient/0000021561"},
                "effectiveDateTime": "2025-02-13T10:00:00Z",
                "valueString": "Sample operational data value"
            }
        ]
    })
    @api.response(400, 'Validation Error', operational_validation_error_model, example={
        "field": "id_patient",
        "error": "Missing ID value for the patient"
    })
    @api.response(403, 'Forbidden', operational_forbidden_model, example={
        "message": "Insufficient permissions. Only admins can access operational data."
    })
    @api.response(500, 'Server Error', operational_server_error_model, example={
        "field": "server",
        "error": "An unexpected error occurred"
    })
    @token_required
    def get(self, id_value, min_date, max_date):
        """
        Retrieve operational data for a patient within a date range (admin only).
        """
        user = request.user
        if user['role'] != 'admin':
            return {'message': 'Insufficient permissions. Only admins can access operational data.'}, 403
        try:
            # Validate required fields
            if not id_value:
                return {'field': 'id_value', 'error': 'Missing ID value for the patient'}, 400
            if not min_date or not max_date:
                return {'field': 'date_range', 'error': 'Missing or invalid date range. Both min_date and max_date are required.'}, 400

            date_range = {
                'min_date': min_date,
                'max_date': max_date
            }

            # Validate data for each operational table
            for table_name in OPERATIONAL_TABLES:
                id_field, date_field = PatientDataValidator.get_field_mappings(table_name)
                validation_data = {
                    id_field: id_value,
                    date_field: date_range
                }
                validation_response = PatientDataValidator.validate_request_data(validation_data, id_field, date_field)
                if validation_response:
                    return validation_response, 400

            # Retrieve data from all operational tables
            result = self.service.get_patient_data_across_tables(
                patient_id=id_value,
                table_names=OPERATIONAL_TABLES,
                start_date=min_date,
                end_date=max_date
            )
            
            if not result:
                return {
                    'resourceType': 'Bundle',
                    'type': 'searchset',
                    'total': 0,
                    'entry': []
                }, 200

            # Return the FHIR bundle directly
            return result, 200
        except ValidationError as e:
            return {'field': 'validation', 'error': str(e)}, 400
        except Exception as e:
            return {'field': 'server', 'error': str(e)}, 500

# Operational Data Query Endpoint (/operational_data/query)
"""
Purpose: Query operational data using JSON request body
Access: Administrators only (requires authentication)
Response: FHIR Bundle containing operational data observations
"""
@api.route('/query')
class OperationalDataQuery(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _, Session = init_db(DATABASE_CREDENTIALS)
        session = Session()
        self.service = PatientService(session)

    @api.doc('post_operational_data')
    @api.expect(operational_query_model)
    @api.response(200, 'Success', operational_success_response_model, example={
        "resourceType": "Bundle",
        "type": "searchset",
        "total": 1,
        "entry": [
            {
                "resourceType": "Observation",
                "id": "example-id",
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "12345-6",
                            "display": "Operational data example"
                        }
                    ]
                },
                "subject": {"reference": "Patient/0000021561"},
                "effectiveDateTime": "2025-02-13T10:00:00Z",
                "valueString": "Sample operational data value"
            }
        ]
    })
    @api.response(400, 'Validation Error', operational_validation_error_model, example={
        "field": "date_range",
        "error": "Missing or invalid date range. Both min_date and max_date are required."
    })
    @api.response(403, 'Forbidden', operational_forbidden_model, example={
        "message": "Insufficient permissions. Only admins can access operational data."
    })
    @api.response(500, 'Server Error', operational_server_error_model, example={
        "field": "server",
        "error": "An unexpected error occurred"
    })
    @token_required
    def post(self):
        """
        Query operational data for a patient (admin only).

        - `id_patient` will be mapped to the appropriate patient ID field for each table.
        - `date_range` will be mapped to the appropriate date field for each table.
        - All operational tables are always queried.

        **Available tables and their patient/date fields:**
        - diuresis: id_paciente, fecha_registro
        - deposiciones: id_paciente, fecha_registro
        - electrocardiograma: id_paciente, fecha_registro
        - medicacion: id_paciente, fecha_registro
        - cierre_ulcera: id_paciente, fecha_registro
        - tratamiento_ulcera: id_paciente, fecha_registro
        - ulceras: id_paciente, fecha_registro
        - contencion: id_paciente, fecha_registro
        - tipo_sonda: id_paciente, fecha_registro
        - cuidado_ulcera: id_paciente, fecha_registro
        - menstruacion: id_paciente, fecha_registro
        - pacientes_hospwin: id_paciente, fecha_registro
        - usuario_hospwin: id_usuario, fecha_ultimo_cambio_clave
        - grupousu_hospwin: id_usuario, None
        - monitor: id_monitor, fecha_registro
        - monitores_activos: id_paciente, fecha_conexion
        - tarjeta: idtarjeta, None
        - fotos_hospwin: id_paciente, f_actual
        """
        user = request.user
        if user['role'] != 'admin':
            return {'message': 'Insufficient permissions. Only admins can access operational data.'}, 403
        try:
            request_data = request.get_json()
            patient_id = request_data.get('id_patient')
            date_range = request_data.get('date_range', {})
            # Validate required fields
            if not patient_id:
                return {'field': 'id_patient', 'error': 'Missing ID value for the patient'}, 400
            if not date_range or 'min_date' not in date_range or 'max_date' not in date_range:
                return {'field': 'date_range', 'error': 'Missing or invalid date range. Both min_date and max_date are required.'}, 400
            # Validate data for each operational table
            for table_name in OPERATIONAL_TABLES:
                id_field, date_field = PatientDataValidator.get_field_mappings(table_name)
                validation_data = {
                    id_field: patient_id,
                    date_field: date_range
                }
                validation_response = PatientDataValidator.validate_request_data(validation_data, id_field, date_field)
                if validation_response:
                    return validation_response, 400
            # Retrieve data from all operational tables
            result = self.service.get_patient_data_across_tables(
                patient_id=patient_id,
                table_names=OPERATIONAL_TABLES,
                start_date=date_range['min_date'],
                end_date=date_range['max_date']
            )
            
            if not result:
                return {
                    'resourceType': 'Bundle',
                    'type': 'searchset',
                    'total': 0,
                    'entry': []
                }, 200

            # Return the FHIR bundle directly
            return result, 200
        except ValidationError as e:
            return {'field': 'validation', 'error': str(e)}, 400
        except Exception as e:
            return {'field': 'server', 'error': str(e)}, 500 