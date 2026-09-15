from pydantic import BaseModel
from datetime import date

class Interaction(BaseModel):
    id: int
    interaction_type: str
    notes: str
    created_at: date