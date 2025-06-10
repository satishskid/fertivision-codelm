#!/usr/bin/env python3
"""
Basic Authentication Module for FertiVision-CodeLM System
Simple session-based authentication for local deployment
"""

from flask import session, request, redirect, url_for, render_template_string, flash
from functools import wraps
import hashlib
import secrets
import time
from config import Config

class BasicAuth:
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the authentication system with Flask app"""
        app.secret_key = secrets.token_hex(16)  # Generate random secret key
        
        # Add login route
        @app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form.get('username', '').strip()
                password = request.form.get('password', '').strip()
                
                if self.validate_credentials(username, password):
                    session['authenticated'] = True
                    session['username'] = username
                    session['login_time'] = time.time()
                    flash('Login successful!', 'success')
                    
                    # Redirect to originally requested page or home
                    next_page = request.args.get('next')
                    if next_page:
                        return redirect(next_page)
                    return redirect(url_for('index'))
                else:
                    flash('Invalid credentials. Please try again.', 'error')
            
            return render_template_string(self.get_login_template())
        
        # Add logout route
        @app.route('/logout')
        def logout():
            session.clear()
            flash('You have been logged out.', 'info')
            return redirect(url_for('login'))
    
    def validate_credentials(self, username, password):
        """Validate username and password"""
        # Simple validation against config values
        return (username == Config.DEFAULT_USERNAME and 
                password == Config.DEFAULT_PASSWORD)
    
    def is_authenticated(self):
        """Check if current session is authenticated"""
        if not Config.ENABLE_AUTH:
            return True  # Skip auth if disabled
        
        if 'authenticated' not in session:
            return False
        
        # Check session timeout
        login_time = session.get('login_time', 0)
        if time.time() - login_time > Config.SESSION_TIMEOUT:
            session.clear()
            return False
        
        return session.get('authenticated', False)
    
    def require_auth(self, f):
        """Decorator to require authentication for routes"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not self.is_authenticated():
                return redirect(url_for('login', next=request.url))
            return f(*args, **kwargs)
        return decorated_function
    
    def get_login_template(self):
        """Return HTML template for login page"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔬 FertiVision Login</title>
    <style>
        :root {
            --primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            --glass-bg: rgba(255, 255, 255, 0.95);
            --shadow-heavy: 0 8px 25px rgba(0, 0, 0, 0.15);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f0f9ff 0%, #e0e7ff 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .login-container {
            background: var(--glass-bg);
            padding: 3rem;
            border-radius: 20px;
            box-shadow: var(--shadow-heavy);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            width: 400px;
            max-width: 90vw;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .login-header h1 {
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .login-header p {
            color: #6b7280;
            font-size: 0.9rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: #374151;
            font-weight: 500;
        }
        
        .form-group input {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
            background: white;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        
        .login-btn {
            width: 100%;
            padding: 0.75rem 1.5rem;
            background: var(--primary-gradient);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
        }
        
        .alert {
            padding: 0.75rem 1rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            font-size: 0.9rem;
        }
        
        .alert-error {
            background-color: #fef2f2;
            color: #dc2626;
            border: 1px solid #fecaca;
        }
        
        .alert-success {
            background-color: #f0fdf4;
            color: #16a34a;
            border: 1px solid #bbf7d0;
        }
        
        .alert-info {
            background-color: #eff6ff;
            color: #2563eb;
            border: 1px solid #bfdbfe;
        }
        
        .default-credentials {
            margin-top: 2rem;
            padding: 1rem;
            background: #fef3c7;
            border-radius: 8px;
            border: 1px solid #f59e0b;
            text-align: center;
            font-size: 0.85rem;
        }
        
        .default-credentials h4 {
            color: #92400e;
            margin-bottom: 0.5rem;
        }
        
        .default-credentials p {
            color: #78350f;
            margin: 0.25rem 0;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>🔬 FertiVision</h1>
            <p>AI-Enhanced Reproductive Classification System</p>
        </div>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            <div class="form-group">
                <label for="username">👤 Username</label>
                <input type="text" id="username" name="username" required autocomplete="username">
            </div>
            
            <div class="form-group">
                <label for="password">🔒 Password</label>
                <input type="password" id="password" name="password" required autocomplete="current-password">
            </div>
            
            <button type="submit" class="login-btn">🚀 Login</button>
        </form>
        
        <div class="default-credentials">
            <h4>📋 Default Credentials</h4>
            <p><strong>Username:</strong> doctor</p>
            <p><strong>Password:</strong> fertility2025</p>
            <p><em>Change these in config.py for production use</em></p>
        </div>
    </div>
</body>
</html>
        '''

# Global auth instance
auth = BasicAuth()
