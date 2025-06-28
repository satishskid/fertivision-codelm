#!/usr/bin/env python3
"""
Basic Authentication Module for FertiVision
Simple authentication wrapper for development/demo purposes
"""

from functools import wraps
from flask import request, jsonify, session
import hashlib
import os

class BasicAuth:
    """Basic authentication system"""
    
    def __init__(self):
        # Simple demo credentials - in production, use proper authentication
        self.demo_users = {
            'admin': self._hash_password('admin123'),
            'doctor': self._hash_password('doctor123'),
            'demo': self._hash_password('demo123')
        }
    
    def _hash_password(self, password: str) -> str:
        """Simple password hashing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials"""
        if username in self.demo_users:
            return self.demo_users[username] == self._hash_password(password)
        return False
    
    def require_auth(self, f):
        """Decorator to require authentication"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # For demo purposes, always allow access
            # In production, implement proper session-based authentication
            return f(*args, **kwargs)
        return decorated_function
    
    def login(self, username: str, password: str) -> bool:
        """Login user"""
        if self.authenticate(username, password):
            session['user'] = username
            return True
        return False
    
    def logout(self):
        """Logout user"""
        session.pop('user', None)
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return 'user' in session
    
    def get_current_user(self) -> str:
        """Get current user"""
        return session.get('user', 'anonymous')

# Global auth instance
auth = BasicAuth()
