import socket
import threading
from .state import clients
from .utils import send, send_user_list
from .handler import handle

HOST = '0.0.0.0'
PORT = 5556

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()


def receive():
    print(f"🚀 Server running on port {PORT}")

    while True:
        client, address = server.accept()

        try:
            send(client, "NICK")

            nickname = client.recv(1024).decode().strip()

            if not nickname:
                client.close()
                continue

            if nickname in clients:
                send(client, "NAME_USED")
                client.close()
                continue

            clients[nickname] = client

            print(f"✅ {nickname} connected from {address}")

            send_user_list()

            thread = threading.Thread(target=handle, args=(client, nickname))
            thread.start()

        except:
            client.close()