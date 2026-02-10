"""
Database connection utilities for MySQL
Uses mysql-connector-python for database operations
"""

import mysql.connector
from mysql.connector import pooling, Error
import os
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

# Parse DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL', '')

def parse_database_url(url):
    """Parse DATABASE_URL into connection parameters"""
    if not url or url.startswith('sqlite'):
        raise ValueError("MySQL DATABASE_URL is required. Format: mysql://user:password@host/database")
    
    # Remove mysql:// prefix
    url = url.replace('mysql://', '').replace('mysql+pymysql://', '')
    
    # Parse: user:password@host/database
    # Use rfind to get last @ to handle @ in password
    if '@' not in url:
        raise ValueError("Invalid DATABASE_URL format")
    
    last_at = url.rfind('@')
    auth = url[:last_at]
    rest = url[last_at+1:]
    user, password = auth.split(':', 1)
    host_db = rest.split('/')
    host = host_db[0]
    database = host_db[1] if len(host_db) > 1 else 'forum_db'
    
    return {
        'host': host,
        'user': user,
        'password': password,
        'database': database,
        'charset': 'utf8mb4',
        'use_unicode': True,
        'autocommit': False
    }

DB_CONFIG = parse_database_url(DATABASE_URL)


@contextmanager
def get_db_connection():
    """
    Context manager for database connections
    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users")
    """
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        yield connection
        connection.commit()
    except Error as e:
        if connection:
            connection.rollback()
        raise e
    finally:
        if connection and connection.is_connected():
            connection.close()


def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Execute a query and optionally fetch results
    
    Args:
        query: SQL query string
        params: Query parameters (tuple or dict)
        fetch_one: Return single row
        fetch_all: Return all rows
    
    Returns:
        For SELECT: dict or list of dicts
        For INSERT: last inserted ID
        For UPDATE/DELETE: number of affected rows
    """
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                # For INSERT, return the last inserted ID
                return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
        finally:
            cursor.close()


def fetch_one(query, params=None):
    """Execute query and fetch one result"""
    return execute_query(query, params, fetch_one=True)


def fetch_all(query, params=None):
    """Execute query and fetch all results"""
    return execute_query(query, params, fetch_all=True)


def insert(query, params=None):
    """Execute INSERT query and return last inserted ID"""
    return execute_query(query, params)


def update(query, params=None):
    """Execute UPDATE query and return affected rows"""
    return execute_query(query, params)


def delete(query, params=None):
    """Execute DELETE query and return affected rows"""
    return execute_query(query, params)
