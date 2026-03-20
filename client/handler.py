def handle_message(state, message: str):
    if not message:
        return

    print("RECV:", repr(message))

    if message == "NICK":
        state.client.send((state.nickname + "\n").encode())
        return

    if message.startswith("USERS|"):
        parts = message.split("|", 1)
        users_raw = parts[1] if len(parts) > 1 else ""
        user_list = users_raw.split(",") if users_raw else []
        from .ui import update_user_list
        update_user_list(state, user_list)
        return

    if message.startswith("TYPING:"):
        parts = message.split(":", 1)
        user = parts[1] if len(parts) > 1 else ""
        if user and user != state.nickname and state.typing_label:
            state.typing_label.config(text=f"{user} sedang mengetik...")
            state.root.after(1500, lambda: state.typing_label.config(text=""))
        return

    # ===== PRIVATE =====
    if message.startswith("[PM]"):
        try:
            sender = message.split(" ")[1].replace(":", "")
        except:
            return

        if sender == state.nickname:
            return

        if sender not in state.chat_history:
            state.chat_history[sender] = []

        state.chat_history[sender].append(("left", message))

        if state.current_chat == sender:
            from .ui import add_message
            add_message(state, message, "left")

    # ===== GLOBAL =====
    elif ":" in message:
        sender = message.split(":", 1)[0]

        if sender == state.nickname:
            return

        if "GLOBAL" not in state.chat_history:
            state.chat_history["GLOBAL"] = []

        state.chat_history["GLOBAL"].append(("left", message))

        if state.current_chat == "GLOBAL":
            from .ui import add_message
            add_message(state, message, "left")