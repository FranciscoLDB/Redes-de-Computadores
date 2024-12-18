import socket
import hashlib
import os
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1028  # Tamanho do buffer
FILENAME = ""  # Nome do arquivo a ser requisitado
END_OF_FILE = b"EOF"  # Sinal de término
FILE_NOT_FOUND = b"FNF" # Sinal de arquivo não encontrado
CHUNKS = b"CHN" # Sinal de chunks
TIME_OUT = 5  # Tempo limite de espera
fileslist = ["elements.txt", "porcentagem.txt", "img.png", "notfound.txt"]
total_chunks = 0

def calculate_checksum(data):
    return hashlib.md5(data).hexdigest()

def save_file(filename, chunks_received):
    os.makedirs("./files received", exist_ok=True)
    try:
        with open(f"./files received/recebido_{filename}", 'wb') as f:
            for chunk_number in sorted(chunks_received.keys()):
                f.write(chunks_received[chunk_number])
    except Exception as e:
        print(f"Erro ao abrir ou escrever no arquivo: {e}")
    print(f"Arquivo {filename} salvo como ./files received/recebido_{filename}")

def verify_checksum(chunks_received):
    for chunk_number, data in chunks_received.items():
        checksum = calculate_checksum(data)
        print(f"Chunk {chunk_number}: {checksum}")

def discard_chunks(chunks_received):
    chunk_number = int(input("Digite o número do chunk a ser descartado: "))
    if chunk_number in chunks_received:
        del chunks_received[chunk_number]
        print(f"Chunk {chunk_number} descartado")
    else:
        print(f"Chunk {chunk_number} não encontrado")

def resend_chunks(sock, chunks_received, filename):
    chunk_number = int(input("Digite o número do chunk a ser reenviado [-1 para reenviar todos]: "))
    if chunk_number == -1:
        request = f"GET /{filename} ALL"
        sock.sendto(request.encode(), (UDP_IP, UDP_PORT))
        print(f"Requisição enviada para {UDP_IP}:{UDP_PORT}")
        sock.settimeout(TIME_OUT)
        try:
            signalChunk, addr = sock.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            print("Tempo limite de espera excedido.")
            input("Pressione qualquer tecla para continuar...")
            return chunks_received
        if signalChunk[:3] != CHUNKS:
            print("Sinal de chunks não recebido")
            input("Pressione qualquer tecla para continuar...")
            return chunks_received
        
        global total_chunks
        total_chunks = int(signalChunk[3:].decode())
        print(f"Total de chunks a serem recebidos: {total_chunks}")
        return receive_file(sock, filename, chunks_received)
    elif chunk_number in find_lost_chunks(chunks_received):
        request = f"GET /{filename} CHUNKS /{chunk_number}"
        sock.sendto(request.encode(), (UDP_IP, UDP_PORT))
        print(f"Requisição enviada para {UDP_IP}:{UDP_PORT}")
        return receive_file(sock, filename)    
    else:
        print(f"Chunk {chunk_number} não encontrado")
        return chunks_received

def find_lost_chunks(chunks_received):
    return [i for i in range(total_chunks) if i not in chunks_received]

def receive_file(sock, filename, chunks_received = {}):
    while True:
        
        sock.settimeout(TIME_OUT)
        try:
            checksum, addr = sock.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            print("Tempo limite de espera excedido.")
            break
        
        if checksum == END_OF_FILE:
            print("Recepção do arquivo concluída.")
            break

        try:
            numbered_chunk, addr = sock.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            print("Tempo limite de espera excedido.")
            break

        chunk_number = int(numbered_chunk[:4])
        data = numbered_chunk[4:]
        print(f"Recebido chunk número {chunk_number} de {addr}")

        if calculate_checksum(data) == checksum.decode():
            chunks_received[chunk_number] = data
        else:
            print("Erro de checksum, dados corrompidos")
    input("Pressione qualquer tecla para continuar...")
    return chunks_received

def get_file(sock, filename):
    request = f"GET /{filename} ALL"
    sock.sendto(request.encode(), (UDP_IP, UDP_PORT))
    print(f"Requisição enviada para {UDP_IP}:{UDP_PORT}")
    sock.settimeout(TIME_OUT)
    try:
        signalChunk, addr = sock.recvfrom(BUFFER_SIZE)
    except socket.timeout:
        print("Tempo limite de espera excedido.")
        input("Pressione qualquer tecla para continuar...")
        return
    
    if signalChunk[:3] == FILE_NOT_FOUND:
        print(f"Arquivo {filename} não encontrado.")
        input("Pressione qualquer tecla para continuar...")
        return
    elif signalChunk[:3] != CHUNKS:
        print("Sinal de chunks não recebido")
        input("Pressione qualquer tecla para continuar...")
        return
    
    global total_chunks
    total_chunks = int(signalChunk[3:].decode())
    print(f"Total de chunks a serem recebidos: {total_chunks}")

    chunks_received = receive_file(sock, filename)

    if not chunks_received:
        print("Nenhum chunk recebido")
        input("Pressione qualquer tecla para continuar...")
        return
    elif len(chunks_received) != total_chunks:
        print(f"Chunks recebidos: {len(chunks_received)}")
        print(f"Chunks faltantes: {total_chunks - len(chunks_received)}")
        input("Pressione qualquer tecla para continuar...")
    
    while True:
        option = menu_file(chunks_received)
        if option == "1":
            save_file(filename, chunks_received)
        elif option == "2":
            verify_checksum(chunks_received)
        elif option == "3":
            discard_chunks(chunks_received)
        elif option == "4":
            chunks_received = resend_chunks(sock, chunks_received, filename)
        elif option == "5":
            break
        else:
            print("Opção inválida. Tente novamente.")
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
    print("=" + " " * 2 + f"4 - Time out [{TIME_OUT}s]" + " " * (23 - len(str(TIME_OUT)) - len("Time out [s]")) + "=")
    print("=" + " " * 2 + "5 - Voltar" + " " * 17 + "=")
    print("=-" * 15 + "=")
    return input("Escolha uma opção: ")

def menu_file(chunks_received):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=-" * 15 + "=")
    print(f"Chunks recebidos: [{', '.join(map(str, sorted(chunks_received.keys())))}]")
    print(f"\nChunks faltantes: {find_lost_chunks(chunks_received)}")
    print("=-" * 15 + "=")
    print("=" + " " * 2 + "Menu de opções:" + " " * 12 + "=")
    print("=" + " " * 2 + "1 - Salvar arquivo" + " " * 8 + "=")
    print("=" + " " * 2 + "2 - Verificar checksum" + " " * 6 + "=")
    print("=" + " " * 2 + "3 - Descartar chunks" + " " * 1 + "=")
    print("=" + " " * 2 + "4 - Reenviar chunks" + " " * 8 + "=")
    print("=" + " " * 2 + "5 - Sair" + " " * 19 + "=")
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
                TIME_OUT = int(input("Digite o novo tempo limite de espera: "))
            elif option == "5":
                break
            else:
                print("Opção inválida. Tente novamente.")
        pass
    elif option == "3":
        break
    else:
        print("Opção inválida. Tente novamente.")
    