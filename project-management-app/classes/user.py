from classes.client import Client


class User:

    all_clients = []

    def __init__(self, name: str):
        self.name = name
        self.clients = []

    def create_client(self, name):
        client = Client(name)
        self.clients.append(client)
        self.all_clients.append(client)
        return client

