#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test module for variable name type hints.

This module demonstrates the usage of type hints in Python,
specifically focusing on dictionary and integer type annotations.
"""

# Define test data #
#------------------#

# Dictionary mapping Spanish terms to English descriptions
s: dict[str, str] = {
    "saturacion_oxigeno": "Oxygen saturation in Blood",
    "temperatura": "Body temperature",
    "presion_arterial": "Blood pressure panel",
    "frecuencia_cardiaca": "Heart rate",
    "frecuencia_respiratoria": "Respiratory rate",
}

# Integer test value
i: int = 1

# Output results #
#----------------#

print(s, i)