from thealth_client_app.models.client import Client

def find_client(id: int, clients: list[Client]):
    for client in clients:
        if client.id == id:
            return client
    return None

def find_client_index(id: int, clients: list[Client]):
    for i in range(len(clients)):
        if clients[i].id == id:
            return i
    return None



