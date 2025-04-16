import psycopg

def get_db_connection():
    northwind = psycopg.connect(
        host='localhost',
        dbname='postgres', 
        user = 'postgres', 
        password = 'root'
    )
    northwind.autocommit = True
    return northwind
