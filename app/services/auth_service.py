#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import modules #
#----------------#

import time
from sqlalchemy.orm import Session
from typing import Dict, Optional, Tuple

# Import project modules #
#------------------------#

from app.models.staff_model import Staff
from app.utils.password_handler import PasswordHandler
from app.utils.time_formatters import _format_arbitrary_dt

# Define classes and methods #
#----------------------------#

class AuthService:
    """
    Authentication service for staff members.
    Implements rate limiting and credential validation.
    """
    def __init__(self):
        self.password_handler = PasswordHandler()
        self.login_attempts: Dict[str, list] = {}  # IP -> list of attempt timestamps
        self.block_duration_mins = 5
        self.max_attempts = 3


    def _is_blocked(self, ip_address: str) -> Tuple[bool, Optional[float]]:
        """
        Check if an IP address is blocked due to too many failed attempts.
        
        Parameters
        ----------
        ip_address : str
            The IP address to check
            
        Returns
        -------
            Tuple[bool, Optional[float]]: (is_blocked, remaining_block_time)
        """
        if ip_address not in self.login_attempts:
            return False, None
            
        attempts = self.login_attempts[ip_address]
        now = time.time()
        
        # Remove attempts older than block_duration_mins
        attempts = [t for t in attempts if now - t < self.block_duration_mins * 60]
        self.login_attempts[ip_address] = attempts
        
        if len(attempts) >= self.max_attempts:
            # Calculate remaining block time
            oldest_attempt = min(attempts)
            block_end = oldest_attempt + (self.block_duration_mins * 60)
            remaining = block_end - now
            
            if remaining > 0:
                return True, remaining
            else:
                # Reset attempts if block time has expired
                self.login_attempts[ip_address] = []
                return False, None
                
        return False, None

    def _record_attempt(self, ip_address: str, success: bool):
        """
        Record a login attempt.
        
        Parameters
        ----------
        ip_address: str
            The IP address of the attempt
        success: bool
            Whether the attempt was successful
        """
        if success:
            # Reset attempts on successful login
            self.login_attempts[ip_address] = []
        else:
            if ip_address not in self.login_attempts:
                self.login_attempts[ip_address] = []
            self.login_attempts[ip_address].append(time.time())

    def authenticate(self, session: Session, username: str, usersurname: str, 
                    password: str, ip_address: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Authenticate a staff member.
        
        Parameters
        ----------
        session: SQLAlchemy session
            The SQLAlchemy session
        username: str
            Staff member's username
        usersurname: str
            Staff member's surname
        password: str
            Staff member's password
        ip_address: str
            IP address of the login attempt
            
        Returns
        -------
        Tuple[bool, Optional[str], Optional[str]]: 
            A tuple containing:
                - success: bool
                - role: Optional[str]
                - error_message: Optional[str]
        """
        # Check if IP is blocked
        is_blocked, remaining_time = self._is_blocked(ip_address)
        if is_blocked:
            return False, None, f"Too many failed attempts. Please try again in {_format_arbitrary_dt(remaining_time, 0)}."

        # Get staff member
        staff = Staff.get_staff_by_credentials(session, username, usersurname)
        
        if not staff:
            self._record_attempt(ip_address, False)
            return False, None, "Invalid credentials"
            
        # Verify password
        if not self.password_handler.verify_password(staff.password, password):
            self._record_attempt(ip_address, False)
            return False, None, "Invalid credentials"
            
        # Successful login
        self._record_attempt(ip_address, True)
        return True, staff.role, None 