from thealth_client_app.models.client import Client
from datetime import date

def delete_client(id: int, clients: list[Client]):
    for i in range(len(clients)):
        if clients[i].id == id:
            clients.pop(i)
            return clients[i]

    return None

