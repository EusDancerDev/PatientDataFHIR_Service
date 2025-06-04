#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vital Signs Service module.

This module provides services for retrieving vital signs data across multiple tables.
"""

# Import modules #
#----------------#

from typing import Dict, List, Optional
 
# Import project modules #
#------------------------#

from app.constants.operational_tables import OPERATIONAL_TABLES
from app.constants.resource_prefixes import RESOURCE_ID_PREFIXES
from app.constants.table_mappings import TABLE_FIELD_MAPPING
from app.constants.vital_signs_tables import VITAL_SIGNS_TABLES
from app.db import MODEL_REGISTRY, filter_data_consolidated
from app.exceptions import ValidationError
from app.services.patient_service import PatientService
from app.utils.form_field_validations import generate_json_validation_response

# Define classes and methods #
#----------------------------#  

class VitalSignsService:
    """
    Service class for retrieving vital signs data across multiple tables.
    """
    
    def __init__(self, patient_service: PatientService):
        """
        Initialise the VitalSignsService with a PatientService instance.
        
        Parameters
        ----------
        patient_service: PatientService
            PatientService instance for data retrieval
        """
        self.patient_service = patient_service

    def retrieve_all_vital_signs(
        self,
        patient_id: str,
        start_date: str,
        end_date: str,
        table_names: Optional[List[str]] = None,
        user_role: Optional[str] = None
    ) -> Dict:
        """
        Retrieve vital signs data from all relevant tables using a single consolidated query.
        
        Parameters
        ----------
        patient_id: str
            Patient ID to filter by
        start_date: str
            Start date for filtering in format YYYY-MM-DD or YYYY-MM-DD HH:MM
        end_date: str
            End date for filtering in format YYYY-MM-DD or YYYY-MM-DD HH:MM
        table_names: Optional[List[str]]
            Optional list of table names to query. If None, queries all vital sign tables.
        user_role: Optional[str]
            User's role for role-based filtering. If None, no role-based filtering is applied.
            
        Returns
        -------
        Dict
            FHIR Bundle containing all vital signs data
            
        Raises
        ------
            ValidationError: If any input validation fails
        """
        # If no specific tables are requested, use all vital signs tables
        if table_names is None:
            table_names = VITAL_SIGNS_TABLES
        else:
            # Filter out any table names that are not in the vital signs list
            table_names = [t for t in table_names if t in VITAL_SIGNS_TABLES]

        # Apply role-based table filtering
        if user_role:
            if user_role == 'medical':
                # Medical staff can only access basic vital signs
                table_names = [t for t in table_names if t in ['temperature', 'blood_pressure', 'heart_rate']]
            elif user_role == 'admin':
                # Admin can only access operational tables
                table_names = [t for t in table_names if t in OPERATIONAL_TABLES]
            else:
                # Other roles get no access
                return self.patient_service.create_fhir_bundle([])

        # Pre-validate inputs for all tables before querying
        validation_errors = self._validate_input_for_all_tables(
            patient_id, start_date, end_date, table_names
        )
        
        # If validation errors found, raise the first error
        if validation_errors:
            first_error = validation_errors[0]
            raise ValidationError(f"{first_error['field']}: {first_error['error']}")
                
        # Prepare request data
        request_data = {
            'id_patient': patient_id,
            'date_range': {
                'min_date': start_date,
                'max_date': end_date
            }
        }
        
        try:
            # Execute consolidated query across all tables
            consolidated_results = filter_data_consolidated(
                self.patient_service.db_session,
                request_data,
                table_names,
                MODEL_REGISTRY
            )
            
            # Collect all FHIR resources
            all_resources = []
            id_counters = {}  # Keep track of ID counts per table
            
            # Process results from each table
            for table_name, table_results in consolidated_results.items():
                # Get the prefix for this table
                prefix = RESOURCE_ID_PREFIXES.get(table_name, "res")
                
                # Initialize counter for this table if not already done
                if table_name not in id_counters:
                    id_counters[table_name] = 1
                
                # Process each result from this table
                for item in table_results:
                    # Convert to HL7 and then FHIR
                    hl7_message = item.to_hl7_v2()
                    resource = self.patient_service._convert_hl7_to_fhir(hl7_message, table_name)
                    
                    if resource:
                        # Update the ID using the appropriate prefix
                        if "id" in resource:
                            resource["id"] = f"{prefix}-{id_counters[table_name]}"
                            id_counters[table_name] += 1
                        
                        all_resources.append(resource)
            
            # Create the combined FHIR Bundle using PatientService's method
            return self.patient_service.create_fhir_bundle(all_resources)
            
        except Exception as e:
            raise ValidationError(f"Error retrieving vital signs data: {str(e)}")
        
    def _validate_input_for_all_tables(
        self,
        patient_id: str,
        start_date: str,
        end_date: str,
        table_names: List[str]
    ) -> List[Dict]:
        """
        Validate input data for all tables before starting threads.
        
        Parameters
        ----------
        patient_id: str
            Patient ID to validate
        start_date: str
            Start date to validate
        end_date: str
            End date to validate
        table_names: List[str]
            List of table names to validate against
            
        Returns
        -------
        List[Dict]
            List of validation errors, empty if no errors
        """
        errors = []
        
        # Validate patient ID and date range for each table
        for table_name in table_names:
            table_mapping = TABLE_FIELD_MAPPING.get(table_name)
            if not table_mapping:
                errors.append({
                    'field': 'table_name',
                    'error': f'Invalid table name: {table_name}'
                })
                continue
                
            id_field = table_mapping['id_field']
            date_field = table_mapping['date_field']
            
            # Validate ID and date values
            validation_data = {
                id_field: patient_id,
                date_field: {
                    "min_date": start_date,
                    "max_date": end_date
                }
            }
            
            # Generate validation response
            validation_results = generate_json_validation_response(validation_data)
            
            # Check for errors
            for field, result in validation_results.items():
                if result['error_msg']:
                    errors.append({
                        'field': field,
                        'error': result['error_msg']
                    })
        
        return errors 