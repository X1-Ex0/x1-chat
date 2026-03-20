from .handler import handle_message

def receive(state):
    buffer = ""

    while True:
        try:
            data = state.client.recv(1024).decode()
            if not data:
                break

            buffer += data

            while "\n" in buffer:
                msg, buffer = buffer.split("\n", 1)
                msg = msg.strip()
                if msg:
                    handle_message(state, msg)

        except Exception as e:
            print("Receive error:", e)
            break


def send_message(state, event=None):
    if state.entry is None:
        return

    msg = state.entry.get().strip()
    if not msg:
        return

    try:
        if state.current_chat == "GLOBAL":
            state.client.send((f"GLOBAL|{state.nickname}|{msg}\n").encode())
        else:
            state.client.send((f"PRIVATE|{state.nickname}|{state.current_chat}|{msg}\n").encode())

        full_msg = f"{state.nickname}: {msg}"

        if state.current_chat not in state.chat_history:
            state.chat_history[state.current_chat] = []

        state.chat_history[state.current_chat].append(("right", full_msg))

        from .ui import add_message
        add_message(state, full_msg, "right")

        state.entry.delete(0, "end")

    except Exception as e:
        print("Send error:", e)
        if state.status_label:
            state.status_label.config(text="Gagal mengirim pesan")