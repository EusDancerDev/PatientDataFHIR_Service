#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test module for ISO format date/time handling.

This module contains tests for converting between different datetime formats,
specifically focusing on ISO format conversions.
"""

# Import modules #
#----------------#

from datetime import datetime as dt

# Test data #
#-----------#

timestamp_non_std_str = "20250502123456"
timestamp_obj = dt.strptime(timestamp_non_std_str, "%Y%m%d%H%M%S")
timestamp_str = timestamp_obj.strftime("%Y-%m-%d %H:%M:%S")
timestamp_obj_isoformat = dt.fromisoformat(timestamp_str)

# Output results #
#---------------#

print(timestamp_obj)
print(timestamp_obj_isoformat)