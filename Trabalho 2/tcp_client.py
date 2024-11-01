import socket
import hashlib
import os

TCP_IP = "127.0.0.1"
TCP_PORT = 5003
BUFFER_SIZE = 8192
TIME_OUT = 5
IS_CONNECTED = False
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
FILESLIST = ["img.png", "15mb.txt", "music.mp3", "notfound.not"]

def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=-" * 15 + "=")
    status = "Conectado" if IS_CONNECTED else "Desconectado"
    print("=" + " " * 2 + f"Status: {status}" + " " * (23 - len(status)) + "=")
    print("=" + " " * 2 + "Menu de opções:    " + " " * 8 + "=")
    print("=" + " " * 2 + "1 - Receber arquivo" + " " * 8 + "=")
    print("=" + " " * 2 + "2 - Chat           " + " " * 8 + "=")
    print("=" + " " * 2 + "3 - Configuração   " + " " * 8 + "=")
    print("=" + " " * 2 + "4 - Conectar       " + " " * 8 + "=")
    print("=" + " " * 2 + "5 - Sair           " + " " * 8 + "=")
    print("=-" * 15 + "=")
    return input("Escolha uma opção: ")

def menu_choose_file():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=-" * 15 + "=")
    print("=" + " " * 2 + "Menu de opções:" + " " * 12 + "=")
    for i, file in enumerate(FILESLIST):
        print("=" + " " * 2 + f"{i+1} - {file}" + " " * (23-len(file)) + "=")
    print("=-" * 15 + "=")
    return int(input("Escolha o arquivo: "))

def menu_config():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=-" * 15 + "=")
        print("=" + " " * 2 + "Menu de opções:" + " " * 12 + "=")
        print("=" + " " * 2 + f"1 - IP [{TCP_IP}]" + " " * (23 - len(TCP_IP) - len("IP []")) + "=")
        print("=" + " " * 2 + f"2 - Porta [{TCP_PORT}]" + " " * (23 - len(str(TCP_PORT)) - len("Porta []")) + "=")
        print("=" + " " * 2 + f"3 - Buffer Size [{BUFFER_SIZE}]" + " " * (23 - len(str(BUFFER_SIZE)) - len("Buffer Size []")) + "=")
        print("=" + " " * 2 + f"4 - Time out [{TIME_OUT}s]" + " " * (23 - len(str(TIME_OUT)) - len("Time out [s]")) + "=")
        print("=" + " " * 2 + "5 - Voltar" + " " * 17 + "=")
        print("=-" * 15 + "=")
        option = input("Escolha uma opção: ")
        if option == "1":
            TCP_IP = input("Digite o IP: ")
        elif option == "2":
            TCP_PORT = int(input("Digite a porta: "))
        elif option == "3":
            BUFFER_SIZE = int(input("Digite o buffer size: "))
        elif option == "4":
            TIME_OUT = int(input("Digite o time out: "))
        elif option == "5":
            break
        else:
            print("Opção inválida. Tente novamente.")

def progress_bar(percent):
    os.system('cls' if os.name == 'nt' else 'clear')
    bar_length = 40
    block = int(round(bar_length * percent / 100))
    text = f"\r[{'#' * block + '-' * (bar_length - block)}] {percent:.2f}%"
    print("\nBaixando arquivo:")
    print(text, end="")

def print_metadata(metadata):
    resp_name, resp_size, resp_pckg, resp_hash = metadata.split(";")
    print(f"Nome: {resp_name.split(':')[1]}")
    print(f"Tamanho: {resp_size.split(':')[1]} bytes")
    print(f"Pacotes: {resp_pckg.split(':')[1]}")
    #print(f"Hash: {resp_hash.split(':')[1]}")

def check_hash(data, file_hash):
    print(f"\nHash calculado: {hashlib.sha256(data).hexdigest()}")
    print(f"Hash recebido: {file_hash}")
    return hashlib.sha256(data).hexdigest() == file_hash

def archive():
    file_index = menu_choose_file() - 1
    if file_index < 0 or file_index >= len(FILESLIST):
        print("Arquivo inválido.")
        return
    file_name = FILESLIST[file_index]
    CLIENT.send(f"ARQUIVO {file_name}".encode('utf-8'))

    # Recebe os metadados
    metadados = CLIENT.recv(BUFFER_SIZE).decode('utf-8')
    resp_name, resp_size, resp_pckg, resp_hash = metadados.split(";")
    print_metadata(metadados)

    file_name = resp_name.split(":")[1]
    file_size = int(resp_size.split(":")[1])
    file_packages = int(resp_pckg.split(":")[1])
    file_hash = resp_hash.split(":")[1]

    # Pede confirmacao para o usuario
    confirm = input("Deseja baixar o arquivo? (s/n) ")
    if confirm.strip().lower() != "s":
        print("Download cancelado.")
        CLIENT.send("NOK".encode('utf-8'))
        return
    # Envia a confirmação
    CLIENT.send("OK".encode('utf-8'))

    # Recebe os dados do arquivo em pacotes
    received_data = b""
    while len(received_data) < file_size:
        packet = CLIENT.recv(BUFFER_SIZE)
        if not packet:
            break
        received_data += packet
        progress_bar((len(received_data) / file_size) * 100)

    # Verifica o hash
    if check_hash(received_data, file_hash):
        with open("client files/" + file_name, "wb") as f:
            f.write(received_data)
        print("Arquivo recebido e verificado com sucesso.")
    else:
        print("Erro na verificação do arquivo.")

    # Recebe o status final
    status = CLIENT.recv(BUFFER_SIZE).decode('utf-8').split(":")[1]
    print(f"Status: {status}")

def chat():
    CLIENT.send("CHAT".encode('utf-8'))
    chat_message = CLIENT.recv(BUFFER_SIZE)
    print(f"Mensagem do servidor: {chat_message.decode('utf-8')}")

def connect():
    global IS_CONNECTED
    if IS_CONNECTED:
        print(f"[{TCP_IP}:{TCP_PORT}] Você já está conectado.")
        return
    try:
        CLIENT.connect((TCP_IP, TCP_PORT))
        IS_CONNECTED = True
        response = CLIENT.recv(BUFFER_SIZE)
        print(response.decode())
    except socket.error as e:
        print(f"[{TCP_IP}:{TCP_PORT}] Erro ao conectar ao servidor {e}")

def main():
    while True:
        option = menu()

        if option == "1":
            archive()
        elif option == "2":
            chat()
        elif option == "3":
            menu_config()
        elif option == "4":
            connect()
        elif option == "5":
            CLIENT.send("SAIR".encode('utf-8'))
            break
        else:
            print("Opção inválida. Tente novamente.")
        input("Pressione qualquer tecla para continuar...")
    CLIENT.close()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()