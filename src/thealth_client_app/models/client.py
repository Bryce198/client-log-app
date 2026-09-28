from pydantic import BaseModel, EmailStr
from datetime import date
from uuid import UUID

#This is the client model for my app. it includes all of the
#fields that are required and need to be tracked by our team.
class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    date_of_birth: date
    phone_number: str
    email: EmailStr
    status: str
    created_at: date
    created_by: str
    parent_info: str

class Client(ClientCreate):
    id: int

    