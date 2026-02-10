
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
# Parse URL (reusing logic)
url = DATABASE_URL.replace('mysql://', '')
if '@' in url:
    last_at = url.rfind('@')
    auth = url[:last_at]
    rest = url[last_at+1:]
    user, password = auth.split(':', 1)
    host, db = rest.split('/')

try:
    conn = mysql.connector.connect(host=host, user=user, password=password, database=db)
    cursor = conn.cursor()
    cursor.execute("DESCRIBE posts")
    columns = [row[0] for row in cursor.fetchall()]
    print(f"Columns in posts table: {columns}")
    
    if 'category' not in columns:
        print("MISSING COLUMN: category")
    else:
        print("Column 'category' exists")
        
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
