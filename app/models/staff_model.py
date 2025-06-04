#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import modules #
#----------------#

from sqlalchemy import Column, Integer, String, text

# Import project modules #
#------------------------#

from app.db import Base

# Define classes and methods #
#----------------------------#

class Staff(Base):
    """
    SQLAlchemy model for the staff table.
    """
    __tablename__ = 'staff'

    index = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    usersurname = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)  # For argon2 hashes
    role = Column(String(10), nullable=False)

    def __init__(self, username, usersurname, password, role):
        self.username = username
        self.usersurname = usersurname
        self.password = password
        self.role = role

    def __repr__(self):
        return f"<Staff(username='{self.username}', usersurname='{self.usersurname}', role='{self.role}')>"

    @classmethod
    def get_staff_by_credentials(cls, session, username, usersurname):
        """
        Retrieve staff member by username and usersurname only.
        """
        return session.query(cls).filter_by(username=username, usersurname=usersurname).first()

    @classmethod
    def get_staff_by_credentials_with_password(cls, session, username, usersurname, password):
        """
        Retrieve staff member by credentials.
        Uses text() to handle special characters in the query.
        """
        query = text("""
            SELECT * FROM staff 
            WHERE username = :username 
            AND usersurname = :usersurname 
            AND password = :password
        """)
        
        result = session.execute(
            query, 
            {
                'username': username,
                'usersurname': usersurname,
                'password': password
            }
        ).first()
        
        return result 