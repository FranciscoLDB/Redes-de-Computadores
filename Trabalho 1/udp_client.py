import socket
import hashlib
import os
from random import randint

# Configurações do cliente
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1028  # Tamanho do buffer
FILENAME = ""  # Nome do arquivo a ser requisitado
END_OF_FILE = b"EOF"  # Sinal de término
FILE_NOT_FOUND = b"FNF" # Sinal de arquivo não encontrado
PACKAGE_LOST = 0  # Probabilidade de perda de pacotes
fileslist = ["elements.txt", "porcentagem.txt", "img.png", "notfound.txt"]

# Função para calcular o checksum
def calculate_checksum(data):
    return hashlib.md5(data).hexdigest()

def get_file(sock, filename):
    # Envio da requisição para o servidor
    request = f"GET /{filename}"
    sock.sendto(request.encode(), (UDP_IP, UDP_PORT))

    # Criação do diretório se não existir
    if not os.path.exists('./files received'):
        os.makedirs('./files received')

    chunks_received = {}
    while True:
        checksum, addr = sock.recvfrom(BUFFER_SIZE)
        if checksum == END_OF_FILE:
            print("Recepção do arquivo concluída.")
            break
        elif checksum == FILE_NOT_FOUND:
            print(f"Arquivo {filename} não encontrado.")
            input("Pressione qualquer tecla para continuar...")
            return

        if randint(1, 100) <= PACKAGE_LOST * 100:
            print("Pacote perdido")
            continue

        numbered_chunk, addr = sock.recvfrom(BUFFER_SIZE)
        chunk_number = int(numbered_chunk[:4])
        data = numbered_chunk[4:]
        print(f"Recebido chunk número {chunk_number} de {addr}")

        if calculate_checksum(data) == checksum.decode():
            chunks_received[chunk_number] = data
        else:
            print("Erro de checksum, dados corrompidos")

    if not chunks_received:
        print("Nenhum chunk recebido")
        return

    # Recepção do arquivo com verificação de checksum
    os.makedirs("./files received", exist_ok=True)
    try:
        with open(f"./files received/recebido_{filename}", 'wb') as f:
            for chunk_number in sorted(chunks_received.keys()):
                f.write(chunks_received[chunk_number])
    except Exception as e:
        print(f"Erro ao abrir ou escrever no arquivo: {e}")
    

    print(f"Arquivo {filename} recebido e salvo como ./files_received/recebido_{filename}\n")
    input("Pressione qualquer tecla para continuar...")

def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=-" * 15 + "=")
    print("=" + " " * 2 + "Menu de opções:" + " " * 12 + "=")
    print("=" + " " * 2 + "1 - Receber arquivo" + " " * 8 + "=")
    print("=" + " " * 2 + "2 - Configuração   " + " " * 8 + "=")
    print("=" + " " * 2 + "3 - Sair" + " " * 19 + "=")
    print("=-" * 15 + "=")
    return input("Escolha uma opção: ")

def menu_choose_file():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=-" * 15 + "=")
    print("=" + " " * 2 + "Menu de opções:" + " " * 12 + "=")
    for i, file in enumerate(fileslist):
        print("=" + " " * 2 + f"{i+1} - {file}" + " " * (23-len(file)) + "=")
    print("=-" * 15 + "=")
    return int(input("Escolha o arquivo: "))

def menu_config():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=-" * 15 + "=")
    print("=" + " " * 2 + "Menu de opções:" + " " * 12 + "=")
    print("=" + " " * 2 + f"1 - IP [{UDP_IP}]" + " " * (23 - len(UDP_IP) - len("IP []")) + "=")
    print("=" + " " * 2 + f"2 - Porta [{UDP_PORT}]" + " " * (23 - len(str(UDP_PORT)) - len("Porta []")) + "=")
    print("=" + " " * 2 + f"3 - Buffer Size [{BUFFER_SIZE}]" + " " * (23 - len(str(BUFFER_SIZE)) - len("Buffer Size []")) + "=")
    print("=" + " " * 2 + f"4 - Package Lost [{PACKAGE_LOST*100}%]" + " " * (23 - len(str(PACKAGE_LOST*100)) - len("Package Lost [%]")) + "=")
    print("=" + " " * 2 + "5 - Voltar" + " " * 17 + "=")
    print("=-" * 15 + "=")
    return input("Escolha uma opção: ")

while True:
    option = menu()
    #os.system('cls' if os.name == 'nt' else 'clear')
    if option == "1":
        while True:
            file_index = menu_choose_file()
            if 1 <= file_index <= len(fileslist):
                FILENAME = fileslist[file_index-1]
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                get_file(sock, FILENAME)
                sock.close()
                break
            else:
                print("Opção inválida. Tente novamente.")
    elif option == "2":
        while True:
            option = menu_config()
            if option == "1":
                UDP_IP = input("Digite o novo IP: ")
            elif option == "2":
                UDP_PORT = int(input("Digite a nova porta: "))
            elif option == "3":
                BUFFER_SIZE = int(input("Digite o novo buffer size: "))
            elif option == "4":
                new_package_lost = float(input("Digite a nova probabilidade de perda de pacotes (0-100): "))
                if 0 <= new_package_lost <= 100:
                    PACKAGE_LOST = new_package_lost / 100
                else:
                    print("Valor inválido. A probabilidade deve estar entre 0 e 100.")
            elif option == "5":
                break
            else:
                print("Opção inválida. Tente novamente.")
        pass
    elif option == "3":
        break
    else:
        print("Opção inválida. Tente novamente.")
    