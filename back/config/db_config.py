import psycopg

def get_db_connection():
    northwind = psycopg.connect(
        host='localhost',
        dbname='northwind', 
        user = 'postgres', 
        password = '3081'
    )
    northwind.autocommit = True
    return northwind
