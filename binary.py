import numpy as np

class binary:
    @staticmethod
    def msgtobinary(msg):
        if type(msg) == str:
            result = ''.join([format(ord(i), "08b") for i in msg])
        
        elif type(msg) == bytes or type(msg) == np.ndarray:
            result = [format(i, "08b") for i in msg]
        
        elif type(msg) == int or type(msg) == np.uint8:
            result = format(msg, "08b")
        
        else:
            raise TypeError("Input type is not supported in this function")
        
        return result
    #RC4
    @staticmethod
    def BinaryToDecimal(binary):
        return int(binary, 2)
    
    @staticmethod
    def KSA(key):
        key_length = len(key)
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % key_length]) % 256
            S[i], S[j] = S[j], S[i]
        return S

    @staticmethod
    def PRGA(S, n):
        i = 0
        j = 0
        key = []
        while n > 0:
            n -= 1
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            K = S[(S[i] + S[j]) % 256]
            key.append(K)
        return key

    @staticmethod
    def preparing_key_array(s):
        return [ord(c) for c in s]

    @staticmethod
    def rc4_encrypt(plaintext,key):
        key = binary.preparing_key_array(key)

        S = binary.KSA(key)
        keystream = np.array(binary.PRGA(S, len(plaintext)))
        plaintext = np.array([ord(i) for i in plaintext])

        cipher = keystream ^ plaintext
        ctext = ''.join(chr(c) for c in cipher)
        return ctext

    @staticmethod
    def rc4_decrypt(ciphertext,key):
        key = binary.preparing_key_array(key)

        S = binary.KSA(key)
        keystream = np.array(binary.PRGA(S, len(ciphertext)))
        ciphertext = np.array([ord(i) for i in ciphertext])

        decoded = keystream ^ ciphertext
        dtext = ''.join(chr(c) for c in decoded)
        return dtext
    # 1. Mã hóa Vigenère Cipher

    @staticmethod
    def vigenere_encrypt(text, key):
        result = ""
        key_index = 0
        for char in text:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                key_char = key[key_index % len(key)].lower()
                shift = ord(key_char) - 97
                result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
                key_index += 1
            else:
                result += char
        return result
    @staticmethod
    def vigenere_decrypt(text, key):
        result = ""
        key_index = 0
        for char in text:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                key_char = key[key_index % len(key)].lower()
                shift = ord(key_char) - 97
                result += chr((ord(char) - shift_base - shift) % 26 + shift_base)
                key_index += 1
            else:
                result += char
        return result

    # 3. Mã hóa XOR Cipher
    @staticmethod
    def xor_cipher(text, key):
        result = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))
        return result
