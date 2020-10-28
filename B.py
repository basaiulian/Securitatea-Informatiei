# Python TCP Client B
import sys
import socket
import json


def my_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def read_file(filepath):
    file_handler = open(filepath, 'r')
    while True:
        line = file_handler.readline()
        if not line:
            break
        print(line)


def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8000)
    my_print('\nConnecting to %s port %s' % server_address)
    sock.connect(server_address)

    my_print('\nA is choosing his operating mode')

    k3 = '1234567887654321'
    iv_k3 = b'3109104011810292'
    json_operating_mode = sock.recv(1024)

    recv_operating_mode = json.loads(json_operating_mode)["operating_mode"]
    my_print("\nReceived operating mode:", recv_operating_mode)

    message = "Operating mode received."
    sock.sendall(message.encode())

    json_k2_iv = sock.recv(1024)
    recv_k2 = json.loads(json_k2_iv)["k2"]
    recv_iv = json.loads(json_k2_iv)["iv"]

    my_print("\nReceived k2:", recv_k2)
    my_print("\nReceived iv:", recv_iv)

    message = "K2 and IV received."
    sock.sendall(message.encode())

    response = sock.recv(1024).decode()
    my_print(response)

    sock.close()


if __name__ == "__main__":
    main()