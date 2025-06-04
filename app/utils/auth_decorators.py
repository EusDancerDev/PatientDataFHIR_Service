#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import modules #
#----------------#

from functools import wraps
from flask import request

# Import project modules #
#------------------------#

from app.utils.jwt_handler import decode_token

# Define classes and methods #
#----------------------------#

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return {'message': 'Token is missing!'}, 401
        token = auth_header.split(' ')[1]
        data = decode_token(token)
        if not data:
            return {'message': 'Token is invalid or expired!'}, 401
        request.user = data  # Attach user info to request
        return f(*args, **kwargs)
    return decorated 