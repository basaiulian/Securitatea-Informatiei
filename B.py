# Python TCP Client B
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
    my_print('\nConnecting to %s port %s' % server_address)
    sock.connect(server_address)

    my_print('\nA is choosing his operating mode')

    k3 = '3112938275822331'
    iv_k3 = b'8190271284791861'
    received = sock.recv(1024)

    received_data = pickle.loads(received)
    received_operating_mode = received_data[0]
    my_print("\nReceived operating mode:", received_operating_mode)

    message = "[B] Operating mode received."
    sock.sendall(message.encode())

    received = sock.recv(1024)
    received_data = pickle.loads(received)
    received_k2, received_k2_iv = received_data[0], received_data[1]

    #my_print("\nReceived k2:", received_k2)
    #my_print("\nReceived iv:", received_k2_iv)

    if received_operating_mode == "CBC":
        k2_decrypted = MyCrypto.cbc_decrypt([received_k2], k3, iv_k3)
        iv_k2_decrypted = MyCrypto.cbc_decrypt([received_k2_iv], k3, iv_k3)

        #message = "[B] k2 and iv received."
        #encrypted_message = MyCrypto.cbc_encrypt([message], k2_decrypted, iv_k2_decrypted)
    else:
        k2_decrypted = MyCrypto.cfb_decrypt([received_k2], k3, iv_k3)
        iv_k2_decrypted = MyCrypto.cfb_decrypt([received_k2_iv], k3, iv_k3)

        #message = "[B] k2 and iv received."
        #encrypted_message = MyCrypto.cfb_encrypt([message], k2_decrypted, iv_k2_decrypted)

    my_print("\nk2:", k2_decrypted)
    my_print("\niv:", iv_k2_decrypted)

    #sock.sendall(encrypted_message)
    #response = sock.recv(256).decode()
    #my_print(response)

    sock.close()


if __name__ == "__main__":
    main()