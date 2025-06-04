#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from flask import Response, request
from flask_restx import Resource, Namespace, fields
import json

#------------------------#
# Import project modules #
#------------------------#

from app.services.patient_service import PatientService
from app.services.vital_signs_service import VitalSignsService
from app.db import init_db
from app.config import DATABASE_CREDENTIALS
from app.exceptions import ValidationError
from app.validators.patient_validators import PatientDataValidator
from app.constants.vital_signs_tables import VITAL_SIGNS_TABLES
from app.utils.auth_decorators import token_required

#------------#
# Operations #
#------------#

# Define namespaces #
#-------------------#

vital_signs_ns = Namespace('vital_signs', description='Vital signs data retrieval operations')

# Define models for POST /vital_signs/query #
#-----------------------------------------#

vital_signs_query_model = vital_signs_ns.model('VitalSignsQuery', {
    'id_patient': fields.String(required=True, description='ID value for the patient', example='0000021561'),
    'date_range': fields.Nested(vital_signs_ns.model('DateRange', {
        'min_date': fields.String(description='Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM)', example='2025-02-13 10:00'),
        'max_date': fields.String(description='End date (YYYY-MM-DD or YYYY-MM-DD HH:MM)', example='2025-02-13 10:50')
    }), required=True)
})

vital_signs_response_model = vital_signs_ns.model('VitalSignsResponse', {
    'resourceType': fields.String(description='Resource type', example='Bundle'),
    'type': fields.String(description='Bundle type', example='searchset'),
    'total': fields.Integer(description='Total number of resources', example=1),
    'entry': fields.List(fields.Raw, description='List of resources')
})

# Define models for responses #
#-----------------------------#

vital_signs_success_response_model = vital_signs_ns.model('VitalSignsSuccessResponse', {
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
                    "code": "8867-4",
                    "display": "Heart rate"
                }
            ]
        },
        "subject": {"reference": "Patient/0000021561"},
        "effectiveDateTime": "2025-02-13T10:00:00Z",
        "valueQuantity": {"value": 72, "unit": "beats/minute"}
    }])
})

vital_signs_validation_error_model = vital_signs_ns.model('VitalSignsValidationError', {
    'field': fields.String(description='Field with error', example='id_patient'),
    'error': fields.String(description='Error message', example='Missing ID value for the patient')
})

vital_signs_forbidden_model = vital_signs_ns.model('VitalSignsForbidden', {
    'field': fields.String(description='Field with error', example='authorization'),
    'error': fields.String(description='Error message', example='Insufficient permissions. Only medical professionals can access vital signs data.')
})

vital_signs_server_error_model = vital_signs_ns.model('VitalSignsServerError', {
    'field': fields.String(description='Field with error', example='server'),
    'error': fields.String(description='Error message', example='An unexpected error occurred')
})

# Define routes # 
#---------------#

