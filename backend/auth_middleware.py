"""
JWT Authentication Middleware
Provides token generation and validation for API authentication
"""

import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from models.user import User

# Secret key for JWT
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24 * 7  # 7 days


def generate_token(user_id):
    """Generate JWT token for a user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_token(token):
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


def token_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                # Expected format: "Bearer <token>"
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Authentication token required'}), 401
        
        # Decode token
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get user from database
        user = User.get_by_id(payload['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 401
        
        # Attach user_id to request for simpler access
        request.user_id = user.id
        request.current_user = user
        
        # Pass user to route function
        return f(current_user=user, *args, **kwargs)
    
    return decorated


def require_auth(f):
    """Alternative decorator - attaches user info to request object"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Authentication token required'}), 401
        
        # Decode token
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get user from database
        user = User.get_by_id(payload['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 401
        
        # Attach user info to request
        request.user_id = user.id
        request.current_user = user
        
        # Call the route function
        return f(*args, **kwargs)
    
    return decorated


def get_current_user():
    """Get current user from request token (optional)"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    try:
        token = auth_header.split(' ')[1]
        payload = decode_token(token)
        if payload:
            return User.get_by_id(payload['user_id'])
    except:
        pass
    
    return None
