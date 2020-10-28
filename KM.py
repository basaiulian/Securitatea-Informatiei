import socket
import sys
import json


def my_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():

    # Creating TCP socket family:
    # Address Format Internet
    # Type: Socket Stream(sequenced, reliable, two-way connection-based byte streams over TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 8000)
    my_print('[Server] Starting up on %s port %s' % server_address)

    sock.bind(server_address)

    sock.listen(2)

    while True:
        my_print('\n[Server] Waiting for A\'s connection\n')
        connection1, client_address1 = sock.accept()

        my_print('\n[Server] Waiting for B\'s connection\n')
        connection2, client_address2 = sock.accept()

        try:
            my_print('[Server] Connection from', client_address1)
            my_print('[Server] Connection from', client_address2)

            k3 = "-"  # citita dintr un fisier?
            operating_mode_A, operating_mode_B = "-", "-"

            choice = connection1.recv(256).decode()


            if choice == "0":
                my_print("A => CBC")
                my_print("B => CFB")
                operating_mode_A = "CBC"
                operating_mode_B = "CFB"
            elif choice == "1":
                my_print("A => CFB")
                my_print("B => CBC")
                operating_mode_A = "CFB"
                operating_mode_B = "CBC"

            k1 = "CRIPTAT_K1_CRIPTAT"
            iv = "CRIPTAT_IV_CRIPTAT"
            k1_iv = {"k1": k1, "iv": iv}
            json_k1_iv = json.dumps(k1_iv)
            connection1.sendall(json_k1_iv.encode())

            operating_mode = {"operating_mode": operating_mode_B}
            json_operating_mode = json.dumps(operating_mode)
            connection2.sendall(json_operating_mode.encode())

            recv_message = connection2.recv(256)
            my_print(recv_message.decode())

            k2 = "CRIPTAT_K2_CRIPTAT"
            iv = "CRIPTAT_IV_CRIPTAT"
            k2_iv = {"k2": k2, "iv": iv}
            json_k2_iv = json.dumps(k2_iv)
            connection2.sendall(json_k2_iv.encode())

            # le primesc si le afisez ( DAR TREBUIESC DECRIPTATE CU K1 si K2 )
            my_print(connection1.recv(1024).decode())
            my_print(connection2.recv(1024).decode())

            connection1.sendall("Communication started!".encode())
            connection2.sendall("Communication started!".encode())




        finally:
            connection1.close()
            my_print('[Server] Connection ended')

if __name__ == "__main__":
    main()