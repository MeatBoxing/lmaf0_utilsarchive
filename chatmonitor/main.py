import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
import requests
import json
import ctypes
from ctypes import wintypes

url = "urlhere"
seen_messages = set()


def ping_server():
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        return data
    except Exception as e:
        print("Error:", e)
        return None

def extract_chat_messages(data, text_edit):
    global seen_messages
    if data and "updates" in data:
        for item in data["updates"]:
            if "type" in item:
                message_type = item["type"]
                if message_type == "chat" and "source" in item and item["source"] == "player":
                    message_key = (item.get('timestamp'), item.get('account'), item.get('message'))
                    if message_key not in seen_messages:
                        text_edit.append(f"<{item.get('account')}> {item.get('message')}")
                        seen_messages.add(message_key)
                elif message_type == "playerquit":
                    quit_key = (item.get('timestamp'), item.get('account'))
                    if quit_key not in seen_messages:
                        text_edit.append(f"<font color='yellow'>{item.get('account')} left the game</font>")
                        seen_messages.add(quit_key)
                elif message_type == "playerjoin":
                    join_key = (item.get('timestamp'), item.get('account'))
                    if join_key not in seen_messages:
                        text_edit.append(f"<font color='yellow'>{item.get('account')} joined the game</font>")
                        seen_messages.add(join_key)

class DarkModeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minecraft Chat")
        self.setWindowIcon(QIcon("chat.png")) # Set your icon file here
        self.setGeometry(100, 100, 800, 600)
        self.set_title_bar_color(0, 128, 128)  # Dark blue color

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout(self.central_widget)
        
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        self.text_edit.setReadOnly(True)
        self.text_edit.setFocusPolicy(Qt.NoFocus)
        self.text_edit.setStyleSheet("background-color: black; color: white;")
        font = self.text_edit.font()
        font.setFamily("Consolas")
        font.setPointSize(16)
        self.text_edit.setFont(font)

        self.setStyleSheet("background-color: black;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_chat)
        self.timer.start(1000)

    def update_chat(self):
        data = ping_server()
        extract_chat_messages(data, self.text_edit)
    
    def set_title_bar_color(self, r, g, b):
        hwnd = self.winId().__int__()
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(wintypes.BOOL(True)), ctypes.sizeof(wintypes.BOOL))
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int))
        color = r + (g << 8) + (b << 16)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(color)), ctypes.sizeof(ctypes.c_int))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dark_mode_app = DarkModeApp()
    dark_mode_app.show()
    sys.exit(app.exec_())
