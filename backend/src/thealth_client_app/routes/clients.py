from fastapi import APIRouter, status, HTTPException, Response, Depends
from thealth_client_app.models.client import ClientCreate, Client
from thealth_client_app.database import get_database
from thealth_client_app import oauth2
from ..logic.interaction import log_interaction
from typing import Annotated
from thealth_client_app.models.employee import TokenData
from uuid import UUID

router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)



@router.get("/", status_code=status.HTTP_200_OK)
def get_clients(conn = Depends(get_database), current_user: TokenData = Depends(oauth2.get_current_user)):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT * FROM clients""")

        return cursor.fetchall()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Client)
def add_client(client: ClientCreate, conn = Depends(get_database), current_user: TokenData = Depends(oauth2.get_current_user), current_employee: dict = Depends(oauth2.get_current_user)):
    with conn.cursor() as cursor:
        cursor.execute("""INSERT INTO clients (first_name, last_name, age, date_of_birth, phone_number, email, status, parent_info, employee_id, event, signup_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *""",
        (client.first_name, client.last_name, client.age, client.date_of_birth, client.phone_number, client.email,
        client.status, client.parent_info, current_employee['id'], client.event, client.signup_date))

        new_client = cursor.fetchone()

        log_interaction(cursor, current_employee['id'], new_client['id'], f'Client Created by {current_employee['first_name']}')
    conn.commit()

    return new_client

@router.get("/{client_id}", status_code=status.HTTP_200_OK)
def get_client(client_id: UUID, conn = Depends(get_database), current_user: TokenData = Depends(oauth2.get_current_user)):
    with conn.cursor() as cursor:

        cursor.execute("""SELECT * FROM clients WHERE id = %s""", (client_id,))
        client = cursor.fetchone()

    if client is None:
        raise HTTPException(status_code=404, 
                            detail=f"Client with ID: {client_id} not found")

    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_client(client_id: UUID, conn = Depends(get_database), current_user: TokenData = Depends(oauth2.get_current_user), current_employee: dict = Depends(oauth2.get_current_user)):
    if current_employee['role'] != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are are not authorized to complete this action. Must be an Admin.')
    
    with conn.cursor() as cursor:

        cursor.execute("""DELETE FROM clients WHERE id = %s RETURNING *""", (client_id,))
        client = cursor.fetchone()

        
        conn.commit()

    if client is None:
        raise HTTPException(status_code= 404, 
                            detail=f"Client with ID: {client_id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{client_id}", status_code=status.HTTP_200_OK, response_model=Client)
def update_client(client_id: UUID, client: ClientCreate, conn = Depends(get_database), current_user: TokenData = Depends(oauth2.get_current_user), current_employee = Depends(oauth2.get_current_user)):
    with conn.cursor() as cursor:

        cursor.execute("""UPDATE clients SET first_name = %s, last_name = %s, age = %s, date_of_birth = %s, phone_number = %s, email = %s,
        status = %s, parent_info = %s, event = %s, signup_date = %s WHERE id = %s RETURNING *""",
        (client.first_name, client.last_name, client.age, client.date_of_birth, client.phone_number,
        client.email, client.status, client.parent_info, client.event, client.signup_date, client_id))

        updated_client = cursor.fetchone()

        log_interaction(cursor, current_employee['id'], updated_client['id'], f'Client Updated by {current_employee['first_name']}')
        conn.commit()

    if updated_client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Client with ID: {id} not found")

    return updated_client