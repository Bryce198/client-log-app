from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from thealth_client_app.database import *
from thealth_client_app.models.employee import Token
from thealth_client_app import utils
from thealth_client_app import oauth2
from typing import Annotated

router = APIRouter(
    prefix='/login',
    tags=['authentication'])

@router.post("/", response_model=Token)
def login_employee(employee_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], conn = Depends(get_database)):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT id, first_name, last_name, email, role, password FROM employees WHERE email = %s""",
                       (employee_credentials.username,))
        employee = cursor.fetchone()

    if employee is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credentials")

    if not utils.verify_pass(employee_credentials.password, employee["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credentials")

    access_token = oauth2.create_token(data= {"sub": str(employee["id"])})

    return {"access_token": access_token, "token_type": "bearer"}

    