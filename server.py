import os  # allows interacting with the os -> file & directory manipulation
import socket
import datetime


class MessageServer:
    def __init__(self, address, port):  # constructor
        self.address = address
        self.port = port
        # dictionar pt a stoca destinatarii si adresele lor
        # s-ar putea sa trebuiasca un SET -> sa nu permita val duplicate
        self.clients = {"john", "elis", "patrick", "harry", "louis"}
        self.servers = [('192.168.68.86', 5000)]  # lista pentru a stoca adresele altor servere

    def start(self):  # starting the server & accepting connections
        # AF_INET = address family, SOCK_STREAM = socket type -> TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.address, self.port))
            server_socket.listen()
            print(f"Server-ul asculta pe {self.address}:{self.port}")
            while True:
                conn, addr = server_socket.accept()
                with conn:
                    print(f"Conexiune noua de la {addr}")
                    data = conn.recv(1024)  # max datasize = 1024 bytes
                    if data:
                        message = data.decode()
                        print(f"Mesaj primit: {message}")
                        self.handle_message(message, conn, addr)

    def handle_message(self, message, conn, addr):
        # Parsare mesaj si extragere informatii
        recipient, sender, subject, text = message.split("|")
        # print(f"Received message: {subject} from {sender} to {recipient}")
        # print(f"Known recipients: {self.clients}")


        if recipient in self.clients:
            # Salveaza mesajul in directorul destinatarului
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{recipient.strip()}_{timestamp}.txt" # f"" = interpolare
            recipient_dir = recipient.strip()
            os.makedirs(recipient_dir, exist_ok=True)
            filename = f"{recipient_dir}/{filename}"
            with open(filename, "w") as file:
                file.write(f"From: {sender}\nSubject: {subject}\n\n{text}")
            print(f"Addr = {addr}")
            if addr[0] == "192.168.68.130":
                conn.sendall(b"Mesaj trimis cu succes.") # b"" = sir de octeti
            else:
                conn.sendall(b"Destinatar gasit.")
        else:
            # !!!! Apare bucla infinita daca serverele se refera intre ele !!! -> Nu mai apare e OK!
            # Cauta servere pentru destinatar
            print("Se verifica celelalte servere.")
            found = False  # Flag to track if the destination was found
            for server in self.servers:
                server_ip = server[0]
                if server_ip == addr[0]:
                    continue  # Exclude current server from search
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect(server)
                        s.sendall(message.encode())
                        data = s.recv(1024)
                        if data == b"Destinatar gasit.":
                            server_ip = server[0]
                            print(f"Destinatar gasit pe serverul cu IP-ul: {server_ip}")
                            conn.sendall(b"Mesaj trimis cu succes.")
                            found = True
                            break  # Exit the loop since the destination was found
                except Exception as e:
                    print(f"Error occurred: {e}")
                    continue  # Continue to the next server if an error occurs

            if not found:
                conn.sendall(b"Destinatarul nu a putut fi gasit.")


def main():
    server = MessageServer("192.168.68.130", 5000)
    server.start()


if __name__ == "__main__":
    main()
