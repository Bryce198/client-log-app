from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID
from typing import Optional

#This is the employee model for the app.
class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    password: str

class EmployeeResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    role: str

class EmployeeUpdate(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    role: str

class EmpoloyeeLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]
