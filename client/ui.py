import tkinter as tk
from datetime import datetime
from .network import send_message

def add_message(state, text, side):
    if state.chat_frame is None or state.canvas is None:
        return

    text = text.strip()
    if not text:
        return

    time_now = datetime.now().strftime("%H:%M")

    container = tk.Frame(state.chat_frame, bg="#e5ddd5")
    container.pack(fill="x", expand=True, pady=2)

    row = tk.Frame(container, bg="#e5ddd5")
    row.pack(fill="x", expand=True)

    color = "#DCF8C6" if side == "right" else "#FFFFFF"

    if side == "right":
        tk.Frame(row, bg="#e5ddd5").pack(side="left", fill="x", expand=True)

    bubble = tk.Frame(row, bg=color, padx=10, pady=6)

    tk.Label(bubble, text=text, bg=color, justify="left", wraplength=280).pack(anchor="w")

    tk.Label(bubble, text=time_now, bg=color, font=("Arial", 7), fg="gray").pack(anchor="e")

    bubble.pack(side="left", padx=10)

    if side == "left":
        tk.Frame(row, bg="#e5ddd5").pack(side="right", fill="x", expand=True)

    state.canvas.update_idletasks()
    state.canvas.yview_moveto(1.0)


def update_user_list(state, user_list):
    for widget in state.user_frame.winfo_children():
        widget.destroy()

    def make_btn(user):
        return tk.Button(
            state.user_frame,
            text=user,
            bg="#075E54" if state.current_chat == user else "#2f3136",
            fg="white",
            relief="flat",
            anchor="w"
        )

    all_btn = make_btn("GLOBAL")
    all_btn.config(command=lambda: select_user(state, "GLOBAL", all_btn))
    all_btn.pack(fill=tk.X, padx=2, pady=1)

    for user in user_list:
        if user and user != state.nickname:
            btn = make_btn(user)
            btn.config(command=lambda u=user, b=btn: select_user(state, u, b))
            btn.pack(fill=tk.X, padx=2, pady=1)


def select_user(state, user, button):
    state.current_chat = user

    if state.selected_button and state.selected_button.winfo_exists():
        state.selected_button.config(bg="#2f3136")

    button.config(bg="#075E54")
    state.selected_button = button

    if state.chat_target_label:
        state.chat_target_label.config(
            text="GLOBAL CHAT" if user == "GLOBAL" else f"Chat dengan {user}"
        )

        for widget in state.chat_frame.winfo_children():
            widget.destroy()

        if user in state.chat_history:
            for side, msg in state.chat_history[user]:
                add_message(state, msg, side)


def build_ui(state):
    root = state.root

    main = tk.Frame(root)
    main.pack(fill=tk.BOTH, expand=True)

    sidebar = tk.Frame(main, width=140, bg="#2f3136")
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="Users", bg="#2f3136", fg="white").pack()

    state.user_frame = tk.Frame(sidebar, bg="#2f3136")
    state.user_frame.pack(fill=tk.BOTH, expand=True)

    chat_area = tk.Frame(main, bg="#e5ddd5")
    chat_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    header = tk.Frame(chat_area, bg="#075E54", height=42)
    header.pack(fill=tk.X)

    state.chat_target_label = tk.Label(header, text="GLOBAL CHAT", bg="#075E54", fg="white")
    state.chat_target_label.pack()

    state.canvas = tk.Canvas(chat_area, bg="#e5ddd5")
    state.canvas.pack(fill=tk.BOTH, expand=True)

    state.chat_frame = tk.Frame(state.canvas, bg="#e5ddd5")
    state.canvas.create_window((0, 0), window=state.chat_frame, anchor="nw")

    state.typing_label = tk.Label(chat_area, text="", fg="gray", bg="#e5ddd5")
    state.typing_label.pack()

    input_frame = tk.Frame(chat_area)
    input_frame.pack(fill=tk.X)

    state.entry = tk.Entry(input_frame)
    state.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    state.entry.bind("<Return>", lambda e: send_message(state))

    tk.Button(input_frame, text="Send", command=lambda: send_message(state)).pack(side=tk.RIGHT)