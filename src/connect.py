import psycopg
from config import HOST, DB_NAME, USER, PASSWORD

def get_db_connection():
    return psycopg.connect(
        host=HOST, 
        dbname=DB_NAME, 
        user=USER, 
        password=PASSWORD
    )