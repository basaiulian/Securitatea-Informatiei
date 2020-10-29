import pickle
import socket
import sys
from MyCrypto import MyCrypto


def my_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


k3 = '3112938275822331'
iv_k3 = b'8190271284791861'

k2 = '5555666622221111'
iv_k2 = b'1249097129147980'

k1 = '1112223334445551'
iv_k1 = b'3910571928794213'


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

            operating_mode_a, operating_mode_b, encrypted_k1, encrypted_iv_k1, encrypted_k2, encrypted_iv_k2 = "-", "-", "-", "-", "-", "-"

            choice = connection1.recv(256).decode()

            if choice == "0":
                operating_mode_a = "CBC"
                operating_mode_b = "CFB"

                encrypted_k1 = MyCrypto.cbc_encrypt(k1, k3, iv_k3)[0]
                encrypted_iv_k1 = MyCrypto.cbc_encrypt(iv_k1, k3, iv_k3)[0]

                encrypted_k2 = MyCrypto.cfb_encrypt(k2, k3, iv_k3)[0]
                encrypted_iv_k2 = MyCrypto.cfb_encrypt(iv_k2, k3, iv_k3)[0]
            elif choice == "1":
                operating_mode_a = "CFB"
                operating_mode_b = "CBC"

                encrypted_k1 = MyCrypto.cfb_encrypt(k1, k3, iv_k3)[0]
                encrypted_iv_k1 = MyCrypto.cfb_encrypt(iv_k1, k3, iv_k3)[0]

                encrypted_k2 = MyCrypto.cbc_encrypt(k2, k3, iv_k3)[0]
                encrypted_iv_k2 = MyCrypto.cbc_encrypt(iv_k2, k3, iv_k3)[0]


            # sending operating mode, k1 and iv for A
            response = pickle.dumps([operating_mode_a, encrypted_k1, encrypted_iv_k1])
            connection1.sendall(response)

            # sending operating mode for B
            response = pickle.dumps([operating_mode_b])
            connection2.sendall(response)

            # receiving confirmation message from B
            received = connection2.recv(256)
            my_print(received.decode())

            # sending k2 and iv to B
            response = pickle.dumps([encrypted_k2, encrypted_iv_k2])
            connection2.sendall(response)

            response_a = connection1.recv(1024)
            response_a_to_decrypt = pickle.loads(response_a)
            response_b = connection2.recv(1024)
            response_b_to_decrypt = pickle.loads(response_b)

            # my_print(response_b_to_decrypt)
            # my_print(response_a_to_decrypt)

            decrypted_response_a, decrypted_response_b = '', ''

            # A => CBC
            # B => CFB
            if choice == "0":
                decrypted_response_a = MyCrypto.cbc_decrypt([response_a_to_decrypt], k1, iv_k1)
                decrypted_response_b = MyCrypto.cfb_decrypt([response_b_to_decrypt], k2, iv_k2)

            # A => CFB
            # B => CBC
            elif choice == "1":
                decrypted_response_a = MyCrypto.cfb_decrypt([response_a_to_decrypt], k1, iv_k1)
                decrypted_response_b = MyCrypto.cbc_decrypt([response_b_to_decrypt], k2, iv_k2)

            my_print(decrypted_response_a)
            my_print(decrypted_response_b)

            my_print("Starting communication")
            connection1.sendall("Communication started!".encode())
            connection2.sendall("Communication started!".encode())

            message_from_a_file = connection1.recv(1024000)
            message_from_a_file = pickle.loads(message_from_a_file)

            if choice == "0":
                decrypted_blocks_number = MyCrypto.cbc_decrypt(message_from_a_file[0], k1, iv_k1)
                decrypted_message = MyCrypto.cbc_decrypt(message_from_a_file[1], k1, iv_k1)

                encrypted_message_for_b = MyCrypto.cfb_encrypt(decrypted_message, k2, iv_k2)
                #print(encrypted_message_for_b)
                response = pickle.dumps([decrypted_blocks_number, encrypted_message_for_b])
            elif choice == "1":
                decrypted_blocks_number = MyCrypto.cfb_decrypt(message_from_a_file[0], k1, iv_k1)
                decrypted_message = MyCrypto.cfb_decrypt(message_from_a_file[1], k1, iv_k1)

                encrypted_message_for_b = MyCrypto.cbc_encrypt(decrypted_message, k2, iv_k2)
                #print(encrypted_message_for_b)
                response = pickle.dumps([decrypted_blocks_number, encrypted_message_for_b])

            #print("Decrypted from A: ", decrypted_message)

            # sending to B
            connection2.sendall(response)

            # receiving response from B to be sent to A

            response_b = connection2.recv(1024)
            response_b_to_decrypt = pickle.loads(response_b)

            if choice == "0":
                decrypted_response_b = MyCrypto.cfb_decrypt([response_b_to_decrypt], k2, iv_k2)
                encrypted_message_for_a = MyCrypto.cbc_encrypt(decrypted_response_b, k1, iv_k1)[0]
            elif choice == "1":
                decrypted_response_b = MyCrypto.cbc_decrypt([response_b_to_decrypt], k2, iv_k2)
                encrypted_message_for_a = MyCrypto.cfb_encrypt(decrypted_response_b, k1, iv_k1)[0]

            response = pickle.dumps([encrypted_message_for_a])
            connection1.sendall(response)


        finally:
            connection1.close()
            my_print('[Server] Connection ended')


if __name__ == "__main__":
    main()
