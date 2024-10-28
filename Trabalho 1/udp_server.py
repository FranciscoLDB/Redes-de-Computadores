import socket

# Configurações do servidor
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Criação do socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Servidor UDP pronto para receber mensagens...")

while True:
    data, addr = sock.recvfrom(1024)  # Buffer de 1024 bytes
    print("Mensagem recebida:", data.decode())
    print("Endereço do cliente:", addr)
    sock.sendto(b"Hello, Client!", addr)
