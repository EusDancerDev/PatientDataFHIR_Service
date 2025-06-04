#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from flask import request, current_app
from flask_restx import Resource, fields, Namespace
from sqlalchemy.orm import Session

#------------------------#
# Import project modules #
#------------------------#

from app.config import DATABASE_CREDENTIALS
from app.db import init_db
from app.services.auth_service import AuthService
from app.utils.jwt_handler import generate_token
from app.utils.time_formatters import _format_arbitrary_dt

#------------#
# Operations #
#------------#

# Define namespaces #
#-------------------#

# Authentication-related operations within the API
auth_ns = Namespace('auth', description='Authentication operations')

# Define models #
#---------------#

auth_success_response_model = auth_ns.model('AuthSuccessResponse', {
    'success': fields.Boolean(description='Whether authentication was successful', example=True),
    'role': fields.String(description='User role if authentication successful', example='medical'),
    'token': fields.String(description='JWT token to be used in Authorisation header. Format: "Bearer {token}"', example='Bearer eyJhbGciOiJIUzI1NiIs...'),
    'message': fields.String(description='Response message', example='Authentication successful. Use the token in the Authorisation header as: "Bearer {token}"')
})

auth_validation_error_model = auth_ns.model('AuthValidationError', {
    'success': fields.Boolean(description='Whether authentication was successful', example=False),
    'message': fields.String(description='Response message', example='No data provided')
})

auth_authentication_failed_model = auth_ns.model('AuthAuthenticationFailed', {
    'success': fields.Boolean(description='Whether authentication was successful', example=False),
    'message': fields.String(description='Response message', example='Invalid credentials')
})

auth_too_many_requests_model = auth_ns.model('AuthTooManyRequests', {
    'success': fields.Boolean(description='Whether authentication was successful', example=False),
    'message': fields.String(description='Too many failed attempts. Please try again in 4m 30s.')
})

auth_internal_server_error_model = auth_ns.model('AuthInternalServerError', {
    'success': fields.Boolean(description='Whether authentication was successful', example=False),
    'message': fields.String(description='Authentication error: Database connection failed')
})

# Request models
auth_query_model = auth_ns.model('AuthQuery', {
    'username': fields.String(required=True, description="Staff member's name", example="Emma"),
    'usersurname': fields.String(required=True, description="Staff member's surname", example="Wilson"),
    'password': fields.String(required=True, description="Staff member's password", example="EmmaW2024!")
})

# Define routes #
#---------------#

# Authentication Endpoint (/auth/login)
"""
# Purpose: Authenticates staff members and provides JWT token
# Access: Public
# Response: JWT token and user role if authentication successful
"""
@auth_ns.route('/login')
class AuthResource(Resource):
    """
    Authentication resource for staff members.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_service = AuthService()
        self.engine, self.Session = init_db(DATABASE_CREDENTIALS)

    @auth_ns.doc('post_auth')
    @auth_ns.expect(auth_query_model)
    @auth_ns.response(200, 'Success', auth_success_response_model, example={
        "success": True,
        "role": "medical",
        "token": "Bearer eyJhbGciOiJIUzI1NiIs...",
        "message": "Authentication successful. Use the token in the Authorisation header as: Bearer {token}"
    })
    @auth_ns.response(400, 'Validation Error', auth_validation_error_model, example={
        "success": False,
        "message": "No data provided"
    })
    @auth_ns.response(401, 'Authentication Failed', auth_authentication_failed_model, example={
        "success": False,
        "message": "Invalid credentials"
    })
    @auth_ns.response(429, 'Too Many Requests', auth_too_many_requests_model, example={
        "success": False,
        "message": f"Too many failed attempts. Please try again in {_format_arbitrary_dt(AuthService().block_duration_mins * 60, 0)}."
    })
    @auth_ns.response(500, 'Internal Server Error', auth_internal_server_error_model, example={
        "success": False,
        "message": "Authentication error: Database connection failed"
    })
    def post(self):
        """
        Authenticate a staff member using POST request.
        Credentials must be sent in the request body for security.
        """
        data = request.json
        if not data:
            return {'success': False, 'message': 'No data provided'}, 400
            
        username = data.get('username')
        usersurname = data.get('usersurname')
        password = data.get('password')
        
        if not all([username, usersurname, password]):
            return {'success': False, 'message': 'Missing required parameters'}, 400
            
        return self._authenticate(username, usersurname, password)

    def _authenticate(self, username: str, usersurname: str, password: str):
        """
        Common authentication logic.
        """
        session = self.Session()
        try:
            success, role, error_message = self.auth_service.authenticate(
                session,
                username,
                usersurname,
                password,
                request.remote_addr
            )
            
            if success:
                token = generate_token(username, role)
                return {
                    'success': True,
                    'role': role,
                    'token': f'Bearer {token}',
                    'message': 'Authentication successful. Use the token in the Authorisation header as: "Bearer {token}"'
                }, 200
            else:
                return {
                    'success': False,
                    'message': error_message
                }, 401
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Authentication error: {str(e)}'
            }, 500
        finally:
            session.close() 