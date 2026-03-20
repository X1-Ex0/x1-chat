import tkinter as tk
import threading
from client.state import AppState
from client.ui import build_ui
from client.network import receive

state = AppState()

def start():
    state.nickname = state.name_entry.get().strip()

    if not state.nickname:
        state.status_label.config(text="Nama tidak boleh kosong")
        return

    try:
        state.client.connect((state.HOST, state.PORT))
    except Exception as e:
        state.status_label.config(text="Gagal connect ke server")
        print(e)
        return

    state.login.pack_forget()
    build_ui(state)

    threading.Thread(target=receive, args=(state,), daemon=True).start()


state.root = tk.Tk()
state.root.geometry("550x600")

state.login = tk.Frame(state.root)
state.login.pack(expand=True)

tk.Label(state.login, text="X1 CHAT").pack()

state.name_entry = tk.Entry(state.login)
state.name_entry.pack()

state.status_label = tk.Label(state.login, text="", fg="red")
state.status_label.pack()

tk.Button(state.login, text="Masuk", command=start).pack()

state.root.mainloop()