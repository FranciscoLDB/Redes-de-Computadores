import socket
import threading
import hashlib
import os
import time

# Variáveis globais para IP e porta
SERVER_IP = "0.0.0.0"
SERVER_PORT = 5003
BUFFER_SIZE = 8192
DELAY = 0.01

def handle_client(client_socket):
    client_ip, client_port = client_socket.getpeername()
    print(f"\033[92mCliente conectado com IP: {client_ip} e porta: {client_port}\033[0m")
    client_socket.send(b"Bem-vindo ao servidor TCP!")

    while True:
        try:
            # Recebe dados do cliente
            request = client_socket.recv(BUFFER_SIZE)
            if not request:
                break

            message = request.decode('utf-8')
            print(f"[{client_ip}:{client_port}] Recebido: {message}")

            if message.strip().upper() == "SAIR":
                print(f"\033[91m[{client_ip}:{client_port}] Cliente solicitou desconexão.\033[0m")
                break
            elif message.strip().upper().startswith("ARQUIVO"):
                _, file_name = message.split()
                file_path = f"server files/{file_name}"
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    file_packages = file_size // BUFFER_SIZE + 1
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                    file_hash = hashlib.sha256(file_data).hexdigest()

                    # Envia os metadados juntos
                    metadata = f"NOME:{file_name};TAMANHO:{file_size};PACOTES:{file_packages};HASH:{file_hash}"
                    client_socket.send(metadata.encode('utf-8'))
                    #print(f"[{client_ip}:{client_port}] Metadados enviados: {metadata}")
                    time.sleep(0.1)

                    # Recebe a confirmação do cliente
                    confirm = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                    if confirm.strip().upper() != "OK":
                        print(f"\033[93m[{client_ip}:{client_port}] Cliente não confirmou o download.\033[0m")
                        continue

                    # Envia os dados do arquivo em pacotes
                    cont_pacotes = 0
                    with open(file_path, "rb") as f:
                        while True:
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            cont_pacotes += 1
                            client_socket.send(bytes_read)
                            if cont_pacotes == 1 or cont_pacotes % (file_packages // 10) == 0 or cont_pacotes == file_packages:
                                print(f"\033[32m[{client_ip}:{client_port}] Enviando dados do arquivo [{cont_pacotes}/{file_packages}]...\033[0m")
                            time.sleep(DELAY)

                    # Envia o status final
                    client_socket.send(b"STATUS:OK")
                    print(f"\033[32m[{client_ip}:{client_port}] Arquivo enviado com sucesso.\033[0m")
                else:
                    client_socket.send(b"STATUS:NOK")
                    print(f"\033[93m[{client_ip}:{client_port}] Arquivo inexistente.\033[0m")

            elif message.strip().upper() == "CHAT":
                # Envia uma mensagem de chat para o cliente
                chat_message = input(f"[{client_ip}:{client_port}] Digite a mensagem para enviar ao cliente: ")
                client_socket.send(chat_message.encode('utf-8'))
            else:
                # Processa a requisição e envia uma resposta
                response = f"Servidor recebeu: {message}"
                client_socket.send(response.encode('utf-8'))
                print(f"[{client_ip}:{client_port}] Resposta enviada: {response}")

        except ConnectionResetError:
            break

    client_socket.close()
    print(f"Cliente desconectado com IP: {client_ip} e porta: {client_port}")

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