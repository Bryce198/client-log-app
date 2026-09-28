import psycopg
from psycopg import rows
from thealth_client_app.password_user import *

def get_database():
    conn = psycopg.connect(host="localhost", 
                               dbname=dbname, 
                               user=user, 
                               password=password,
                               row_factory=rows.dict_row) # pyright: ignore[reportArgumentType]

    try:
        yield conn
    finally:
        conn.close
