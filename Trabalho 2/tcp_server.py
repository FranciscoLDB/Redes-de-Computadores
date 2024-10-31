import socket
import threading
import hashlib
import os

# Variáveis globais para IP e porta
SERVER_IP = "0.0.0.0"
SERVER_PORT = 5002
BUFFER_SIZE = 1024

def handle_client(client_socket):
    print("Cliente conectado.")
    client_socket.send(b"Bem-vindo ao servidor TCP!")

    while True:
        try:
            # Recebe dados do cliente
            request = client_socket.recv(BUFFER_SIZE)
            if not request:
                break

            message = request.decode('utf-8')
            print(f"Recebido: {message}")

            if message.strip().upper() == "SAIR":
                print("Cliente solicitou desconexão.")
                break
            elif message.strip().upper() == "ARQUIVO":
                # Envia um arquivo para o cliente
                with open("server files/img.png", "rb") as f:
                    file_data = f.read()
                file_hash = hashlib.md5(file_data).hexdigest()
                client_socket.send(file_data)
                client_socket.send(file_hash.encode('utf-8'))
            elif message.strip().upper() == "CHAT":
                # Envia uma mensagem de chat para o cliente
                chat_message = "Olá do servidor!"
                client_socket.send(chat_message.encode('utf-8'))
            else:
                # Processa a requisição e envia uma resposta
                response = f"Servidor recebeu: {message}"
                client_socket.send(response.encode('utf-8'))

        except ConnectionResetError:
            break

    client_socket.close()
    print("Cliente desconectado.")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(5)
    print(f"Servidor ouvindo na porta {SERVER_PORT}...")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexão aceita de {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()