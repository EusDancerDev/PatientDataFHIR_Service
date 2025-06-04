#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Custom exceptions for the Patient Data Retrieval API.
"""

# Define classes #
#----------------#

class PatientServiceError(Exception):
    """Base exception for patient service errors"""
    pass

class ValidationError(PatientServiceError):
    """Validation error in patient service"""
    pass

class DatabaseError(PatientServiceError):
    """Database error in patient service"""
    pass 