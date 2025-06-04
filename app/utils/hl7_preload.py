#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HL7 preloader module.

This module preloads all necessary HL7 components to avoid circular imports
when the application starts. Import this module early in the application
startup sequence.
"""

# IMPORTANT: Circular Import Prevention
# This explicit import of hl7apy.v2_5 is crucial for preventing circular imports.
# 
# The issue occurs because:
# 1. When creating a Message with ORU_R01, hl7apy tries to load the v2_5 module
# 2. If this happens during application startup while other modules are still loading,
#    it creates a circular dependency
# 3. This fails on the first run but succeeds on subsequent runs (after the module is cached)
#
# By explicitly importing v2_5 first and having this module loaded early in the
# application's __init__.py, we ensure the dependency is fully resolved before
# any other component tries to use it.
import hl7apy.v2_5

# Import other commonly used HL7 components
from hl7apy.core import Message

# Define a function to validate that preloading was successful
def validate_hl7_preload():
    """
    Validate that HL7 modules were preloaded successfully.
    """
    # Test creating a simple message to ensure everything is loaded
    try:
        test_message = Message("ORU_R01")
        test_message.msh.msh_12 = "2.5"
        return True
    except Exception as e:
        print(f"Error preloading HL7 modules: {e}")
        return False 