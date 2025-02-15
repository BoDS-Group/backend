import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection settings
DATABASE_URL = "postgresql://username:password@localhost:5432/mydatabase"

def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()