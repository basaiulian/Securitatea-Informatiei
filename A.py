import pickle
import sys
import socket
from MyCrypto import MyCrypto


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
    k3 = '3112938275822331'
    iv_k3 = b'8190271284791861'
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

    received = sock.recv(1024)

    received_data = pickle.loads(received)
    received_k1 = received_data[1]
    received_iv_k1 = received_data[2]

    k1_decrypted, iv_k1_decrypted = '', ''

    if operating_mode == "CBC":
        k1_decrypted = MyCrypto.cbc_decrypt([received_k1], k3, iv_k3)
        iv_k1_decrypted = MyCrypto.cbc_decrypt([received_iv_k1], k3, iv_k3)

        #message = "[A] k1 and iv received."
        #encrypted_message = MyCrypto.cbc_encrypt([message], k1_decrypted, iv_k1_decrypted)
    else:
        k1_decrypted = MyCrypto.cfb_decrypt([received_k1], k3, iv_k3)
        iv_k1_decrypted = MyCrypto.cfb_decrypt([received_iv_k1], k3, iv_k3)

        #message = "[A] k1 and iv received."
        #encrypted_message = MyCrypto.cfb_encrypt([message], k1_decrypted, iv_k1_decrypted)

    my_print("\nk1:", k1_decrypted)
    my_print("\nk1_iv:", iv_k1_decrypted)

    #sock.sendall(encrypted_message)
    #response = sock.recv(256).decode()
    #my_print(response)

    sock.close()


if __name__ == "__main__":
    main()