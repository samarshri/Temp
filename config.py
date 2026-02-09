import os
from datetime import timedelta

class Config:
    """Application configuration"""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Use PostgreSQL in production (Render provides DATABASE_URL)
    # Use SQLite locally for development
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        # Render uses postgres:// but SQLAlchemy needs postgresql://
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url or \
        f'sqlite:///{os.path.join(BASE_DIR, "forum.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # AI Configuration
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'mock')  # 'mock', 'openai', 'gemini'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    AI_MODEL = os.environ.get('AI_MODEL', 'gpt-3.5-turbo')
    
    # Pagination
    POSTS_PER_PAGE = 20
    COMMENTS_PER_PAGE = 50
