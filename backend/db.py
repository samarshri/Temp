"""
Database connection utilities for MySQL (with SQLite fallback)
Uses mysql-connector-python for MySQL and sqlite3 for local/fallback
"""

import os
import sqlite3
from contextlib import contextmanager
from dotenv import load_dotenv

# Try importing mysql.connector, but don't fail if not present (for lightweight envs)
try:
    import mysql.connector
    from mysql.connector import pooling, Error
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

load_dotenv()

# Parse DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL', '')
USE_SQLITE = False
DB_CONFIG = {}

# Check if we should use SQLite
if not DATABASE_URL or DATABASE_URL.startswith('sqlite'):
    USE_SQLITE = True
    DB_NAME = 'forum.db'
    if DATABASE_URL.startswith('sqlite:///'):
        DB_NAME = DATABASE_URL.replace('sqlite:///', '')
    print(f"⚠️ Using SQLite database: {DB_NAME}")
else:
    # Parse MySQL URL
    if not MYSQL_AVAILABLE:
        raise ImportError("mysql-connector-python is required for MySQL but not installed.")
        
    try:
        url = DATABASE_URL.replace('mysql://', '').replace('mysql+pymysql://', '')
        if '@' not in url:
            raise ValueError("Invalid DATABASE_URL format")
        
        last_at = url.rfind('@')
        auth = url[:last_at]
        rest = url[last_at+1:]
        user, password = auth.split(':', 1)
        host_db = rest.split('/')
        host = host_db[0]
        database = host_db[1] if len(host_db) > 1 else 'forum_db'
        
        DB_CONFIG = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'use_unicode': True,
            'autocommit': False
        }
    except Exception as e:
        print(f"Error parsing DATABASE_URL: {e}")
        # Fallback to local SQLite if parsing fails
        USE_SQLITE = True
        DB_NAME = 'forum.db'
        print(f"⚠️ Fallback to SQLite database: {DB_NAME}")

def init_sqlite_db():
    """Initialize SQLite database with schema if needed"""
    if not os.path.exists(DB_NAME):
        print("Initializing new SQLite database...")
        conn = sqlite3.connect(DB_NAME)
        script_path = os.path.join(os.path.dirname(__file__), 'schema_sqlite.sql')
        if os.path.exists(script_path):
            with open(script_path, 'r') as f:
                conn.executescript(f.read())
            print("Schema applied.")
        else:
            print("⚠️ schema_sqlite.sql not found!")
        conn.close()

if USE_SQLITE:
    init_sqlite_db()

@contextmanager
def get_db_connection():
    """Context manager for database connections (MySQL or SQLite)"""
    if USE_SQLITE:
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        
        # Helper for dict rows
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
            
        conn.row_factory = dict_factory
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    else:
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
    Handles both MySQL (%s) and SQLite (?) syntax
    """
    params = params or ()
    
    # Convert MySQL syntax (%s) to SQLite syntax (?) if using SQLite
    if USE_SQLITE:
        query = query.replace('%s', '?')
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # For MySQL, we request dictionary cursor in the context manager usually,
        # but here we unify.
        # SQLite uses row_factory, MySQL needs dictionary=True
        
        if not USE_SQLITE and hasattr(conn, 'cursor'):
             cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, params)
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                # For INSERT, return last inserted ID
                if query.strip().upper().startswith('INSERT'):
                    return cursor.lastrowid
                # For UPDATE/DELETE, return rowcount
                return cursor.rowcount
        finally:
            cursor.close()


def fetch_one(query, params=None):
    return execute_query(query, params, fetch_one=True)

def fetch_all(query, params=None):
    return execute_query(query, params, fetch_all=True)

def insert(query, params=None):
    return execute_query(query, params)

def update(query, params=None):
    return execute_query(query, params)

def delete(query, params=None):
    return execute_query(query, params)
