import socket
import hashlib
import os

# Configurações do cliente
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1024  # Tamanho do buffer
FILENAME = "example.txt"  # Nome do arquivo a ser requisitado
END_OF_FILE = b"EOF"  # Sinal de término

# Função para calcular o checksum
def calculate_checksum(data):
    return hashlib.md5(data).hexdigest()

def get_file(sock, filename):
    # Envio da requisição para o servidor
    request = f"GET /{filename}"
    sock.sendto(request.encode(), (UDP_IP, UDP_PORT))

    # Recepção do arquivo com verificação de checksum
    with open(f"recebido_{filename}", 'wb') as f:
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

    print(f"Arquivo {filename} recebido e salvo como recebido_{filename}\n")

def menu():
    print("=-" * 15 + "=")
    print("=" + " " * 2 + "Menu de opções:" + " " * 12 + "=")
    print("=" + " " * 2 + "1 - Enviar arquivo" + " " * 9 + "=")
    print("=" + " " * 2 + "2 - Sair" + " " * 19 + "=")
    print("=-" * 15 + "=")
    return input("Escolha uma opção: ")

while True:
    option = menu()
    #os.system('cls' if os.name == 'nt' else 'clear')
    if option == "1":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        get_file(sock, FILENAME)
        sock.close()
    elif option == "2":
        break
    else:
        print("Opção inválida. Tente novamente.")
    