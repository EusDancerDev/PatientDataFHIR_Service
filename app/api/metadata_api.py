#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from flask_restx import Resource, Namespace, fields

#------------#
# Operations #
#------------#

# Define namespaces #
#-------------------#

metadata_ns = Namespace('metadata', description='API metadata and documentation endpoints')

# Define models for responses #
#-----------------------------#

metadata_api_success_model = metadata_ns.model('MetadataAPISuccess', {
    'message': fields.String(description='API documentation message', example='API Documentation for Patient Data Retrieval'),
    'usage': fields.String(description='API usage information', example='This API provides access to patient vital signs and operational data. See /metadata/vital_signs and /metadata/operational_data for more details.')
})

metadata_vital_signs_success_model = metadata_ns.model('MetadataVitalSignsSuccess', {
    'tables': fields.List(fields.String, description='List of vital signs tables', example=[
        "saturacion_oxigeno", "temperatura", "presion_arterial",
        "frecuencia_cardiaca", "frecuencia_respiratoria", "glucosa", "peso"
    ]),
    'fields': fields.Raw(description='Fields metadata', example={
        "id_patient": "Patient ID value (format: 0000021561)",
        "date_range": {
            "min_date": "Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM)",
            "max_date": "End date (YYYY-MM-DD or YYYY-MM-DD HH:MM)"
        }
    }),
    'format': fields.String(description='Data format', example='FHIR v5 Bundle')
})

metadata_operational_data_success_model = metadata_ns.model('MetadataOperationalDataSuccess', {
    'tables': fields.List(fields.String, description='List of operational data tables', example=[
        "diuresis", "deposiciones", "electrocardiograma", "medicacion",
        "cierre_ulcera", "tratamiento_ulcera", "ulceras", "contencion",
        "tipo_sonda", "cuidado_ulcera", "menstruacion", "pacientes_hospwin",
        "usuario_hospwin", "grupousu_hospwin", "monitor", "monitores_activos",
        "tarjeta", "fotos_hospwin"
    ]),
    'fields': fields.Raw(description='Fields metadata', example={
        "id_patient": "Patient ID value (format: 0000021561)",
        "date_range": {
            "min_date": "Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM)",
            "max_date": "End date (YYYY-MM-DD or YYYY-MM-DD HH:MM)"
        }
    }),
    'format': fields.String(description='Data format', example='FHIR v5 Bundle')
})

metadata_server_error_model = metadata_ns.model('MetadataServerError', {
    'error': fields.String(description='Error message', example='An unexpected error occurred')
})

# Define routes #
#---------------#

# API Documentation Endpoint (/metadata/api)
"""
Purpose: Provides general API documentation and usage information
Access: Public
Response: API documentation message and usage information
"""
@metadata_ns.route('/api')
class APIDocumentation(Resource):
    @metadata_ns.response(200, 'Success', metadata_api_success_model, example={
        "message": "API Documentation for Patient Data Retrieval",
        "usage": "This API provides access to patient vital signs and operational data. See /metadata/vital_signs and /metadata/operational_data for more details."
    })
    @metadata_ns.response(500, 'Server Error', metadata_server_error_model, example={
        "error": "An unexpected error occurred"
    })
    def get(self):
        """Get API documentation and usage information"""
        return {
            "message": "API Documentation for Patient Data Retrieval",
            "usage": "This API provides access to patient vital signs and operational data. See /metadata/vital_signs and /metadata/operational_data for more details."
        }

# Vital Signs Metadata Endpoint (/metadata/vital_signs)
"""
Purpose: Provides metadata about available vital signs tables and their structure
Access: Public
Response: List of vital signs tables, field descriptions, and data format
"""
@metadata_ns.route('/vital_signs')
class VitalSignsMetadata(Resource):
    @metadata_ns.response(200, 'Success', metadata_vital_signs_success_model, example={
        "tables": [
            "saturacion_oxigeno", "temperatura", "presion_arterial",
            "frecuencia_cardiaca", "frecuencia_respiratoria", "glucosa", "peso"
        ],
        "fields": {
            "id_patient": "Patient ID value (format: 0000021561)",
            "date_range": {
                "min_date": "Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM)",
                "max_date": "End date (YYYY-MM-DD or YYYY-MM-DD HH:MM)"
            }
        },
        "format": "FHIR v5 Bundle"
    })
    @metadata_ns.response(500, 'Server Error', metadata_server_error_model, example={
        "error": "An unexpected error occurred"
    })
    def get(self):
        """Get metadata for vital signs tables"""
        return {
            "tables": [
                "saturacion_oxigeno", "temperatura", "presion_arterial",
                "frecuencia_cardiaca", "frecuencia_respiratoria", "glucosa", "peso"
            ],
            "fields": {
                "id_patient": "Patient ID value (format: 0000021561)",
                "date_range": {
                    "min_date": "Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM)",
                    "max_date": "End date (YYYY-MM-DD or YYYY-MM-DD HH:MM)"
                }
            },
            "format": "FHIR v5 Bundle"
        }

# Operational Data Metadata Endpoint (/metadata/operational_data)
"""
Purpose: Provides metadata about available operational data tables and their structure
Access: Public
Response: List of operational data tables, field descriptions, and data format
"""
@metadata_ns.route('/operational_data')
class OperationalDataMetadata(Resource):
    @metadata_ns.response(200, 'Success', metadata_operational_data_success_model, example={
        "tables": [
            "diuresis", "deposiciones", "electrocardiograma", "medicacion",
            "cierre_ulcera", "tratamiento_ulcera", "ulceras", "contencion",
            "tipo_sonda", "cuidado_ulcera", "menstruacion", "pacientes_hospwin",
            "usuario_hospwin", "grupousu_hospwin", "monitor", "monitores_activos",
            "tarjeta", "fotos_hospwin"
        ],
        "fields": {
            "id_patient": "Patient ID value (format: 0000021561)",
            "date_range": {
                "min_date": "Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM)",
                "max_date": "End date (YYYY-MM-DD or YYYY-MM-DD HH:MM)"
            }
        },
        "format": "FHIR v5 Bundle"
    })
    @metadata_ns.response(500, 'Server Error', metadata_server_error_model, example={
        "error": "An unexpected error occurred"
    })
    def get(self):
        """Get metadata for operational data tables"""
        return {
            "tables": [
                "diuresis", "deposiciones", "electrocardiograma", "medicacion",
                "cierre_ulcera", "tratamiento_ulcera", "ulceras", "contencion",
                "tipo_sonda", "cuidado_ulcera", "menstruacion", "pacientes_hospwin",
                "usuario_hospwin", "grupousu_hospwin", "monitor", "monitores_activos",
                "tarjeta", "fotos_hospwin"
            ],
            "fields": {
                "id_patient": "Patient ID value (format: 0000021561)",
                "date_range": {
                    "min_date": "Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM)",
                    "max_date": "End date (YYYY-MM-DD or YYYY-MM-DD HH:MM)"
                }
            },
            "format": "FHIR v5 Bundle"
        } 