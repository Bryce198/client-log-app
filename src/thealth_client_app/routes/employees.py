from thealth_client_app.models.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from fastapi import APIRouter, status, HTTPException, Response, Depends
from thealth_client_app import utils
from thealth_client_app.database import *

router = APIRouter(
    prefix="/employees",
    tags=["employees"]
)




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, conn = Depends(get_database)):
    pass_hash = utils.hash_pass(employee.password) 
    employee.password = pass_hash

    with conn.cursor() as cursor:

        cursor.execute("""INSERT INTO employees (first_name, last_name, email, role, password) VALUES 
        (%s, %s, %s, %s, %s) RETURNING *""",
        (employee.first_name, employee.last_name, employee.email, employee.role, employee.password))

        created_employee = cursor.fetchone()
        conn.commit()

    if created_employee is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Employee could not be created.")

    return created_employee

@router.get("/{employee_id}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse)
def show_employee(employee_id: int, conn = Depends(get_database)):
    with conn.cursor() as cursor:

        cursor.execute("""SELECT * FROM employees WHERE id = %s""", (employee_id,))
        employee = cursor.fetchone()

    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with the ID: {employee_id} was not found.")

    return employee

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[EmployeeResponse])
def show_employees(conn = Depends(get_database)):
    with conn.cursor() as cursor:

        cursor.execute("""SELECT id, first_name, last_name, email, role FROM employees""")
        employees = cursor.fetchall()

    if employees is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no employees yet")
    
    return employees

@router.put("/{employee_id}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeUpdate, conn = Depends(get_database)):
    with conn.cursor() as cursor:

        cursor.execute("""UPDATE employees SET first_name = %s, last_name = %s, email = %s, role = %s WHERE id = %s RETURNING *""", 
                   (employee.first_name, employee.last_name, employee.email, employee.role, employee_id))

        updated_employee = cursor.fetchone()
        conn.commit()

    if updated_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error, employee with ID: {employee_id} was not found.")

    return updated_employee

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, conn = Depends(get_database)):
    with conn.cursor() as cursor:

        cursor.execute("""DELETE FROM employees WHERE id = %s RETURNING *""", 
                   (employee_id,))
        employee = cursor.fetchone()

    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error, employee with ID: {employee_id} was not found.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)