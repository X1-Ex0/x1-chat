from .state import clients

def send(client, message):
    try:
        if message.strip():
            client.send((message + "\n").encode())
    except:
        pass


def broadcast(message, sender_client=None):
    for client in clients.values():
        if client != sender_client:
            send(client, message)


def send_user_list():
    user_list = ",".join(clients.keys())
    print("USERS:", user_list)

    for client in clients.values():
        send(client, f"USERS|{user_list}")