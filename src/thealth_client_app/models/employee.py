from pydantic import BaseModel, EmailStr
from datetime import datetime

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
    first_name: str
    last_name: str
    email: EmailStr
    role: str

