#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Patient Data Retrieval API - Main Application Module

This module serves as the entry point for a Flask-based REST API 
that handles medical patient data retrieval.

For detailed API documentation, please refer to:
1. Swagger UI: 
   - http://localhost:5013/docs when running locally
   - http://localhost:5010/docs when running with Docker
2. OpenAPI specification: 
   - docs/openapi.yaml
3. Documentation overview: 
   - docs/README.md

IMPORTANT NOTE ON SWAGGER UI EXAMPLES (Flask-RESTX 1.3.0 and similar versions):

- Due to a long-standing limitation/bug in Flask-RESTX 
  (see: https://github.com/python-restx/flask-restx/issues/391),
  the OpenAPI/Swagger UI will NOT display response examples 
  for nested lists of objects (e.g., lists of resources) 
  unless the example is provided in every nested model.
- The only reliable workaround (as of Flask-RESTX 1.3.0) 
  is to DUPLICATE the example in both the parent and all 
  nested models (including lists).
- Attempts to use the `example` or `examples` keyword in 
  @api.response or @api.marshal_with decorators will NOT 
  work for nested lists in these versions.
- This duplication workaround is expected to be unnecessary 
  in future versions of Flask-RESTX, so if you upgrade, 
  check the release notes and test if the duplication is 
  still required.

Summary: Example duplication in model definitions (especially 
for nested lists) is intentional and required for correct 
Swagger UI display in current Flask-RESTX.
"""

#----------------#
# Import modules #
#----------------#

import os
from flask import Flask
from flask_cors import CORS
from flask_restx import Api

#------------------------#
# Import project modules #
#------------------------#

from app.config import DATABASE_CREDENTIALS
from app.db import init_db

#------------------#
# Define functions #
#------------------#

def create_app():
    """Create and configure the Flask application."""
    # Create the Flask app instance 
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    # Set the secret key for the app
    app.secret_key = os.environ.get('FLASK_SECRET_KEY', '<gXg17Vh+q1:e)d[')

    # Disable sorting of JSON keys
    app.json.sort_keys = False

    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
        }
    }

    # Create the API instance with specific configuration
    api = Api(
        app,
        version='3.4',
        title='Patient Data Retrieval API',
        description='API for retrieving and filtering patient medical data',
        doc='/docs',
        prefix='/api',
        default='Patient Data',
        default_label='Patient data operations',
        validate=True,
        ordered=True,
        authorizations=authorizations,
        security='Bearer',
    )

    # Import API modules after creating the API instance
    from app.api.auth_api import auth_ns
    # from app.api.data_retrieval_api import api as patient_data_ns  # REMOVE
    from app.api.vital_signs_api import vital_signs_ns
    from app.api.operational_data_api import api as operational_data_ns
    from app.api.metadata_api import metadata_ns

    # Add the namespaces to the API
    api.add_namespace(auth_ns)
    # api.add_namespace(patient_data_ns)  # REMOVE
    api.add_namespace(vital_signs_ns)
    api.add_namespace(operational_data_ns)
    api.add_namespace(metadata_ns)

    return app

# Application entry point #
#-------------------------#

if __name__ == '__main__':
    # Create the Flask application
    app = create_app()

    # Initialise the database before starting the app
    init_db(config=DATABASE_CREDENTIALS)

    # Run the app with debug mode on port 5013 (local)
    port = int(os.environ.get('PORT', 5013))
    app.run(debug=True, host='0.0.0.0', port=port)
