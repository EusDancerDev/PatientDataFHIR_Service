#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test module for authentication functionality.

This module contains tests for:
1. Password hashing and verification
2. Login endpoint functionality
3. JWT token validation
4. Rate limiting implementation
"""

# Import modules #
#----------------#

import unittest
from datetime import datetime, timedelta
import json

# Import project modules #
#------------------------#

from app.api.auth_api import AuthResource
from app.utils.password_handler import PasswordHandler
from app.models.staff_model import Staff
from app.db import init_db
from app.config import DATABASE_CREDENTIALS

# Define test case classes and methods #
#--------------------------------------#

class TestAuthentication(unittest.TestCase):
    """Test cases for authentication functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Initialize database session
        self.engine, Session = init_db(DATABASE_CREDENTIALS)
        self.session = Session()
        
        # Initialize auth resource
        self.auth_resource = AuthResource()
        
        # Initialize password handler
        self.password_handler = PasswordHandler()

    def tearDown(self):
        """Clean up after tests."""
        self.session.close()

    def test_password_hashing(self):
        """Test password hashing and verification."""
        # Test password
        test_password = "TestPass123!"
        
        # Hash the password
        hashed_password = self.password_handler.hash_password(test_password)
        
        # Verify the password
        self.assertTrue(self.password_handler.verify_password(test_password, hashed_password))
        
        # Test wrong password
        self.assertFalse(self.password_handler.verify_password("WrongPass123!", hashed_password))

    def test_login_endpoint(self):
        """Test the login endpoint."""
        # Test data
        test_credentials = {
            'username': 'test_user',
            'password': 'TestPass123!'
        }
        
        # Test successful login
        response = self.auth_resource.post()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)
        self.assertIn('role', data)
        
        # Test invalid credentials
        test_credentials['password'] = 'WrongPass123!'
        response = self.auth_resource.post()
        self.assertEqual(response.status_code, 401)

    def test_token_validation(self):
        """Test JWT token validation."""
        # Test data
        test_credentials = {
            'username': 'test_user',
            'password': 'TestPass123!'
        }
        
        # Get token
        response = self.auth_resource.post()
        data = json.loads(response.data)
        token = data['token']
        
        # Test token validation
        self.assertTrue(self.auth_resource.validate_token(token))
        
        # Test invalid token
        self.assertFalse(self.auth_resource.validate_token('invalid_token'))

    def test_rate_limiting(self):
        """Test rate limiting functionality."""
        # Test data
        test_credentials = {
            'username': 'test_user',
            'password': 'TestPass123!'
        }
        
        # Make multiple requests
        for _ in range(5):
            response = self.auth_resource.post()
            self.assertEqual(response.status_code, 200)
        
        # Next request should be rate limited
        response = self.auth_resource.post()
        self.assertEqual(response.status_code, 429)

# Main execution #
#----------------#

if __name__ == '__main__':
    unittest.main() 