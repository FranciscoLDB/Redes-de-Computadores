import socket

# Configurações do cliente
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b"Hello, Server!"

# Criação do socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Envio da mensagem para o servidor
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

# Recebimento da resposta do servidor
data, server = sock.recvfrom(1024)
print("Resposta do servidor:", data.decode())
print("Endereço do servidor:", server)
