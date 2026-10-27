from fastapi import status, APIRouter, Response, HTTPException, Depends
from .. import database, oauth2
from ..models.interactions import Interaction

def log_interaction(cursor, employee_id, client_id, interaction_type):
    cursor.execute("""INSERT INTO public.interactions (interaction_type, employee_id, client_id) VALUES (%s, %s, %s)""",
                    (interaction_type, employee_id, client_id))