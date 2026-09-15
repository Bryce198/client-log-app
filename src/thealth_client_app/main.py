from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel, EmailStr
from fastapi.params import Body
from datetime import date
from thealth_client_app.models.client import ClientCreate, Client
from thealth_client_app.models.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from thealth_client_app.models.interactions import Interaction
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
    

@app.get("/", status_code=status.HTTP_200_OK)
def get_home():
    return {"Message": "Hello Home Page"}


@app.get("/clients", status_code=status.HTTP_200_OK)
def get_clients():
    cursor.execute("""SELECT * FROM clients""")
    clients = cursor.fetchall()
    return clients


@app.post("/clients", status_code=status.HTTP_201_CREATED)
def add_client(client: ClientCreate):
    cursor.execute("""INSERT INTO clients (first_name, last_name, age, date_of_birth, phone_number, email, status, created_at, created_by, parent_info)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *""", 
    (client.first_name, client.last_name, client.age, client.date_of_birth, client.phone_number, client.email,
     client.status, client.created_at, client.created_by, client.parent_info))

    new_client = cursor.fetchone()
    conn.commit()

    return new_client

@app.get("/clients/{client_id}", status_code=status.HTTP_200_OK)
def get_client(client_id: int):
    cursor.execute("""SELECT * FROM clients WHERE id = %s""", (client_id,))
    client = cursor.fetchone()

    if client is None:
        raise HTTPException(status_code= 404, detail= f"Client with ID: {client_id} not found")

    return client

@app.delete("/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_client(client_id: int):
    cursor.execute("""DELETE FROM clients WHERE id = %s RETURNING *""", (client_id,))
    client = cursor.fetchone()
    conn.commit()

    if client is None:
        raise HTTPException(status_code= 404, detail=f"Client with ID: {client_id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/clients/{client_id}", status_code=status.HTTP_200_OK)
def update_client(client_id: int, client: ClientCreate):
    cursor.execute("""UPDATE clients SET first_name = %s, last_name = %s, age = %s, date_of_birth = %s, phone_number = %s, email = %s,
    status = %s, created_at = %s, created_by = %s, parent_info = %s WHERE id = %s RETURNING *""",
    (client.first_name, client.last_name, client.age, client.date_of_birth, client.phone_number,
     client.email, client.status, client.created_at, client.created_by, client.parent_info, client_id))

    updated_client = cursor.fetchone
    conn.commit()

    if updated_client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Client with ID: {id} not found")

    return updated_client

@app.post("/employees", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate):
    cursor.execute("""INSERT INTO employees (first_name, last_name, email, role, password) VALUES 
    (%s, %s, %s, %s, %s) RETURNING *""",
    (employee.first_name, employee.last_name, employee.email, employee.role, employee.password))

    created_employee = cursor.fetchone()
    conn.commit()

    if created_employee is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Employee could not be created.")

    return created_employee

@app.get("/employees/{employee_id}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse)
def show_employee(employee_id: int):
    cursor.execute("""SELECT * FROM employees WHERE id = %s""", (employee_id,))
    employee = cursor.fetchone()

    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with the ID: {employee_id} was not found.")

    return employee

@app.get("/employees", status_code=status.HTTP_200_OK, response_model=list[EmployeeResponse])
def show_employees():
    cursor.execute("""SELECT id, first_name, last_name, email, role FROM employees""")
    employees = cursor.fetchall()

    if employees is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no employees yet")
    
    return employees

@app.put("/employees/{employee_id}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeUpdate):
    cursor.execute("""UPDATE employees SET first_name = %s, last_name = %s, email = %s, role = %s WHERE id = %s RETURNING *""", 
                   (employee.first_name, employee.last_name, employee.email, employee.role, employee_id))

    updated_employee = cursor.fetchone()
    conn.commit()

    if updated_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error, employee with ID: {employee_id} was not found.")

    return updated_employee

@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int):
    cursor.execute("""DELETE FROM employees WHERE id = %s RETURNING *""", 
                   (employee_id,))
    employee = cursor.fetchone()

    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error, employee with ID: {employee_id} was not found.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)