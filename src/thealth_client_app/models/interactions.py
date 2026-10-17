from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class Interaction(BaseModel):
    employee_id: UUID
    client_id: UUID
    created_at: datetime