from flask import Flask, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection parameters from environment variables
DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
DB_PORT = os.environ.get('POSTGRES_PORT', '5432')
DB_NAME = os.environ.get('POSTGRES_DB', 'flaskapp')
DB_USER = os.environ.get('POSTGRES_USER', 'postgres')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'password')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    conn.autocommit = True
    return conn

# Initialize the database if needed
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create a test table if it doesn't exist
    cur.execute('''
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Insert test data if table is empty
    cur.execute("SELECT COUNT(*) FROM test_table")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO test_table (name) VALUES ('Test Item 1'), ('Test Item 2')")
    
    cur.close()
    conn.close()

@app.route('/')
def index():
    return jsonify({
        'message': 'Flask application running successfully',
        'database_connection': 'Connected to PostgreSQL'
    })

@app.route('/items')
def get_items():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM test_table")
        items = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize the database on startup
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)