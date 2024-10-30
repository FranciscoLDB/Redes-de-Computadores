import socket
import os
import hashlib
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1024  # Tamanho do buffer
END_OF_FILE = b"EOF"  # Sinal de término
FILE_NOT_FOUND = b"FNF" # Sinal de arquivo não encontrado
CHUNKS = b"CHN" # Sinal de chunks
DELAY = 0.2  # Delay das mensagens

def calculate_checksum(data):
    return hashlib.md5(data).hexdigest()

# Criação do socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"IP {UDP_IP} | Porta {UDP_PORT}")
print(f"Tamanho do buffer: {BUFFER_SIZE} bytes")
print("Servidor UDP pronto para receber mensagens...")

def file_request(request):
    filename = request.split()[1].lstrip('/')
    filepath = os.path.join('./server files', filename)
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as f:
            chunk_number = 0
            
            total_chunks = os.path.getsize(filepath) // BUFFER_SIZE + 1
            print(f"Total de chunks a serem enviados: {total_chunks}")
            sock.sendto(CHUNKS + str(total_chunks).encode(), addr)
            time.sleep(DELAY)
            while True: 
                chunk = f.read(BUFFER_SIZE)
                if not chunk:
                    break

                checksum = calculate_checksum(chunk)
                numbered_chunk = f"{chunk_number:04d}".encode() + chunk
                sock.sendto(checksum.encode(), addr)
                time.sleep(DELAY)

                sock.sendto(numbered_chunk, addr)
                print(f"Chunk número {chunk_number} enviado para {addr}")
                time.sleep(DELAY)
                
                chunk_number += 1
            
            sock.sendto(END_OF_FILE, addr)
            print(f"Arquivo {filename} enviado para {addr}\n")
    else:
        sock.sendto(FILE_NOT_FOUND, addr)
        print(f"Arquivo {filename} não encontrado. Mensagem de erro enviada.")

def chunk_request(request):
    filename = request.split()[1].lstrip('/')
    filepath = os.path.join('./server files', filename)
    chunk_request = request.split()[3].lstrip('/')
    print(f"Requisição de chunk {chunk_request} do arquivo {filename}")
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as f:
            chunk_number = int(chunk_request)
            f.seek(chunk_number * BUFFER_SIZE)
            chunk = f.read(BUFFER_SIZE)
            if not chunk:
                sock.sendto(END_OF_FILE, addr)
                print(f"Chunk {chunk_request} do arquivo {filename} enviado para {addr}")
            else:
                checksum = calculate_checksum(chunk)
                numbered_chunk = f"{chunk_number:04d}".encode() + chunk
                sock.sendto(checksum.encode(), addr)
                time.sleep(DELAY)
                sock.sendto(numbered_chunk, addr)
                print(f"Chunk número {chunk_number} enviado")
                
            sock.sendto(END_OF_FILE, addr)
            print(f"Arquivo {filename} enviado para {addr}\n")
    else:
        sock.sendto(FILE_NOT_FOUND, addr)
        print(f"Arquivo {filename} não encontrado. Mensagem de erro enviada.")

while True:
    global addr
    data, addr = sock.recvfrom(BUFFER_SIZE)
    request = data.decode().strip()
    print(f"\nRequisição recebida de {addr}: {request}")

    if request.startswith("GET") and request.endswith("ALL"):
        file_request(request)
    elif request.startswith("GET") and "CHUNKS" in request:
        chunk_request(request)
    else:
        error_message = "ERRO: Requisição inválida"
        sock.sendto(error_message.encode(), addr)
        print(f"Requisição inválida de {addr}. Mensagem de erro enviada.")
