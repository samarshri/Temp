"""
Database initialization script
Creates tables and default admin user
"""

import mysql.connector
from werkzeug.security import generate_password_hash
from db import DB_CONFIG, get_db_connection
import os

def init_database():
    """Initialize database with schema and default data"""
    
    print("Initializing database...")
    
    # Read schema file
    schema_path = os.path.join(os.path.dirname(__file__), 'schema_v2.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    # Connect and execute schema
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Execute each statement separately
            statements = schema_sql.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)
            
            print("[OK] Tables created successfully")
            
            # Create default admin user
            admin_password = generate_password_hash('admin123')
            insert_admin = """
            INSERT INTO users (username, name, email, password_hash, role, branch, year, is_moderator, reputation_points)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_admin, (
                'admin',
                'Admin User',
                'admin@forum.com',
                admin_password,
                'admin',
                'Administration',
                'Faculty',
                True,
                1000
            ))
            
            cursor.close()
            print("[OK] Default admin created: admin@forum.com / admin123")
            
        print("\n" + "="*60)
        print("Database initialization complete!")
        print("="*60)
        
    except Exception as e:
        print(f"[ERROR] Error initializing database: {e}")
        raise


if __name__ == "__main__":
    confirm = input("This will DROP all existing tables and data. Continue? (yes/no): ")
    if confirm.lower() == 'yes':
        init_database()
    else:
        print("Operation cancelled.")
