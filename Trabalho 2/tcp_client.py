# cliente_tcp.py
import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))

    response = client.recv(4096)
    print(response.decode())

if __name__ == "__main__":
    main()