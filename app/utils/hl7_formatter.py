#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HL7 message formatting utilities.

This module provides helper functions and constants for formatting patient data
into HL7 v2.x messages.
"""

# Import modules #
#----------------#

# Import from standard library first
from datetime import datetime
from typing import Any
from dateutil import parser

# IMPORTANT: Circular Import Prevention
# When creating a Message with ORU_R01, hl7apy implicitly tries to load v2_5 module.
# If this module isn't already loaded when Message is first accessed, it creates a 
# circular import that fails on first run but succeeds on subsequent runs.
# Explicitly importing v2_5 before any other hl7apy components prevents this issue.
import hl7apy.v2_5
from hl7apy.core import Message

# Import project modules #
#------------------------#

from app.utils.date_and_time_utils import get_current_datetime
from app.utils.time_formatters import dt_to_string

# Define functions #
#------------------#

def format_datetime(dt: datetime) -> str:
    """Format datetime for HL7 messages."""
    try:
        # Strip microseconds and format to HL7 standard format
        dt_without_micros = dt.replace(microsecond=0)
        return dt_to_string(dt_without_micros, dt_fmt_str="%Y%m%d%H%M%S")
    except Exception as e:
        return ""

def generate_message_control_id() -> str:
    """Generate a unique message control ID."""
    return get_current_datetime(time_fmt_str="%Y%m%d%H%M%S%f")

def format_vital_signs_message(
    patient_id: str,
    measurement_type: str,
    measurement_id: str,
    value: Any,
    register_datetime: datetime = None,
    units: str = "",
    reference_range: str = "",
    abnormal_flags: str = "",
    observation_datetime: str = None,
    observation: str = None,
    period_start: str = None,
    period_end: str = None,
    visit_number: str = "",
    patient_class: str = "I",  # I=Inpatient, O=Outpatient, E=Emergency
    location: str = "",
    attending_doctor: str = "",
    hospital_service: str = "",
    priority: str = "R",  # R=Routine, S=Stat, A=ASAP
    specimen_source: str = "",
    ordering_provider: str = ""
) -> str:
    """
    Format vital signs data into an HL7 message using hl7apy library.
    """
    try:
        # Create a new HL7 message
        message = Message("ORU_R01")
        
        # MSH - Message Header
        msh = message.msh
        msh.msh_3 = "OSAKIDETZA"
        msh.msh_4 = "PATIENT_DATA_RETRIEVER"
        msh.msh_5 = "REMOTE_SYSTEM"
        msh.msh_6 = "REMOTE_APP"
        msh.msh_7 = format_datetime(datetime.now())
        msh.msh_9 = "ORU^R01"
        msh.msh_10 = generate_message_control_id()
        msh.msh_11 = "P"
        # This version specification (2.5) must match the imported hl7apy.v2_5 module.
        # The Message("ORU_R01") constructor above implicitly requires v2_5,
        # which is why we import hl7apy.v2_5 explicitly at the top of this file.
        msh.msh_12 = "2.5"
        
        # PID - Patient Identification
        pid = message.add_segment("PID")
        pid.pid_1 = "1"
        pid.pid_3 = patient_id
        
        # PV1 - Patient Visit
        pv1 = message.add_segment("PV1")
        pv1.pv1_1 = "1"
        pv1.pv1_2 = patient_class
        pv1.pv1_3 = location
        pv1.pv1_7 = attending_doctor
        pv1.pv1_10 = hospital_service
        pv1.pv1_19 = visit_number
        
        # OBR - Observation Request
        obr = message.add_segment("OBR")
        obr.obr_1 = "1"
        obr.obr_2 = measurement_id
        obr.obr_3 = measurement_type
        obr.obr_4 = priority
        
        # Format dates for OBR_6 and OBR_7
        if period_start:
            try:
                # Parse with microseconds support
                period_start_dt = parser.parse(str(period_start))
                obr.obr_6 = format_datetime(period_start_dt)
            except (ValueError, TypeError):
                obr.obr_6 = ""
        elif observation_datetime:
            try:
                # Parse with microseconds support
                observation_dt = parser.parse(str(observation_datetime))
                obr.obr_6 = format_datetime(observation_dt)
            except (ValueError, TypeError):
                obr.obr_6 = ""
        elif register_datetime:
            obr.obr_6 = format_datetime(register_datetime)
        else:
            obr.obr_6 = ""
            
        if period_end:
            try:
                # Parse with microseconds support
                period_end_dt = parser.parse(str(period_end))
                obr.obr_7 = format_datetime(period_end_dt)
            except (ValueError, TypeError):
                obr.obr_7 = ""
        elif register_datetime:
            obr.obr_7 = format_datetime(register_datetime)
        else:
            obr.obr_7 = ""
            
        obr.obr_15 = specimen_source
        obr.obr_16 = ordering_provider
        obr.obr_25 = "F"  # Final result
        
        # OBX - Observation/Result
        obx = message.add_segment("OBX")
        obx.obx_1 = "1"
        obx.obx_2 = "NM"  # Numeric
        obx.obx_3 = f"{measurement_type}^{measurement_type.replace('_', ' ').title()}"
        obx.obx_5 = str(value)
        obx.obx_6 = units if units else ""
        obx.obx_7 = reference_range if reference_range else ""
        obx.obx_8 = abnormal_flags
        obx.obx_11 = "F"  # Final result
        obx.obx_14 = format_datetime(register_datetime) if register_datetime else ""
        
        if observation:
            # NTE - Notes and Comments
            nte = message.add_segment("NTE")
            nte.nte_1 = "1"
            nte.nte_3 = observation
        
        # Convert message to string
        return str(message.to_er7())
            
    except Exception as e:
        raise