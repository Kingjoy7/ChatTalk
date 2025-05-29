📡 Multi-User Chat Application (Raw Sockets in Python)
A simple command-line based multi-user chat application built using raw Python sockets and threading, allowing multiple clients to connect to a single server and exchange real-time messages.

🛠️ Features
Real-time communication between multiple clients.

Server handles multiple client connections using multithreading.

Each client can send messages that are broadcast to all other connected clients.

Server logs client connections, disconnections, and messages.

Graceful client disconnection handling.

🧱 Tech Stack
Language: Python

Modules Used:

socket — for networking.

threading — to handle concurrent connections.

🗂️ Project Structure
bash
Copy
Edit
chat-app/
├── server.py     # Server-side script
├── client.py     # Client-side script
└── README.md     # Project documentation
🚀 Getting Started
🔧 Prerequisites
Python 3.x installed on your system.

🖥️ Running the Server
Open a terminal.

Navigate to the project directory.

Run the server:

bash
Copy
Edit
python server.py
By default, the server listens on 127.0.0.1 (localhost) and port 5000.

👥 Running a Client
Open another terminal (or multiple terminals for multiple clients).

Navigate to the project directory.

Run the client:

bash

python client.py
Enter your username when prompted, and start chatting!

📷 Example
Server Terminal:

[SERVER STARTED] Listening on 127.0.0.1:5000
[NEW CONNECTION] Alice connected.
[MESSAGE] Alice: Hello everyone!
[DISCONNECTED] Bob has left the chat.
Client Terminal:
markdown

Enter your name: Alice
You joined the chat.
> Hello everyone!
🧠 How It Works
Server:

Binds to a host and port.

Accepts incoming client connections in separate threads.

Broadcasts received messages to all connected clients except the sender.

Client:

Connects to the server.

Sends user input to the server.

Listens for incoming messages from the server in a separate thread.

🧪 To Test
Start the server.

Run multiple client scripts in different terminals.

Send messages from each client and observe how all connected clients receive the broadcast.

📌 Limitations
No encryption (plaintext messages over the network).

No GUI — command-line interface only.

No user authentication.

🚧 Future Enhancements
Add username validation and private messaging.

Implement GUI with tkinter or PyQt.

Add chat history, user list, and typing indicators.

Integrate TLS/SSL for secure communication.

📄 License
This project is open-source and available under the MIT License.
