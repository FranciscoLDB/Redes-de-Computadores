import socket
import hashlib
import os

IP = "127.0.0.1"
PORT = 5002
BUFFER_SIZE = 1024

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))

    # Recebe a mensagem de boas-vindas do servidor
    response = client.recv(BUFFER_SIZE)
    print(response.decode())

    while True:
        print("\nMenu:")
        print("1. Sair")
        print("2. Arquivo")
        print("3. Chat")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            client.send("SAIR".encode('utf-8'))
            break
        elif choice == "2":
            client.send("ARQUIVO".encode('utf-8'))
            file_data = client.recv(BUFFER_SIZE)
            file_hash = client.recv(BUFFER_SIZE)

            # Verifica o hash
            received_hash = hashlib.md5(file_data).hexdigest()
            if received_hash == file_hash.decode('utf-8'):
                with open("received_file", "wb") as f:
                    f.write(file_data)
                print("Arquivo recebido e verificado com sucesso.")
            else:
                print("Erro na verificação do arquivo.")
        elif choice == "3":
            client.send("CHAT".encode('utf-8'))
            chat_message = client.recv(BUFFER_SIZE)
            print(f"Mensagem do servidor: {chat_message.decode('utf-8')}")
        else:
            print("Opção inválida. Tente novamente.")

    # Fecha a conexão
    client.close()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()