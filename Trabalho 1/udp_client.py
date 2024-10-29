import socket
import hashlib
import os

# Configurações do cliente
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1028  # Tamanho do buffer
FILENAME = ""  # Nome do arquivo a ser requisitado
END_OF_FILE = b"EOF"  # Sinal de término
fileslist = ["example.txt", "elements.txt", "porcentagem.txt", "img.png"]

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
    print("=" + " " * 2 + "1 - Receber arquivo" + " " * 9 + "=")
    print("=" + " " * 2 + "2 - Configuração   " + " " * 9 + "=")
    print("=" + " " * 2 + "3 - Sair" + " " * 19 + "=")
    print("=-" * 15 + "=")
    return input("Escolha uma opção: ")

def menu_choose_file():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=-" * 15 + "=")
    print("=" + " " * 2 + "Menu de opções:" + " " * 12 + "=")
    for i, file in enumerate(fileslist):
        print("=" + " " * 2 + f"{i+1} - {file}" + " " * (20-len(file)) + "=")
    print("=-" * 15 + "=")
    return int(input("Escolha o arquivo: "))

def menu_config():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=-" * 15 + "=")
    print("=" + " " * 2 + "Menu de opções:" + " " * 12 + "=")
    print("=" + " " * 2 + f"1 - Alterar IP [{UDP_IP}]" + " " * (15 - len(UDP_IP)) + "=")
    print("=" + " " * 2 + f"2 - Alterar Porta [{UDP_PORT}]" + " " * (12 - len(str(UDP_PORT))) + "=")
    print("=" + " " * 2 + f"3 - Alterar Buffer Size [{BUFFER_SIZE}]" + " " * (6 - len(str(BUFFER_SIZE))) + "=")
    print("=" + " " * 2 + "4 - Voltar" + " " * 16 + "=")
    print("=-" * 15 + "=")
    return input("Escolha uma opção: ")

while True:
    option = menu()
    #os.system('cls' if os.name == 'nt' else 'clear')
    if option == "1":
        file_index = menu_choose_file()
        FILENAME = fileslist[file_index-1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        get_file(sock, FILENAME)
        sock.close()
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
                break
            else:
                print("Opção inválida. Tente novamente.")
        pass
    elif option == "3":
        break
    else:
        print("Opção inválida. Tente novamente.")
    