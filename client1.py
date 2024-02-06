import socket

class MessageClient:
    def __init__(self):
        self.server_address = None
        self.server_port = None
        self.client_name = None

    def connect(self, server_address, server_port, client_name):
        self.server_address = server_address
        self.server_port = server_port
        self.client_name = client_name

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.server_address, self.server_port))
            message = f"connect|{self.client_name}"
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            print(data.decode())

    def send_new_message(self):
        if not self.server_address or not self.server_port or not self.client_name:
            print("Eroare: Conexiunea la server nu este stabilită. Vă rugăm să vă conectați mai întâi.")
            return

        recipient = input("Introduceti destinatarul: ")
        subject = input("Introduceti subiectul: ")
        text = input("Introduceti continutul mesajului: ")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.server_address, self.server_port))
            message = f"send_new_message|{self.client_name}|{recipient}|{subject}|{text}"
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            print(data.decode())

    def disconnect(self):
        if not self.server_address or not self.server_port or not self.client_name:
            print("Eroare: Conexiunea la server nu este stabilită.")
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.server_address, self.server_port))
            message = f"disconnect|{self.client_name}"
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            print(data.decode())
            self.server_address = None
            self.server_port = None
            self.client_name = None

def main():
    client = MessageClient()
    server_address = "192.168.100.159"
    server_port = 5000

    while True:
        command = input("Introduceti comanda (connect/send/disconnect): ")
        if command == "connect":
            client_name = input("Introduceti numele clientului: ")
            client.connect(server_address, server_port, client_name)
        elif command == "send":
            client.send_new_message()
        elif command == "disconnect":
            client.disconnect()
            break
        else:
            print("Comanda introdusa nu este valida.")

if __name__ == "__main__":
    main()
