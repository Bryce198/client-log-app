import psycopg
from psycopg import rows
import os
from dotenv import load_dotenv

load_dotenv()

def get_database():
    conn = psycopg.connect(host=os.getenv("DB_HOST"),
                           dbname=os.getenv("DB_NAME"), 
                           user=os.getenv("DB_USER"), 
                           password=os.getenv("DB_PASSWORD"),
                           row_factory=rows.dict_row) # pyright: ignore[reportArgumentType]

    try:
        yield conn
    finally:
        conn.close
