#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import modules #
#----------------#

from argon2 import PasswordHasher
from typing import List, Dict

# Define classes and methods #
#----------------------------#

class PasswordHandler:
    """
    Utility class for password handling using argon2.
    """
    def __init__(self):
        self.ph = PasswordHasher()

    def hash_password(self, password: str) -> str:
        """
        Hash a password using argon2.
        
        Parameters
        ----------
        password: str
            The password to hash
            
        Returns
        -------
        str
            The hashed password
        """
        return self.ph.hash(password)

    def verify_password(self, hash: str, password: str) -> bool:
        """
        Verify a password against its hash.
        
        Parameters
        ----------
        hash: str
            The hashed password
        password: str
            The password to verify
            
        Returns
        -------
        bool
            True if the password matches the hash, False otherwise
        """
        try:
            self.ph.verify(hash, password)
            return True
        except Exception:
            return False

def generate_test_passwords() -> List[Dict[str, str]]:
    """
    Generate test data with hashed passwords.
    
    Returns:
        List[Dict[str, str]]: List of dictionaries containing test data
    """
    ph = PasswordHasher()
    
    # Test data with unique passwords for each user
    test_data = [
        # British names
        {"username": "John", "usersurname": "Smith", "role": "medical", "plain_password": "JohnS2024!"},
        {"username": "Emma", "usersurname": "Wilson", "role": "admin", "plain_password": "EmmaW2024!"},
        {"username": "James", "usersurname": "Brown", "role": "medical", "plain_password": "JamesB2024!"},
        
        # Spanish names
        {"username": "María", "usersurname": "García", "role": "admin", "plain_password": "MariaG2024!"},
        {"username": "Carlos", "usersurname": "Rodríguez", "role": "medical", "plain_password": "CarlosR2024!"},
        {"username": "Ana", "usersurname": "Martínez", "role": "medical", "plain_password": "AnaM2024!"},
        
        # Basque names
        {"username": "Aitor", "usersurname": "Etxeberria", "role": "admin", "plain_password": "AitorE2024!"},
        {"username": "Maite", "usersurname": "Zubizarreta", "role": "medical", "plain_password": "MaiteZ2024!"},
        {"username": "Iñaki", "usersurname": "Otxoa", "role": "medical", "plain_password": "InakiO2024!"},
        {"username": "Nerea", "usersurname": "Urrutia", "role": "admin", "plain_password": "NereaU2024!"}
    ]
    
    # Add hashed passwords to each entry
    for entry in test_data:
        entry["password"] = ph.hash(entry["plain_password"])
        # Remove the plain password from the final data
        del entry["plain_password"]
    
    return test_data 