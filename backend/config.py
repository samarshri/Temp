import os
from datetime import timedelta

class Config:
    """Application configuration for MySQL-based forum"""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # AI Configuration
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'mock')  # 'mock', 'openai', 'gemini'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    AI_MODEL = os.environ.get('AI_MODEL', 'gpt-3.5-turbo')
    
    # Pagination
    POSTS_PER_PAGE = 20
    COMMENTS_PER_PAGE = 50
