import socket

def send_message(server_address, server_port):
    recipient = input("Introduceti destinatarul: ")
    sender = input("Introduceti expeditorul: ")
    subject = input("Introduceti subiectul: ")
    text = input("Introduceti textul mesajului: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_address, server_port))
        message = f"{recipient}|{sender}|{subject}|{text}"
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        while data != b"":
            print(data.decode())  # Afisam mesajul primit de la server
            data = client_socket.recv(1024)

def main():
    # Exemplu de utilizare a clientului
    server_address = "192.168.68.130"
    server_port = 5000
    send_message(server_address, server_port)

if __name__ == "__main__":
    main()
