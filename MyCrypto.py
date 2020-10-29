from Crypto.Cipher import AES


class MyCrypto:
    iv_block = b'5678242345334569'

    @staticmethod
    def fill_string(string, fill_value, size):
        while len(string) < size:
            string += fill_value
        return string

    @staticmethod
    def xor(string1, string2):
        if type(string1) == str:
            string1 = bytearray(string1.encode())
        if type(string2) == str:
            string2 = bytearray(string2.encode())
        result = bytearray()
        for char1, char2 in zip(string1, string2):
            result.append(char1 ^ char2)
        return result

    @staticmethod
    def cbc_encrypt(text, key, iv):

        first, last = 0, 16

        # input
        key = bytearray(key.encode())
        intermediary = iv

        # output
        encrypted_blocks = []

        # creating AES object with key, CBC mode and iv
        encryptor = AES.new(key, AES.MODE_CBC, MyCrypto.iv_block)

        # filling the string if its length is less than 16 ( 128 bits )
        if len(text) < 16:
            text = MyCrypto.fill_string(text, ' ', 16)

        while first < len(text):
            # taking current block from text
            plain_text_block = text[first:last]

            # filling blocks with length less than 16 ( 128 bits )
            if len(plain_text_block) < 16:
                plain_text_block = MyCrypto.fill_string(plain_text_block, ' ', 16)

            # encoding intermediary if it is string
            if type(intermediary) == str:
                intermediary = intermediary.encode('utf8')

            # XOR operation between current block and intermediary ( IV or last block )
            intermediary = bytes(intermediary)
            current_xor = MyCrypto.xor(plain_text_block, intermediary)

            # encrypting using AES and appending encrypted cipher to blocks
            encrypted_block_cipher = encryptor.encrypt(current_xor)
            encrypted_blocks.append(encrypted_block_cipher)

            # preparing variables for the next iteration
            # by choosing the next intermediary
            # and setting first and last for the next block
            intermediary = encrypted_block_cipher
            first = last
            last = min(last + 16, len(text))

        return encrypted_blocks

    @staticmethod
    def cbc_decrypt(encrypted_blocks, key, iv):

        # input
        key = bytearray(key.encode('utf8'))

        # output
        result = ''

        # creating AES object with key, CBC mode and iv
        decrypter = AES.new(key, AES.MODE_CBC, MyCrypto.iv_block)

        for idx, current_block in enumerate(encrypted_blocks):

            # decrypting every block
            block = decrypter.decrypt(current_block)

            # if it is the first iteration then we should apply XOR operation between iv and current block
            # else we should apply XOR operation between current block and last block
            if idx == 0:
                plain_text_block = MyCrypto.xor(block, iv)
            else:
                plain_text_block = MyCrypto.xor(block, encrypted_blocks[idx - 1])

            # building result
            result += str(plain_text_block.decode('utf8'))
        return result

    @staticmethod
    def cfb_encrypt(text, key, iv):
        """ Order: encrypt iv, xor result with plain text, iv becomes encryption """

        first, last = 0, 16

        # input
        key = bytearray(key.encode('utf8'))
        intermediary = iv

        # output
        encrypted_blocks = []

        # creating AES object with key, CFB mode and iv
        encryptor = AES.new(key, AES.MODE_CFB, MyCrypto.iv_block)

        # filling the string if its length is less than 16 ( 128 bits )
        if len(text) < 16:
            text = MyCrypto.fill_string(text, ' ', 16)

        while first < len(text):
            # taking current block from text
            plain_text_block = text[first:last]

            # filling blocks with length less than 16 ( 128 bits )
            if len(plain_text_block) < 16:
                plain_text_block = MyCrypto.fill_string(plain_text_block, ' ', 16)

            # encoding intermediary if it is string
            if type(intermediary) == str:
                intermediary = intermediary.encode('utf8')
            intermediary = bytearray(intermediary)

            # encrypting intermediary using AES
            encrypted_block_cipher = encryptor.encrypt(intermediary)

            # XOR operation between current block and intermediary ( IV or last block )
            encrypted_block_cipher = MyCrypto.xor(plain_text_block, encrypted_block_cipher)

            # appending encrypted cipher to blocks
            encrypted_blocks.append(bytes(encrypted_block_cipher))

            # preparing variables for the next iteration
            # by choosing the next intermediary
            # and setting first and last for the next block
            intermediary = encrypted_block_cipher
            first = last
            last = min(last + 16, len(text))

        return encrypted_blocks

    @staticmethod
    def cfb_decrypt(encrypted_blocks, key, iv):

        # input
        key = bytearray(key.encode('utf8'))

        # output
        result = ''

        # creating AES object with key, CFB mode and iv
        decrypter = AES.new(key, AES.MODE_CFB, MyCrypto.iv_block)

        for idx, encrypted_block in enumerate(encrypted_blocks):

            # if it is the first iteration then we should apply operation XOR between iv and current block
            # else we should apply XOR operation between current block and last block
            if idx == 0:
                if type(iv) == str:
                    iv = bytes(iv.encode('utf8'))
                aux = decrypter.encrypt(iv)
                plain_text_block = MyCrypto.xor(aux, encrypted_block)
            else:
                aux = decrypter.encrypt(bytes(encrypted_blocks[idx - 1]))
                plain_text_block = MyCrypto.xor(aux, encrypted_block)

            # building result
            result += str(plain_text_block.decode('utf8'))
        return result
