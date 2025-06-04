#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Import modules #
#----------------#

import jwt
import datetime

# Import project modules #
#------------------------#

from app.utils.date_and_time_utils import get_current_datetime

# Define secret key #
#-------------------#

SECRET_KEY = "your-very-secret-key"  # Replace with a secure value in production

# Define functions #
#------------------#

def generate_token(username, role):
    """
    Generate a JWT token for the given username and role.
    """
    payload = {
        "username": username,
        "role": role,
        "exp": get_current_datetime() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None 