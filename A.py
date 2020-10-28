# Python TCP Client A
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
    my_print('[Client] Connecting to %s port %s' % server_address)
    sock.connect(server_address)

    operating_mode = "-"
    k3 = '1234567887654321'
    iv_k3 = b'3109104011810292'
    choice = ""
    choices = ["0", "1"]
    while choice not in choices:
        my_print("Please enter your choice [0 for CBC | 1 for CFB ]")
        choice = input()

    if choice == "0":
        operating_mode = "CBC"
    elif choice == "1":
        operating_mode = "CFB"

    sock.sendall(choice.encode())

    json_k1_iv = sock.recv(1024)

    recv_k1 = json.loads(json_k1_iv)["k1"]
    recv_iv = json.loads(json_k1_iv)["iv"]

    # decriptare recv_k1 folosind k3
    # decriptare recv_iv folosind k3

    my_print("\nOperating mode:", operating_mode)
    my_print("\nReceived k1:", recv_k1)
    my_print("\nReceived iv:", recv_iv)

    message = "K1 and IV received."
    sock.sendall(message.encode())

    response = sock.recv(1024).decode()
    my_print(response)

    sock.close()


if __name__ == "__main__":
    main()