import socket
import threading
import os

# Variáveis globais para IP e porta
SERVER_IP = "0.0.0.0"
SERVER_PORT = 5003
BUFFER_SIZE = 8192

def handle_client(client_socket):
    client_ip, client_port = client_socket.getpeername()
    print(f"\033[92mCliente conectado com IP: {client_ip} e porta: {client_port}\033[0m")
    try:
        # Recebe a requisição do cliente
        request = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        print(f"Requisição recebida:\n{request}")

        # Parse da requisição HTTP
        headers = request.split('\n')
        first_line = headers[0].split()
        method = first_line[0]
        path = first_line[1]

        if method == 'GET':
            # Define o caminho do arquivo solicitado
            if path == '/':
                path = '/index.html'
            file_path = f"server files{path}"

            # Verifica se o arquivo existe
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    response_body = file.read()
                response_header = 'HTTP/1.1 200 OK\n'
            else:
                try:
                    with open('server files/error.html', 'rb') as file:
                        response_body = file.read()
                except:
                    response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
                response_header = 'HTTP/1.1 404 Not Found\n'

            # Envia a resposta HTTP
            if path.endswith('.jpeg'):
                response_header += 'Content-Type: image/jpeg\n'
            elif path.endswith('.png'):
                response_header += 'Content-Type: image/png\n'
            elif path.endswith('.json'):
                response_header += 'Content-Type: application/json\n'
            else:
                response_header += 'Content-Type: text/html\n'
            response_header += f'Content-Length: {len(response_body)}\n'
            response_header += 'Connection: close\n\n'
            client_socket.send(response_header.encode('utf-8') + response_body)
        else:
            # Método não suportado
            response_body = b"<html><body><h1>405 Method Not Allowed</h1></body></html>"
            response_header = 'HTTP/1.1 405 Method Not Allowed\n'
            response_header += 'Content-Type: text/html\n'
            response_header += f'Content-Length: {len(response_body)}\n'
            response_header += 'Connection: close\n\n'
            client_socket.send(response_header.encode('utf-8') + response_body)
    except Exception as e:
        print(f"Erro ao processar a requisição: {e}")
    finally:
        client_socket.close()
        if '200 OK' in response_header:
            print(f"\033[92mResposta enviada com sucesso:\n{response_header}\033[0m")
        else:
            print(f"\033[91mResposta enviada com erro:\n{response_header}\033[0m")
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