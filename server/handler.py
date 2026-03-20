from .state import clients
from .utils import send, broadcast, send_user_list

def handle(client, nickname):
    buffer = ""

    while True:
        try:
            data = client.recv(1024).decode()
            if not data:
                break

            buffer += data

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                message = message.strip()

                if not message:
                    continue

                if message.startswith("GLOBAL|"):
                    _, sender, msg = message.split("|", 2)
                    broadcast(f"{sender}: {msg}", sender_client=client)

                elif message.startswith("PRIVATE|"):
                    _, sender, target, msg = message.split("|", 3)
                    if target in clients:
                        send(clients[target], f"[PM] {sender}: {msg}")

                elif message.startswith("TYPING|"):
                    _, sender, target = message.split("|")

                    if target == "GLOBAL":
                        broadcast(f"TYPING:{sender}", sender_client=client)
                    elif target in clients:
                        send(clients[target], f"TYPING:{sender}")

        except:
            break

    print(f"{nickname} disconnected")

    if nickname in clients:
        del clients[nickname]

    send_user_list()
    client.close()