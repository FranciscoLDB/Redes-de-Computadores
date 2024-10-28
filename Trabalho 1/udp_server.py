import socket
import os
import hashlib

# Configurações do servidor
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1024  # Tamanho do buffer
END_OF_FILE = b"EOF"  # Sinal de término

# Função para calcular o checksum
def calculate_checksum(data):
    return hashlib.md5(data).hexdigest()

# Criação do socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Servidor UDP pronto para receber mensagens...")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    request = data.decode().strip()
    print(f"Requisição recebida de {addr}: {request}")

    if request.startswith("GET"):
        filename = request.split()[1].lstrip('/')
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                while True:
                    chunk = f.read(BUFFER_SIZE)
                    if not chunk:
                        break
                    checksum = calculate_checksum(chunk)
                    sock.sendto(checksum.encode(), addr)
                    sock.sendto(chunk, addr)
                # Enviar sinal de término
                sock.sendto(END_OF_FILE, addr)
                print(f"Arquivo {filename} enviado para {addr}")
        else:
            error_message = f"ERRO: Arquivo {filename} não encontrado no diretório {os.getcwd()}"
            sock.sendto(error_message.encode(), addr)
            print(error_message)
    else:
        error_message = "ERRO: Requisição inválida"
        sock.sendto(error_message.encode(), addr)
        print(f"Requisição inválida de {addr}. Mensagem de erro enviada.")
