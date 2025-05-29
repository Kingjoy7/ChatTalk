import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import datetime

# === CONFIG ===
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 12345
DEFAULT_USERNAME = 'Guest'
THEME = 'dark'  # Options: 'dark' or 'light'

# === COLOR SCHEME ===
colors = {
    'dark': {
        'bg': '#1e1e1e',
        'fg': '#ffffff',
        'input_bg': '#2d2d2d',
        'input_fg': '#ffffff',
        'system': '#888888',
        'username': '#4FC3F7',
        'timestamp': '#9CCC65'
    },
    'light': {
        'bg': '#f2f2f2',
        'fg': '#000000',
        'input_bg': '#ffffff',
        'input_fg': '#000000',
        'system': '#555555',
        'username': '#1565C0',
        'timestamp': '#558B2F'
    }
}

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")
        self.master.geometry("700x500")
        self.master.protocol("WM_DELETE_WINDOW", self.disconnect)

        self.theme = colors[THEME]
        self.sock = None
        self.username = None
        self.running = False

        self.build_gui()
        self.prompt_login()

    def build_gui(self):
        self.master.configure(bg=self.theme['bg'])

        self.chat_area = scrolledtext.ScrolledText(self.master, bg=self.theme['bg'], fg=self.theme['fg'], state='disabled', wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.entry_frame = tk.Frame(self.master, bg=self.theme['bg'])
        self.entry_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.msg_entry = tk.Entry(self.entry_frame, bg=self.theme['input_bg'], fg=self.theme['input_fg'])
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.msg_entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = tk.Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT)

        self.user_list = tk.Listbox(self.master, bg=self.theme['input_bg'], fg=self.theme['input_fg'], width=25)
        self.user_list.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=5)

        self.setup_tags()

    def setup_tags(self):
        self.chat_area.tag_config('system', foreground=self.theme['system'], font=('Arial', 10, 'italic'))
        self.chat_area.tag_config('username', foreground=self.theme['username'], font=('Arial', 10, 'bold'))
        self.chat_area.tag_config('timestamp', foreground=self.theme['timestamp'], font=('Arial', 9))

    def prompt_login(self):
        host = simpledialog.askstring("Server IP", "Enter server IP:", initialvalue=DEFAULT_HOST)
        port = simpledialog.askinteger("Port", "Enter port number:", initialvalue=DEFAULT_PORT)
        username = simpledialog.askstring("Username", "Choose a username:", initialvalue=DEFAULT_USERNAME)

        if not host or not port or not username:
            self.master.destroy()
            return

        self.username = username
        self.connect(host, port)

    def connect(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host, port))
            self.sock.send(self.username.encode('utf-8'))
            self.running = True
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.display_system_message("Connected to the server.")
        except Exception as e:
            messagebox.showerror("Connection Failed", f"Failed to connect to server: {e}")
            self.master.destroy()

    def receive_messages(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message.startswith("USERLIST:"):
                    users = message.split(":", 1)[1].split(",")
                    self.update_user_list(users)
                elif message.startswith("KICKED:"):
                    self.display_system_message("You were kicked from the chat by an admin.")
                    break
                elif message == "SERVER_SHUTDOWN":
                    self.display_system_message("Server has shut down.")
                    break
                else:
                    self.display_message(message)
            except:
                break
        self.disconnect()

    def send_message(self):
        message = self.msg_entry.get().strip()
        if message:
            try:
                self.sock.send(message.encode('utf-8'))
                self.msg_entry.delete(0, tk.END)
            except:
                self.display_system_message("Failed to send message. Server might be down.")

    def update_user_list(self, users):
        self.user_list.delete(0, tk.END)
        for user in users:
            self.user_list.insert(tk.END, user)

    def display_message(self, message):
        self.chat_area.config(state='normal')

        # Parse timestamp and username if possible
        if ']:' in message:
            try:
                username_part, msg_part = message.split(']: ', 1)
                username = username_part.split(' [')[0]
                timestamp = username_part.split('[')[-1]
                self.chat_area.insert(tk.END, f"[{timestamp}] ", 'timestamp')
                self.chat_area.insert(tk.END, f"{username}: ", 'username')
                self.chat_area.insert(tk.END, f"{msg_part}\n")
            except:
                self.chat_area.insert(tk.END, f"{message}\n")
        else:
            self.chat_area.insert(tk.END, f"{message}\n")

        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def display_system_message(self, message):
        timestamp = datetime.datetime.now().strftime("[%H:%M]")
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{timestamp} * {message}\n", 'system')
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def disconnect(self):
        if self.running:
            self.running = False
            try:
                self.sock.close()
            except:
                pass
            self.display_system_message("Disconnected from server.")
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
