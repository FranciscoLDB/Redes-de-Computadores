import socket
import os
import hashlib
import time
from random import randint

# Configurações do servidor
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1024  # Tamanho do buffer
END_OF_FILE = b"EOF"  # Sinal de término
PACKAGE_LOST = 0.1  # Probabilidade de perda de pacotes

# Função para calcular o checksum
def calculate_checksum(data):
    return hashlib.md5(data).hexdigest()

# Criação do socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"IP {UDP_IP} | Porta {UDP_PORT}")
print(f"Tamanho do buffer: {BUFFER_SIZE} bytes")
print("Servidor UDP pronto para receber mensagens...")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    request = data.decode().strip()
    print(f"Requisição recebida de {addr}: {request}")

    if request.startswith("GET"):
        filename = request.split()[1].lstrip('/')
        filepath = os.path.join('./server files', filename)
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as f:
                chunk_number = 0
                while True: 
                    chunk = f.read(BUFFER_SIZE)
                    if not chunk:
                        break

                    # Simular perda de pacotes
                    if randint(1, 100) <= PACKAGE_LOST * 100:
                        print(f"Pacote {chunk_number} perdido")
                        chunk_number += 1
                        continue

                    checksum = calculate_checksum(chunk)
                    numbered_chunk = f"{chunk_number:04d}".encode() + chunk
                    sock.sendto(checksum.encode(), addr)
                    #print(f"Checksum {checksum} enviado para {addr}")
                    time.sleep(0.2)  # Delay de 0.2 segundos

                    sock.sendto(numbered_chunk, addr)
                    print(f"Chunk número {chunk_number} enviado para {addr}")
                    time.sleep(0.2)  # Delay de 0.2 segundos
                    
                    chunk_number += 1
                # Enviar sinal de término
                sock.sendto(END_OF_FILE, addr)
                print(f"Arquivo {filename} enviado para {addr}")
        else:
            error_message = f"ERRO: Arquivo {filename} não encontrado no diretório ./server files"
            sock.sendto(error_message.encode(), addr)
            print(error_message)
    else:
        error_message = "ERRO: Requisição inválida"
        sock.sendto(error_message.encode(), addr)
        print(f"Requisição inválida de {addr}. Mensagem de erro enviada.")
