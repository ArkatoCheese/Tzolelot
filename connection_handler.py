import socket
RECEIVE_BUFFER = 1024
MESSAGE_END = "\n\n"


class ConnectionHandler:
    def __init__(self, connection_socket: socket.socket):
        self.socket = connection_socket

    def send_message(self, message):
        print(f"Sending:\n{message}")
        self.socket.send((message + MESSAGE_END).encode())

    def receive_message(self):
        message = ""
        while not message.endswith(MESSAGE_END):
            message += self.socket.recv(RECEIVE_BUFFER).decode()
        print(f"Received:\n{message}")
        return message[:-len(MESSAGE_END)]
