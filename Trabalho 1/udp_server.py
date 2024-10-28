import socket

# Configurações do servidor
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1024  # Tamanho do buffer

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
                    sock.sendto(chunk, addr)
            print(f"Arquivo {filename} enviado para {addr}")
        else:
            error_message = "ERRO: Arquivo não encontrado"
            sock.sendto(error_message.encode(), addr)
            print(f"Arquivo {filename} não encontrado. Mensagem de erro enviada para {addr}")
    else:
        error_message = "ERRO: Requisição inválida"
        sock.sendto(error_message.encode(), addr)
        print(f"Requisição inválida de {addr}. Mensagem de erro enviada.")
