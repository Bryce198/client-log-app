from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from fastapi.params import Body
from datetime import date
from thealth_client_app.models.client import ClientCreate, Client
from thealth_client_app.models.employee import Employee
from thealth_client_app.models.interactions import Interaction
from thealth_client_app.logic.find_client import find_client, find_client_index
from thealth_client_app.logic.delete_client import delete_client
import psycopg
from psycopg import rows
from thealth_client_app.password_user import password, user, dbname
import time

app = FastAPI()

while True:

    try:
        conn = psycopg.connect(host="localhost", 
                           dbname=dbname, 
                           user=user, 
                           password=password,
                           row_factory=rows.dict_row) # pyright: ignore[reportArgumentType]
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as e:
        print("Connection to database failed")
        print(e)
        time.sleep(2)
    
clients = [      Client(id= 1,
                        first_name= "George", 
                        last_name= "Kirk", 
                        age= 21, 
                        date_of_birth= date(2004, 10, 22), 
                        phone_number= "202-454-9940", 
                        email= "George@gmail.com",
                        status= "Registered",
                        created_at= date(2026, 9, 11),
                        created_by= "Bryce",
                        parent_info= "N/A"),

                  Client(id= 2,
                         first_name= "Bobby",
                         last_name= "Smith",
                         age= 25,
                         date_of_birth= date(2000, 4, 11),
                         phone_number= "301-555-2312",
                         email= "BobbySmith7@gmail.com",
                         status= "Registered",
                         created_at= date(2026, 9, 11),
                         created_by= "Bryce",
                         parent_info= "N/A")]

@app.get("/", status_code=status.HTTP_200_OK)
def get_home():
    return {"Message": "Hello Home Page"}


@app.get("/clients", status_code=status.HTTP_200_OK)
def get_clients():
    cursor.execute("""SELECT * FROM clients""")
    clients = cursor.fetchall()
    return {"Clients": clients}


@app.post("/clients", status_code=status.HTTP_201_CREATED)
def add_client(client: ClientCreate):
    cursor.execute("""INSERT INTO clients (first_name, last_name, age, date_of_birth, phone_number, email, status, created_at, created_by, parent_info)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *""", 
    (client.first_name, client.last_name, client.age, client.date_of_birth, client.phone_number, client.email,
     client.status, client.created_at, client.created_by, client.parent_info))

    new_client = cursor.fetchone()
    conn.commit()

    return {"New Client": new_client}

@app.get("/clients/{id}", status_code=status.HTTP_200_OK)
def get_client(client_id: int):
    cursor.execute("""SELECT * FROM clients WHERE id = %s""", (client_id,))
    client = cursor.fetchone()
    if client is None:
        raise HTTPException(status_code= 404, detail= f"Client with ID: {client_id} not found")

    return {"Client Info": client}

@app.delete("/clients/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_client(client_id: int):
    cursor.execute("""DELETE FROM clients WHERE id = %s RETURNING *""", (client_id,))
    client = cursor.fetchone()
    conn.commit()

    if client is None:
        raise HTTPException(status_code= 404, detail=f"Client with ID: {client_id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/clients/{id}", status_code=status.HTTP_200_OK)
def update_client(client_id: int, client: ClientCreate):
    cursor.execute("""UPDATE clients SET first_name = %s, last_name = %s, age = %s, date_of_birth = %s, phone_number = %s, email = %s,
    status = %s, created_at = %s, created_by = %s, parent_info = %s WHERE id = %s RETURNING *""",
    (client.first_name, client.last_name, client.age, client.date_of_birth, client.phone_number,
     client.email, client.status, client.created_at, client.created_by, client.parent_info, client_id))

    updated_client = cursor.fetchone
    conn.commit()

    if updated_client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Client with ID: {id} not found")

    return {"Updated Client": updated_client}