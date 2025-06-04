#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FHIR formatter module for converting HL7 v2 messages to FHIR v5 resources.

This module provides functions for converting HL7 v2 messages to FHIR v5 resources.
It handles the conversion of different types of observations and measurements.
"""

# Import modules #
#----------------#

# Standard library #
from datetime import datetime, timezone
from typing import Dict, Optional, Union

# FHIR resources #
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.observation import Observation
from fhir.resources.period import Period
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference

# Define functions #
#------------------#

def format_vital_signs_fhir(
    patient_id: str,
    measurement_id: str,
    value: Union[float, str],
    register_datetime: Optional[datetime] = None,
    units: Optional[str] = None,
    reference_range: Optional[str] = None,
    observation_datetime: Optional[datetime] = None,
    observation: Optional[str] = None,
    period_start: Optional[str] = None,
    period_end: Optional[str] = None,
    loinc_code: Optional[str] = None,
    loinc_description: Optional[str] = None
) -> Dict:
    """
    Convert vital signs data to FHIR v5 Observation resource.
    
    Parameters
    ----------
    patient_id : str
        The patient's ID.
    measurement_id : str
        The unique identifier for this measurement.
    value : Union[float, str]
        The measurement value.
    register_datetime : Optional[datetime]
        The date and time when the measurement was registered.
    units : Optional[str]
        The units of measurement.
    reference_range : Optional[str]
        The reference range for the measurement.
    observation_datetime : Optional[datetime]
        The date and time when the observation was made.
    observation : Optional[str]
        Additional observations or notes.
    period_start : Optional[str]
        The start of the observation period.
    period_end : Optional[str]
        The end of the observation period
    loinc_code : Optional[str]
        The LOINC code for this measurement.
    loinc_description : Optional[str]
        The description of the LOINC code.
        
    Returns
    -------
    Dict
        A FHIR v5 Observation resource as a dictionary.
    """
    # Ensure datetimes are timezone-aware
    if observation_datetime and observation_datetime.tzinfo is None:
        observation_datetime = observation_datetime.replace(tzinfo=timezone.utc)
    if register_datetime and register_datetime.tzinfo is None:
        register_datetime = register_datetime.replace(tzinfo=timezone.utc)

    # Create the base Observation resource with all required fields as kwargs
    obs = Observation.model_construct(
        resourceType="Observation",
        status="final",
        id=measurement_id,
        effectiveDateTime=observation_datetime if observation_datetime else None,
        issued=register_datetime if register_datetime else None
    )
    
    # Set the category (vital signs)
    obs.category = [
        CodeableConcept.model_construct(
            coding=[
                Coding.model_construct(
                    system="http://terminology.hl7.org/CodeSystem/observation-category",
                    code="vital-signs",
                    display="Vital Signs"
                )
            ]
        )
    ]
    
    # Set the code using the provided LOINC information
    obs.code = CodeableConcept.model_construct(
        coding=[
            Coding.model_construct(
                system="http://loinc.org",
                code=loinc_code,
                display=loinc_description
            )
        ]
    )
    
    # Set the subject (patient)
    obs.subject = Reference.model_construct(
        reference=f"Patient/{patient_id}"
    )
    
    # Set the value with proper unit handling
    if loinc_code == "85354-9":  # Blood pressure - special handling
        # Split the string value (e.g. "120/80") into systolic and diastolic
        try:
            systolic, diastolic = str(value).split('/')
            # Create components for systolic and diastolic pressure
            obs.component = [
                {
                    "code": {
                        "coding": [
                            {
                                "system": "http://loinc.org",
                                "code": "8480-6",
                                "display": "Systolic blood pressure"
                            }
                        ]
                    },
                    "valueQuantity": {
                        "value": float(systolic),
                        "unit": units,
                        "system": "http://unitsofmeasure.org",
                        "code": units
                    }
                },
                {
                    "code": {
                        "coding": [
                            {
                                "system": "http://loinc.org",
                                "code": "8462-4",
                                "display": "Diastolic blood pressure"
                            }
                        ]
                    },
                    "valueQuantity": {
                        "value": float(diastolic),
                        "unit": units,
                        "system": "http://unitsofmeasure.org",
                        "code": units
                    }
                }
            ]
        except (ValueError, AttributeError):
            # If parsing fails, fall back to string representation
            obs.valueString = str(value)
    elif isinstance(value, (int, float)):
        obs.valueQuantity = Quantity.model_construct(
            value=float(value),
            unit=units,
            system="http://unitsofmeasure.org",
            code=units
        )
    else:
        obs.valueString = str(value)
    
    # Set the reference range if provided
    if reference_range:
        # Parse the reference range if it's in the format "min-max"
        try:
            low, high = reference_range.split('-')
            obs.referenceRange = [{
                "low": {
                    "value": float(low),
                    "unit": units,
                    "system": "http://unitsofmeasure.org",
                    "code": units
                },
                "high": {
                    "value": float(high),
                    "unit": units,
                    "system": "http://unitsofmeasure.org",
                    "code": units
                }
            }]
        except ValueError:
            # If parsing fails, use the text format
            obs.referenceRange = [{"text": reference_range}]
    
    # Set the note if provided
    if observation:
        obs.note = [
            {
                "text": observation
            }
        ]
    
    # Set the period if provided
    if period_start or period_end:
        obs.effectivePeriod = Period.model_construct(
            start=period_start,
            end=period_end
        )
    
    # Return the dictionary with all datetimes converted to ISO strings
    return _convert_datetimes_to_iso(obs.model_dump())

def _convert_datetimes_to_iso(obj):
    """
    Recursively convert all datetime objects in a dict/list to ISO 8601 strings.
    """
    if isinstance(obj, dict):
        return {k: _convert_datetimes_to_iso(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_datetimes_to_iso(i) for i in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj

def format_operational_data_fhir(
    patient_id: str,
    measurement_id: str,
    value: str,
    units: Optional[str] = None,
    reference_range: Optional[str] = None,
    register_datetime: Optional[datetime] = None,
    observation_datetime: Optional[datetime] = None,
    observation: Optional[str] = None,
    loinc_code: str = "UNKNOWN",
    loinc_description: str = "Operational data"
) -> Dict:
    """
    Format operational data as a FHIR Observation resource.
    
    Parameters
    ----------
    patient_id: str
        Patient ID
    measurement_id: str
        Measurement ID
    value: str
        Measurement value
    units: Optional[str]
        Units of measurement
    reference_range: Optional[str]
        Reference range for the measurement
    register_datetime: Optional[datetime]
        Registration datetime
    observation_datetime: Optional[datetime]
        Observation datetime
    observation: Optional[str]
        Additional observation notes
    loinc_code: str
        LOINC code for the measurement
    loinc_description: str
        LOINC description for the measurement
        
    Returns
    -------
    Dict
        FHIR Observation resource
    """
    # Create the basic resource
    resource = {
        "resourceType": "Observation",
        "id": measurement_id,
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "activity",
                        "display": "Activity"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": loinc_code,
                    "display": loinc_description
                }
            ]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        }
    }
    
    # Add value
    if value is not None:
        resource["valueString"] = str(value)
    
    # Add effective time if available
    if observation_datetime:
        resource["effectiveDateTime"] = observation_datetime.isoformat()
    elif register_datetime:
        resource["effectiveDateTime"] = register_datetime.isoformat()
    
    # Add note if available
    if observation:
        resource["note"] = [{"text": observation}]
    
    return resource

# Parameters and constants #
#--------------------------#

# Timestamp format string #
time_fmt_str = "%Y-%m-%dT%H:%M:%S%z"