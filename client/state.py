import socket

class AppState:
    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 0

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.nickname = ""
        self.current_chat = "GLOBAL"
        self.selected_button = None
        self.chat_history = {"GLOBAL": []}

        # UI refs
        self.root = None
        self.login = None
        self.name_entry = None
        self.status_label = None
        self.entry = None
        self.canvas = None
        self.chat_frame = None
        self.user_frame = None
        self.typing_label = None
        self.chat_target_label = None
        self.typing_after_id = None