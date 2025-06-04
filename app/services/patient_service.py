#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Patient service module for handling patient data operations.

This module provides services for retrieving and managing patient data across different tables.
It handles all business logic, data validation, and error handling for the patient data API.
"""

# Import modules #
#----------------#

from datetime import datetime
from typing import Dict, List, Optional, Type, Union

from sqlalchemy.orm import Session

# Import project modules #
#------------------------#

from app.constants.operational_tables import OPERATIONAL_TABLES
from app.constants.table_mappings import TABLE_FIELD_MAPPING
from app.db import BaseModel, filter_data
from app.exceptions import DatabaseError, ValidationError
from app.models.patient_models import TABLE_MODEL_MAP
from app.utils.fhir_formatter import format_operational_data_fhir, format_vital_signs_fhir
from app.utils.form_field_validations import (
    generate_json_validation_response,
    validate_date_field_support,
)
from app.utils.loinc_mappings import LOINC_MAPPINGS
from app.utils.time_formatters import dt_to_string, parse_dt_string

# Define classes and methods #
#----------------------------#  

class PatientService:
    """
    Service class for handling patient data operations.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialise the PatientService with a database session.
        
        Parameters
        ----------
        db_session: Session
            SQLAlchemy database session
        """
        self.db_session = db_session

    # Public Methods #
    #----------------#

    def retrieve_patient_data(self, request_data: Dict, model_class: Optional[Type[BaseModel]] = None) -> Dict:
        """
        Main method for retrieving patient data with validation and error handling.
        
        Parameters
        ----------
        request_data: Dict
            Dictionary containing the request data with:
                - table_name: Name of the table to query
                - id_patient: Patient ID value
                - date_range: Dictionary with min_date and max_date for date range
        model_class: Optional[Type[BaseModel]]
            Optional SQLAlchemy model class to use. If not provided, will be determined from table_name.
            
        Returns
        -------
        Dict
            Dictionary containing:
                - data: List of patient data records
                - count: Number of records found
                
        Raises
        ------
        ValidationError
            If request data validation fails
        DatabaseError
            If database operation fails
        """
        try:
            # Validate request data
            self._validate_request_data(request_data)
            
            # Get model class and table name
            table_name = request_data.get('table_name')
            if model_class is None:
                model_class = self.get_model_for_table(table_name)
            else:
                # If model_class is provided, find the corresponding table name
                table_name = next((name for name, model in TABLE_MODEL_MAP.items() if model == model_class), None)
            
            # Get filtered data
            filtered_data = filter_data(
                self.db_session,
                request_data,
                model_class=model_class
            )

            # Convert model instances to HL7 v2 messages
            hl7_v2_messages = [item.to_hl7_v2() for item in filtered_data]
            
            # Convert HL7 v2 messages to FHIR resources
            fhir_resources = [res for res in (self._convert_hl7_to_fhir(msg, table_name)
                                              for msg in hl7_v2_messages) 
                                              if res is not None]
            
            # Return as FHIR Bundle using the bundle creation method
            return self.create_fhir_bundle(fhir_resources)
        
        except ValueError as e:
            raise ValidationError(str(e))
        except Exception as e:
            raise DatabaseError(f"Database error: {str(e)}")

    def get_patient_data_across_tables(
        self,
        patient_id: str,
        table_names: Optional[List[str]] = None,
        start_date: Optional[Union[str, datetime]] = None,
        end_date: Optional[Union[str, datetime]] = None
    ) -> Dict[str, List[Dict]]:
        """
        Get patient data across multiple tables.
        
        Parameters
        ----------
        patient_id: str
            Patient ID to filter by
        table_names: Optional[List[str]]
            Optional list of table names to query. If None, queries all tables.
        start_date: Optional[Union[str, datetime]]
            Optional start date for filtering
        end_date: Optional[Union[str, datetime]]
            Optional end date for filtering
            
        Returns
        -------
            Dictionary mapping table names to lists of patient data
        """
        if table_names is None:
            table_names = list(TABLE_MODEL_MAP.keys())
        
        all_resources = []
        for table_name in table_names:
            try:
                # Build request data for each table
                request_data = {
                    'table_name': table_name,
                    'id_patient': patient_id
                }
                
                # Only add date range if the table supports it
                table_mapping = TABLE_FIELD_MAPPING.get(table_name)
                if table_mapping and table_mapping['date_field'] is not None:
                    request_data['date_range'] = {
                        'min_date': start_date if isinstance(start_date, str) else start_date.isoformat() if start_date else None,
                        'max_date': end_date if isinstance(end_date, str) else end_date.isoformat() if end_date else None
                    }
                
                # Get data for the table
                data = self.retrieve_patient_data(request_data)
                if data and 'entry' in data:
                    all_resources.extend(data['entry'])
            except ValueError:
                # Skip tables that don't have patient ID fields
                continue
            except ValidationError as e:
                # Log validation errors but continue processing other tables
                print(f"Validation error for table {table_name}: {str(e)}")
                continue
        
        # Create a single FHIR bundle with all resources
        return self.create_fhir_bundle(all_resources)

    def handle_error(self, error: Exception) -> Dict:
        """
        Handle different types of errors uniformly.
        
        Parameters
        ----------
        error: Exception
            The exception to handle
            
        Returns
        -------
            Dictionary containing error details
        """
        if isinstance(error, ValidationError):
            return {
                'field': 'validation',
                'error': str(error)
            }
        elif isinstance(error, DatabaseError):
            return {
                'field': 'database',
                'error': str(error)
            }
        else:
            return {
                'field': 'server',
                'error': str(error)
            }

    def get_model_for_table(self, table_name: str) -> Optional[Type[BaseModel]]:
        """
        Get the model class for a given table name.
        
        Parameters
        ----------
        table_name: str
            Name of the table
            
        Returns
        -------
            Model class if found, None otherwise
        """
        return TABLE_MODEL_MAP.get(table_name.lower())

    def create_fhir_bundle(self, resources: List[Dict]) -> Dict:
        """
        Create a FHIR bundle from a list of resources.
        
        Parameters
        ----------
        resources: List[Dict]
            List of FHIR resources to include in the bundle
            
        Returns
        -------
        Dict
            FHIR Bundle containing the resources
        """
        # Filter out any None or invalid resources
        valid_resources = [res for res in resources if res and isinstance(res, dict)]
        
        # Create the bundle
        bundle = {
            'resourceType': 'Bundle',
            'type': 'searchset',
            'total': len(valid_resources),
            'entry': []
        }
        
        # Add each resource to the bundle
        for resource in valid_resources:
            if 'resource' in resource:
                # If the resource is already in the correct format
                bundle['entry'].append(resource)
            else:
                # If the resource needs to be wrapped
                bundle['entry'].append({
                    'resource': resource
                })
        
        return bundle

    # Internal Methods #
    #------------------#

    def _validate_request_data(self, request_data: Dict) -> None:
        """
        Validate request data before processing.
        
        Parameters
        ----------
        request_data: Dict
            Dictionary containing the request data with:
                - table_name: Name of the table to query
                - id_patient: Patient ID value
                - date_range: Optional dictionary with min_date and max_date for date range
        
        Raises
        ------
        ValidationError
            If validation fails
        """
        if not request_data:
            raise ValidationError("No medical data provided")

        # Check if ID value is present
        if 'id_patient' not in request_data or not request_data['id_patient']:
            raise ValidationError("Missing ID value for the patient")

        # Check if the table supports date filtering and if date range is provided
        table_name = request_data.get('table_name')
        has_date_field = 'date_range' in request_data and request_data['date_range']
        validate_date_field_support(table_name, has_date_field)

        # Validate field values
        validation_results = generate_json_validation_response(request_data)
        for field, result in validation_results.items():
            if result['error_msg']:
                raise ValidationError(f"{field}: {result['error_msg']}")

    def _model_to_dict(self, model_instance: BaseModel) -> Dict:
        """
        Convert a model instance to a dictionary.
        
        Parameters
        ----------
        model_instance: BaseModel
            SQLAlchemy model instance
            
        Returns
        -------
        Dict
            Dictionary representation of the model
        """
        result = {}
        for column in model_instance.__table__.columns:
            value = getattr(model_instance, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result
    
    def _format_fhir_dt(self, datetime_str_hl7: str) -> Optional[str]:
        """
        Format an HL7 v2.X-compliant datetime string to FHIR datetime format.
        """
        timestamp_obj = parse_dt_string(datetime_str_hl7, dt_fmt_str="%Y%m%d%H%M%S")
        timestamp_str = dt_to_string(timestamp_obj, dt_fmt_str="%Y-%m-%d %H:%M:%S")
        timestamp_obj_isoformat = datetime.fromisoformat(timestamp_str)
        return timestamp_obj_isoformat

    def _convert_hl7_to_fhir(self, hl7_message: str, table_name: str) -> Dict:
        """
        Convert an HL7 v2 message to a FHIR v5 resource.
        """
        # Parse the HL7 message
        segments = hl7_message.split('\r')
        
        # Extract relevant information from MSH segment
        msh_segment = segments[0].split('|')
        message_type = msh_segment[8].split('^')
        
        # Validate message type (should be ORU^R01 for observation results)
        if message_type[0] != 'ORU' or message_type[1] != 'R01':
            return None
        
        # Extract patient information from PID segment
        pid_segment = segments[1].split('|')
        patient_id = pid_segment[3].split('^')[0]
        
        # Robustly find the OBX segment
        obx_segment = next((s.split('|') for s in segments if s.startswith('OBX')), None)
        if not obx_segment:
            return None
        value = obx_segment[5] if len(obx_segment) > 5 else ''
        unit = obx_segment[6] if len(obx_segment) > 6 and obx_segment[6] else ''
        ref_range = obx_segment[7] if len(obx_segment) > 7 and obx_segment[7] else ''
        
        # If value is empty or only whitespace, omit this record from FHIR output
        if not value or value.strip() == '':
            return None
        
        # Get the LOINC mapping information for this table
        loinc_info = LOINC_MAPPINGS[table_name]
        
        # Prepare register_datetime and observation_datetime safely
        register_datetime = (
            self._format_fhir_dt(msh_segment[7])
            if len(msh_segment) > 7 and msh_segment[7] and msh_segment[7].strip() != ''
            else None
        )
        observation_datetime = (
            self._format_fhir_dt(obx_segment[14])
            if len(obx_segment) > 14 and obx_segment[14] and obx_segment[14].strip() != ''
            else None
        )
        
        # Handle observation notes safely
        observation_notes = (
            obx_segment[8] 
            if len(obx_segment) > 8 and obx_segment[8] and obx_segment[8].strip() != ''
            else None
        )
        
        # Use the appropriate formatter based on whether this is operational data
        if table_name in OPERATIONAL_TABLES:
            return format_operational_data_fhir(
                patient_id=patient_id,
                measurement_id=obx_segment[1],
                value=value,
                units=unit,
                reference_range=ref_range,
                register_datetime=register_datetime,
                observation_datetime=observation_datetime,
                observation=observation_notes,
                loinc_code=loinc_info.loinc_code,
                loinc_description=loinc_info.description
            )
        else:
            return format_vital_signs_fhir(
                patient_id=patient_id,
                measurement_id=obx_segment[1],
                value=value,
                units=unit,
                reference_range=ref_range,
                register_datetime=register_datetime,
                observation_datetime=observation_datetime,
                observation=observation_notes,
                loinc_code=loinc_info.loinc_code,
                loinc_description=loinc_info.description
            )