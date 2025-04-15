import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postegres",
        user="postegres",
        password="root"
    )
    conn.autocommit = True
    return conn
