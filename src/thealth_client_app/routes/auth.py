from fastapi import APIRouter, Depends, status, HTTPException, Response
from thealth_client_app.database import *
from thealth_client_app.models.employee import EmpoloyeeLogin
from thealth_client_app import utils

router = APIRouter(
    prefix='/login',
    tags=['Authentication'])

@router.post("/")
def login_employee(employee_credentials: EmpoloyeeLogin, conn = Depends(get_database)):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT * FROM employees WHERE email = %s""",
                       (employee_credentials.email,))
        employee = cursor.fetchone()

    if employee is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")

    if not utils.verify_pass(employee_credentials.password, employee["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")

    return {"token": "Return Token"}

    