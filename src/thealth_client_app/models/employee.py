from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

#This is the employee model for the app.
class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    password: str

class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: str

class EmployeeUpdate(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: str

class EmpoloyeeLogin(BaseModel):
    email: EmailStr
    password: str
