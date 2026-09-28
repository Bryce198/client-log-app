from fastapi import APIRouter, status, HTTPException, Response, Depends
from thealth_client_app.models.client import ClientCreate, Client
from thealth_client_app.database import *

router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)



@router.get("/", status_code=status.HTTP_200_OK)
def get_clients(conn = Depends(get_database)):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT * FROM clients""")

    return cursor.fetchall()


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_client(client: ClientCreate, conn = Depends(get_database)):
    with conn.cursor() as cursor:
        cursor.execute("""INSERT INTO clients (first_name, last_name, age, date_of_birth, phone_number, email, status, created_at, created_by, parent_info)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *""", 
        (client.first_name, client.last_name, client.age, client.date_of_birth, client.phone_number, client.email,
        client.status, client.created_at, client.created_by, client.parent_info))

    new_client = cursor.fetchone()
    conn.commit()

    return new_client

@router.get("/{client_id}", status_code=status.HTTP_200_OK)
def get_client(client_id: int, conn = Depends(get_database)):
    with conn.cursor() as cursor:

        cursor.execute("""SELECT * FROM clients WHERE id = %s""", (client_id,))
        client = cursor.fetchone()

    if client is None:
        raise HTTPException(status_code= 404, detail= f"Client with ID: {client_id} not found")

    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_client(client_id: int, conn = Depends(get_database)):
    with conn.cursor() as cursor:

        cursor.execute("""DELETE FROM clients WHERE id = %s RETURNING *""", (client_id,))
        client = cursor.fetchone()
        conn.commit()

    if client is None:
        raise HTTPException(status_code= 404, detail=f"Client with ID: {client_id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{client_id}", status_code=status.HTTP_200_OK)
def update_client(client_id: int, client: ClientCreate, conn = Depends(get_database)):
    with conn.cursor() as cursor:

        cursor.execute("""UPDATE clients SET first_name = %s, last_name = %s, age = %s, date_of_birth = %s, phone_number = %s, email = %s,
        status = %s, created_at = %s, created_by = %s, parent_info = %s WHERE id = %s RETURNING *""",
        (client.first_name, client.last_name, client.age, client.date_of_birth, client.phone_number,
        client.email, client.status, client.created_at, client.created_by, client.parent_info, client_id))

        updated_client = cursor.fetchone
        conn.commit()

    if updated_client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Client with ID: {id} not found")

    return updated_client