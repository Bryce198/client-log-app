
def log_interaction(cursor, employee_id, client_id, interaction_type):
    cursor.execute("""INSERT INTO public.interactions (interaction_type, employee_id, client_id) VALUES (%s, %s, %s)""",
                    (interaction_type, employee_id, client_id))