# Vital Signs Data Endpoint (/vital_signs/<id_value>/<min_date>/<max_date>)
"""
Purpose: Retrieves vital signs data for a patient within a date range
Access: Medical professionals only (requires authentication)
Response: FHIR Bundle containing vital signs observations
"""
@vital_signs_ns.route('/<id_value>/<min_date>/<max_date>')
@vital_signs_ns.param('id_value', 'ID value for the patient')
@vital_signs_ns.param('min_date', 'Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM). If only date is provided, time defaults to 00:00')
@vital_signs_ns.param('max_date', 'End date (YYYY-MM-DD or YYYY-MM-DD HH:MM). If only date is provided, time defaults to 23:59')
class VitalSignsData(Resource):
    """Resource for retrieving vital signs data across multiple tables using an optimised UNION ALL query."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialise database session and services
        _, Session = init_db(DATABASE_CREDENTIALS)
        session = Session()
        self.patient_service = PatientService(session)
        self.vital_signs_service = VitalSignsService(self.patient_service)

    @vital_signs_ns.doc('get_vital_signs')
    @vital_signs_ns.response(200, 'Success', vital_signs_success_response_model, example={
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
                            "code": "8867-4",
                            "display": "Heart rate"
                        }
                    ]
                },
                "subject": {"reference": "Patient/0000021561"},
                "effectiveDateTime": "2025-02-13T10:00:00Z",
                "valueQuantity": {"value": 72, "unit": "beats/minute"}
            }
        ]
    })
    @vital_signs_ns.response(400, 'Validation Error', vital_signs_validation_error_model, example={
        "field": "id_patient",
        "error": "Missing ID value for the patient"
    })
    @vital_signs_ns.response(403, 'Forbidden', vital_signs_forbidden_model, example={
        "field": "authorization",
        "error": "Insufficient permissions. Only medical professionals can access vital signs data."
    })
    @vital_signs_ns.response(500, 'Server Error', vital_signs_server_error_model, example={
        "field": "server",
        "error": "An unexpected error occurred"
    })
    @token_required
    def get(self, id_value, min_date, max_date):
        """Retrieve all vital signs data for a patient within a date range using an optimised UNION ALL query for better performance."""
        user = request.user  # Contains 'username' and 'role'
        if user['role'] != 'medical':
            return Response(
                response=json.dumps({
                    'field': 'authorization',
                    'error': 'Insufficient permissions. Only medical professionals can access vital signs data.'
                }),
                status=403,
                mimetype='application/json'
            )
        try:
            # Basic validation for required fields
            if not id_value:
                return Response(
                    response=json.dumps({
                        'field': 'id_value',
                        'error': 'Missing ID value for the patient'
                    }),
                    status=400,
                    mimetype='application/json'
                )
                
            if not min_date or not max_date:
                return Response(
                    response=json.dumps({
                        'field': 'date_range',
                        'error': 'Both min_date and max_date are required'
                    }),
                    status=400,
                    mimetype='application/json'
                )
            
            # Validate ID value
            any_table = VITAL_SIGNS_TABLES[0]  # Get any vital signs table for validation
            id_field, date_field = PatientDataValidator.get_field_mappings(any_table)
            
            # Validate ID and date values
            validation_data = {
                id_field: id_value,
                date_field: {
                    "min_date": min_date,
                    "max_date": max_date
                }
            }
            
            validation_response = PatientDataValidator.validate_request_data(
                validation_data, id_field, date_field
            )
            if validation_response:
                return validation_response

            # Retrieve all vital signs data
            result = self.vital_signs_service.retrieve_all_vital_signs(
                patient_id=id_value,
                start_date=min_date,
                end_date=max_date
            )
            
            return Response(
                response=json.dumps(result),
                status=200,
                mimetype='application/json'
            )
        except ValidationError as e:
            return Response(
                response=json.dumps({
                    'field': 'validation',
                    'error': str(e)
                }),
                status=400,
                mimetype='application/json'
            )
        except Exception as e:
            return Response(
                response=json.dumps({
                    'field': 'server',
                    'error': str(e)
                }),
                status=500,
                mimetype='application/json'
            ) 

# Vital Signs Query Endpoint (/vital_signs/query)
"""
Purpose: Query vital signs data using JSON request body
Access: Medical professionals only (requires authentication)
Response: FHIR Bundle containing vital signs observations
"""
@vital_signs_ns.route('/query')
class VitalSignsQuery(Resource):
    @vital_signs_ns.doc('post_vital_signs_query')
    @vital_signs_ns.expect(vital_signs_query_model)
    @vital_signs_ns.response(200, 'Success', vital_signs_success_response_model, example={
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
                            "code": "8867-4",
                            "display": "Heart rate"
                        }
                    ]
                },
                "subject": {"reference": "Patient/0000021561"},
                "effectiveDateTime": "2025-02-13T10:00:00Z",
                "valueQuantity": {"value": 72, "unit": "beats/minute"}
            }
        ]
    })
    @vital_signs_ns.response(400, 'Validation Error', vital_signs_validation_error_model, example={
        "field": "date_range",
        "error": "Missing or invalid date range. Both min_date and max_date are required."
    })
    @vital_signs_ns.response(403, 'Forbidden', vital_signs_forbidden_model, example={
        "field": "authorization",
        "error": "Insufficient permissions. Only medical professionals can access vital signs data."
    })
    @vital_signs_ns.response(500, 'Server Error', vital_signs_server_error_model, example={
        "field": "server",
        "error": "An unexpected error occurred"
    })
    @token_required
    def post(self):
        """Query patient vital signs data for all vital sign tables using JSON request body."""
        user = request.user  # Contains 'username' and 'role'
        if user['role'] != 'medical':
            return {
                'field': 'authorization',
                'error': 'Insufficient permissions. Only medical professionals can access vital signs data.'
            }, 403
        try:
            request_data = request.get_json()
            patient_id = request_data.get('id_patient')
            date_range = request_data.get('date_range', {})
            # Validate basic required fields
            if not patient_id:
                return {'field': 'id_patient', 'error': 'Missing ID value for the patient'}, 400
            if not date_range or 'min_date' not in date_range or 'max_date' not in date_range:
                return {'field': 'date_range', 'error': 'Missing or invalid date range. Both min_date and max_date are required.'}, 400
            # Validate ID and date values
            any_table = VITAL_SIGNS_TABLES[0]
            id_field, date_field = PatientDataValidator.get_field_mappings(any_table)
            validation_data = {
                id_field: patient_id,
                date_field: date_range
            }
            validation_response = PatientDataValidator.validate_request_data(validation_data, id_field, date_field)
            if validation_response:
                return validation_response, 400
            # Retrieve all vital signs data
            _, Session = init_db(DATABASE_CREDENTIALS)
            session = Session()
            patient_service = PatientService(session)
            vital_signs_service = VitalSignsService(patient_service)
            result = vital_signs_service.retrieve_all_vital_signs(
                patient_id=patient_id,
                start_date=date_range['min_date'],
                end_date=date_range['max_date']
            )
            return result, 200
        except ValidationError as e:
            return {'field': 'validation', 'error': str(e)}, 400
        except Exception as e:
            return {'field': 'server', 'error': str(e)}, 500 