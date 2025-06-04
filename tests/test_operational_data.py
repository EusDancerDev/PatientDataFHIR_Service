#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test module for operational data functionality.

This module contains tests for:
1. API endpoints for data retrieval
2. Authentication and authorisation
3. Operational tables configuration
4. Data retrieval and validation
5. Data format conversion (HL7 and FHIR)
"""

# Import modules #
#----------------#

import json
import unittest
from datetime import datetime, timedelta

# Import project modules #
#------------------------#
from app.api.auth_api import AuthResource
from app.api.operational_data_api import PatientData
from app.api.vital_signs_api import VitalSignsData
from app.config import DATABASE_CREDENTIALS
from app.constants.operational_tables import OPERATIONAL_TABLES
from app.db import init_db
from app.models.patient_models import TABLE_MODEL_MAP
from app.services.patient_service import PatientService
from app.utils.fhir_formatter import hl7_to_fhir
from app.validators.patient_validators import PatientDataValidator

# Define test case classes and methods #
#--------------------------------------#

class TestOperationalData(unittest.TestCase):
    """Test cases for operational data functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Initialize database session
        self.engine, Session = init_db(DATABASE_CREDENTIALS)
        self.session = Session()
        self.patient_service = PatientService(self.session)
        
        # Initialize API resources
        self.patient_data = PatientData()
        self.vital_signs_data = VitalSignsData()
        self.auth_resource = AuthResource()

    def tearDown(self):
        """Clean up after tests."""
        self.session.close()

    def test_api_endpoints(self):
        """Test the API endpoints for data retrieval."""
        # Test data
        patient_id = "0000021561"
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M")
        end_date = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Test POST /vital_signs/query
        request_data = {
            'id_patient': patient_id,
            'date_range': {
                'min_date': start_date,
                'max_date': end_date
            }
        }
        # Simulate POST /api/vital_signs/query
        response = self.vital_signs_data.post()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('resourceType', data)
        self.assertEqual(data['resourceType'], 'Bundle')

        # Test GET /vital_signs
        response = self.vital_signs_data.get(patient_id, start_date, end_date)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('resourceType', data)
        self.assertEqual(data['resourceType'], 'Bundle')

    def test_authentication(self):
        """Test the authentication endpoint."""
        # Test data
        test_credentials = {
            'username': 'test_user',
            'password': 'TestPass123!'
        }

        # Test login
        response = self.auth_resource.post()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)
        self.assertIn('role', data)

    def test_operational_tables_list(self):
        """Test that all operational tables are properly defined."""
        self.assertIsInstance(OPERATIONAL_TABLES, list)
        self.assertTrue(len(OPERATIONAL_TABLES) > 0)
        
        # Verify each table has a corresponding model
        for table_name in OPERATIONAL_TABLES:
            self.assertIn(table_name, TABLE_MODEL_MAP)
            model_class = TABLE_MODEL_MAP[table_name]
            self.assertTrue(hasattr(model_class, '__tablename__'))
            self.assertEqual(model_class.__tablename__, table_name)

    def test_operational_data_retrieval(self):
        """Test retrieving operational data for a patient."""
        # Test data
        patient_id = "0000021561"
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()

        # Test each operational table
        for table_name in OPERATIONAL_TABLES:
            model_class = TABLE_MODEL_MAP[table_name]
            
            # Get field mappings
            id_field, date_field = PatientDataValidator.get_field_mappings(table_name)
            
            # Query the table
            query = self.session.query(model_class).filter(
                getattr(model_class, id_field) == patient_id
            )
            
            if date_field:
                query = query.filter(
                    getattr(model_class, date_field).between(start_date, end_date)
                )
            
            results = query.all()
            
            # Verify results
            self.assertIsInstance(results, list)
            for result in results:
                self.assertIsInstance(result, model_class)
                self.assertEqual(getattr(result, id_field), patient_id)
                if date_field:
                    result_date = getattr(result, date_field)
                    self.assertTrue(start_date <= result_date <= end_date)

    def test_operational_data_validation(self):
        """Test validation of operational data queries."""
        # Test data
        patient_id = "0000021561"
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()

        # Test each operational table
        for table_name in OPERATIONAL_TABLES:
            # Get field mappings
            id_field, date_field = PatientDataValidator.get_field_mappings(table_name)
            
            # Test validation data
            validation_data = {
                id_field: patient_id,
                date_field: {
                    "min_date": start_date.strftime("%Y-%m-%d %H:%M"),
                    "max_date": end_date.strftime("%Y-%m-%d %H:%M")
                }
            }
            
            # Validate the data
            validation_response = PatientDataValidator.validate_request_data(
                validation_data, id_field, date_field
            )
            
            # Verify validation
            self.assertIsNone(validation_response)

    def test_operational_data_hl7_conversion(self):
        """Test conversion of operational data to HL7 format."""
        # Test data
        patient_id = "0000021561"
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()

        # Test each operational table
        for table_name in OPERATIONAL_TABLES:
            model_class = TABLE_MODEL_MAP[table_name]
            
            # Get field mappings
            id_field, date_field = PatientDataValidator.get_field_mappings(table_name)
            
            # Query the table
            query = self.session.query(model_class).filter(
                getattr(model_class, id_field) == patient_id
            )
            
            if date_field:
                query = query.filter(
                    getattr(model_class, date_field).between(start_date, end_date)
                )
            
            results = query.all()
            
            # Test HL7 conversion for each result
            for result in results:
                hl7_message = result.to_hl7_v2()
                self.assertIsInstance(hl7_message, str)
                self.assertTrue(len(hl7_message) > 0)
                
                # Verify basic HL7 message structure
                self.assertTrue(hl7_message.startswith('MSH|'))
                self.assertIn('OBX|', hl7_message)

    def test_operational_data_fhir_conversion(self):
        """Test conversion of operational data to FHIR format."""
        # Test data
        patient_id = "0000021561"
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()

        # Test each operational table
        for table_name in OPERATIONAL_TABLES:
            model_class = TABLE_MODEL_MAP[table_name]
            
            # Get field mappings
            id_field, date_field = PatientDataValidator.get_field_mappings(table_name)
            
            # Query the table
            query = self.session.query(model_class).filter(
                getattr(model_class, id_field) == patient_id
            )
            
            if date_field:
                query = query.filter(
                    getattr(model_class, date_field).between(start_date, end_date)
                )
            
            results = query.all()
            
            # Test FHIR conversion for each result
            for result in results:
                # First convert to HL7
                hl7_message = result.to_hl7_v2()
                
                # Then convert HL7 to FHIR
                fhir_resource = hl7_to_fhir(hl7_message)
                
                # Verify FHIR resource structure
                self.assertIsInstance(fhir_resource, dict)
                self.assertEqual(fhir_resource['resourceType'], 'Observation')
                self.assertIn('code', fhir_resource)
                self.assertIn('subject', fhir_resource)
                self.assertIn('valueQuantity', fhir_resource)

# Main execution #
#----------------#

if __name__ == '__main__':
    unittest.main() 