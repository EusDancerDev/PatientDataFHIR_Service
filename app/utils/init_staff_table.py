#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import modules #
#----------------#

import sys
from pathlib import Path

# Add the project root to the Python path #
#----------------------------------------#

project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

# Import project modules #
#------------------------#

from app.db import init_db
from app.config import DATABASE_CREDENTIALS
from app.models.staff_model import Staff
from app.utils.password_handler import generate_test_passwords

# Define functions #
#------------------#

def init_staff_table():
    """
    Initialise the staff table with test data.
    """
    try:
        # Initialise database connection
        _, Session = init_db(DATABASE_CREDENTIALS)
        
        # Create a session
        session = Session()
        
        # Generate test data
        test_data = generate_test_passwords()
        
        # Insert test data
        for entry in test_data:
            staff = Staff(
                username=entry["username"],
                usersurname=entry["usersurname"],
                password=entry["password"],
                role=entry["role"]
            )
            session.add(staff)
        
        # Commit the changes
        session.commit()
        print("Staff table initialised successfully with test data.")
        
    except Exception as e:
        print(f"Error initializing staff table: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    init_staff_table() 