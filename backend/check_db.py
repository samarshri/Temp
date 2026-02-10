
import os
import sys
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"DATABASE_URL: {DATABASE_URL}")

if not DATABASE_URL:
    print("No DATABASE_URL found")
    sys.exit(1)
    
try:
    # Manual parsing to be sure
    url = DATABASE_URL.replace('mysql://', '')
    if '@' in url:
        last_at = url.rfind('@')
        auth = url[:last_at]
        rest = url[last_at+1:]
        user, password = auth.split(':', 1)
        host, db = rest.split('/')
        
        print(f"Connecting to {host} with user {user} to db {db}")
        
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )
        
        if conn.is_connected():
            print("Successfully connected to MySQL database")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"Number of users: {count}")
            cursor.close()
            conn.close()
        else:
            print("Failed to connect")
            
except Exception as e:
    print(f"Error connecting to database: {e}")
