import socket
import hashlib

# Configurações do cliente
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1024  # Tamanho do buffer
FILENAME = "example.txt"  # Nome do arquivo a ser requisitado
END_OF_FILE = b"EOF"  # Sinal de término

# Função para calcular o checksum
def calculate_checksum(data):
    return hashlib.md5(data).hexdigest()

# Criação do socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Envio da requisição para o servidor
request = f"GET /{FILENAME}"
sock.sendto(request.encode(), (UDP_IP, UDP_PORT))

# Recepção do arquivo com verificação de checksum
with open(f"recebido_{FILENAME}", 'wb') as f:
    while True:
        checksum, addr = sock.recvfrom(BUFFER_SIZE)
        if checksum == END_OF_FILE:
            print("Recepção do arquivo concluída.")
            break
        data, addr = sock.recvfrom(BUFFER_SIZE)
        if calculate_checksum(data) == checksum.decode():
            f.write(data)
            print(f"Recebido {len(data)} bytes de {addr}")
        else:
            print("Erro de checksum, dados corrompidos")

print(f"Arquivo {FILENAME} recebido e salvo como recebido_{FILENAME}")
