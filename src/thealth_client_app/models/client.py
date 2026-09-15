from pydantic import BaseModel
from datetime import date

class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    date_of_birth: date
    phone_number: str
    email: str
    status: str
    created_at: date
    created_by: str
    parent_info: str

class Client(ClientCreate):
    id: int

    