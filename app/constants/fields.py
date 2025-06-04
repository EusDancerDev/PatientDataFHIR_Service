#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fields constants module.

This module derives ID_FIELDS and DATE_FIELDS from TABLE_FIELD_MAPPING
to maintain consistency and avoid manual definition.
"""

# Import project modules #
#------------------------#

from app.constants.table_mappings import TABLE_FIELD_MAPPING

# Define parameters #
#-------------------#

# Derive ID_FIELDS and DATE_FIELDS from TABLE_FIELD_MAPPING
ID_FIELDS = list(set(
    mapping['id_field']
    for mapping in TABLE_FIELD_MAPPING.values()
    if mapping['id_field'] is not None
))

DATE_FIELDS = list(set(
    mapping['date_field']
    for mapping in TABLE_FIELD_MAPPING.values()
    if mapping['date_field'] is not None
))