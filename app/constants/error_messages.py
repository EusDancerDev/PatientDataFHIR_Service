#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Error Messages Module

This module contains all error messages used throughout the application.
These messages are used for form field validation and other error handling.
"""

# Date validation errors
INVALID_DATE_FORMAT_ERROR = "dates must be in 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM' format. For example: '2025-03-26' or '2025-03-26 14:30'"
INVALID_DATE_RANGE_ERROR = "'min_date' must be less than or equal to 'max_date'"
INVALID_DATE_RANGE_FORMAT_ERROR = "date range filtering requires a dictionary with 'min_date' and 'max_date' keys"
MISSING_DATE_VALUES_ERROR = "both 'min_date' and 'max_date' are required for date range filtering"

# Field validation errors
INVALID_ID_FORMAT_ERROR = "ID must be a 10 character string containing only digits"
INVALID_ID_TYPE_ERROR = "ID must be a string with numeric characters" 