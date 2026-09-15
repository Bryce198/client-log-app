from pydantic import BaseModel
from datetime import datetime

class Interaction(BaseModel):
    id: int
    employee_id: int
    client_id: int
    interaction_type: str
    notes: str
    created_at: datetime