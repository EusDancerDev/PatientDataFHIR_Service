#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration module for the application.

This module contains application-wide settings and constants.
"""

# %% IMPORT MODULES #

import os

#%% 1. TIME-RELATED PARAMETERS

# Supported date units
PANDAS_DATE_UNIT_LIST = ['D', 'ms', 'ns', 's', 'us']
NUMPY_DATE_UNIT_LIST = ['Y', 'M', 'D', 'h', 'm', 's', 'ms', 'us', 'ns']


# %% 2. DATABASES

# Determine if running in Docker
IS_DOCKER = os.getenv('DOCKER_ENV', 'false').lower() == 'true'

# Database initialisation with credentials
DATABASE_CREDENTIALS = { 
    'username': 'postgres',
    'password': 'admin',
    'host': 'localhost' if not IS_DOCKER else os.getenv('DB_HOST', 'host.docker.internal'),
    'port': os.getenv('DB_PORT', '5432'),
    'database_name': 'KM0'
}

# PostgreSQL error codes and messages
DATABASE_ERROR_CODES = {
    "42P04": "Database already exists",
    "28P01": "Wrong username/password authentication failed",
    "3D000": "Unknown database name",
    "08001": "Unable to establish connection/wrong host name",
    "08006": "Connection failure/connection terminated",
    "42501": "Insufficient privileges"
}