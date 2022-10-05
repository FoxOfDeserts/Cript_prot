import logging
import random
import math
import sympy
import json
import datetime


def prime_num(prime_size):
    while True:
        random_binary_num = [str(round(random.random())) for _ in range(prime_size)]
        random_binary_num[0] = "1"
        random_binary_num[-1] = "1"
        prime_ = int("".join(random_binary_num), 2)
        if sympy.isprime(prime_) is False:
            continue
        else:
            break
    return prime_


def gen_inverse_modulo(mode: int, elem: int):
    return alg_euc(mode, elem)[2]


def alg_euc(x: int, y: int):
    if x < y:
        mp = x
        x = y
        y = mp
    A = [0, 1]
    B = [1, 0]
    nod, a, b = 0, 0, 0
    while y != 0:
        q = x // y
        r = x - q * y
        a = A[1] - q * A[0]
        b = B[1] - q * B[0]
        x = y
        y = r
        A[1] = A[0]
        A[0] = a
        B[1] = B[0]
        B[0] = b
        nod = x
        a = A[1]
        b = B[1]
    return nod, a, b


class RSA:
    def __init__(self):
        self.data = str(datetime.datetime.now())[:-7].replace(":", "-")

    @staticmethod
    def key_gen(key_digit):

        sec_key = {'privateExponent': 0, 'prime1': prime_num(key_digit // 2),
                   'prime2': prime_num(key_digit // 2)}  # [p, q, d]
        public_key = {"publicExponent": 0, "N": sec_key["prime1"] * sec_key["prime2"]}  # [n = p*q, exp]
        phi = (sec_key["prime1"] - 1) * (sec_key["prime2"] - 1)
        while True:
            public_exp = random.randint(1, phi - 1)
            mod, a, privat_exp = alg_euc(phi, public_exp)
            if mod ^ 1 == 0 and ((privat_exp * public_exp) % phi) ^ 1 == 0:
                if privat_exp < 0:
                    privat_exp += phi
                public_key["publicExponent"] = public_exp
                sec_key['privateExponent'] = privat_exp
                break
        return public_key, sec_key

    @staticmethod
    def encrypt(pub_key: dict, bytes_mess: bytes, mode: int = 0):
        if mode == 0:
            __n = pub_key["N"]
            __pub_exp = pub_key["publicExponent"]
        elif mode == 1:
            __n = pub_key["prime1"] * pub_key["prime2"]
            __pub_exp = pub_key['privateExponent']
        else:
            raise ValueError("Incorrect encryption mode")

        _msg_len_bytes = len(bytes_mess)
        _key_byte_len = len(__n.to_bytes(math.ceil(math.log2(__n) / 8), byteorder="big"))

        if _key_byte_len > 2048:
            _key_byte_len = 2048

        _block_len = _key_byte_len - 2
        _pad_bytes_size = math.ceil(math.log(_key_byte_len, 2) / 8)  # Нахожу размерность байтов для паддинга.
        # Округление в большую сторону кратность степени размера блока 8-ке
        # _pad_bytes_size = кратности степени размера блока 8-ке.

        _msg_blocks = [bytes_mess[x:x + _block_len] for x in range(0, _msg_len_bytes, _block_len)]

        for _block_in_msg in range(len(_msg_blocks)):
            _count_pad = (_block_len + 1) - len(_msg_blocks[_block_in_msg])
            _padding_byte = _count_pad.to_bytes(_pad_bytes_size, byteorder="big")

            for _ in range(_count_pad):
                _msg_blocks[_block_in_msg] += _padding_byte

        _encrypted_msg_blocks = [pow(int.from_bytes(_block, byteorder='big'), __pub_exp, __n)
                                 for _block in
                                 _msg_blocks.copy()]

        return b"".join([x.to_bytes(math.ceil(math.log2(x) / 8), byteorder="big") for x in _encrypted_msg_blocks])

    @staticmethod
    def decrypt(sec_key: dict, encrypted_msg: bytes, mode: int = 0):

        if mode == 0:
            __n = sec_key["prime1"] * sec_key["prime2"]
            __sec_exp = sec_key['privateExponent']
        elif mode == 1:
            __n = sec_key["N"]
            __sec_exp = sec_key["publicExponent"]
        else:
            raise ValueError("Incorrect mode")

        _msg_len_bytes = len(encrypted_msg)
        _key_byte_len = len(
            __n.to_bytes(
                math.ceil(math.log2(__n) / 8), byteorder="big"))

        if _key_byte_len > 2048:
            _key_byte_len = 2048

        _block_len = _key_byte_len - 1

        _encrypted_msg_blocks = [int.from_bytes(encrypted_msg[x:x + _key_byte_len], "big") for x in
                                 range(0, _msg_len_bytes, _key_byte_len)]

        _decrypted_msg = [x.to_bytes(_block_len, byteorder="big") for x in
                          [pow(num, __sec_exp, __n) for num in
                           _encrypted_msg_blocks]]

        for _block_in_decrypted in range(len(_decrypted_msg)):
            _byte_check = _decrypted_msg[_block_in_decrypted][-1]
            __checker = 0
            for i in range(len(_decrypted_msg[_block_in_decrypted]) - 1, (_block_len - _byte_check) - 1, -1):
                if _decrypted_msg[_block_in_decrypted][i] == _byte_check:
                    __checker += 1

            if __checker == _byte_check:
                _decrypted_msg[_block_in_decrypted] = _decrypted_msg[_block_in_decrypted][:_block_len - __checker]
            else:
                raise ValueError("Wrong key")
        return b"".join(_decrypted_msg)

    def pkcs_8_12(self, secret_key: list[int], public_key: list[int], date):

        pub_k = {"SubjectPublicKeyInfo": {"publicExponent": public_key[1], "N": public_key[0]},
                 "PKCS10CertRequest": "NULL", "Certificate": "NULL", "PKCS7CertChain-PKCS": "NULL"}

        sec_k = {'privateExponent': secret_key[2], 'prime1': secret_key[0], 'prime2': secret_key[1],
                 'exponent1': secret_key[2] % (secret_key[0] - 1),
                 'exponent2': secret_key[2] % (secret_key[1] - 1),
                 'coefficient': alg_euc(secret_key[0], secret_key[1])[2]}

        file = open(f"results\\PubKey - {date}.json", "w")
        json.dump(pub_k, file, indent=4)
        file.close()

        file = open(f"results\\SecKey - {date}.json", "w")
        json.dump(sec_k, file, indent=4)
        file.close()

    @staticmethod
    def pkcs_7_bytes(encrypted_msg: bytes, date):
        res = {"Version": 0,
               "EncryptedContentInfo":
                   {"ContentType": "text",
                    "ContentEncryptionAlgorithmIdentifier": "rsaEncryption",
                    "encryptedContent": encrypted_msg.hex(),
                    "OPTIONAL": "NULL"}}
        file = open(f"results\\EncMsg - {date}.json", "w")
        json.dump(res, file, indent=4)
        file.close()

    @staticmethod
    def PKCS_7_CAdES(msg, signature, hash_type, pub_key, mark):
        signature_ = {"CMSVersion": "1", "DigestAlgorithmIdentifiers": hash_type,
                      "EncapsulatedContentInfo": {"ContentType": "text", "OCTET STRING": msg},
                      "CertificateSet": pub_key,
                      "RevocationInfoChoises": "NULL",
                      "SignerInfos":
                          {"CMSVersion": "1", "SignerIdentifier": "Цой Георгий",
                           "DigestAlgorithmIdentifier": hash_type,
                           "SignedAttributes": "NULL",
                           "SignatureAlgorithmIdentifier": "RSAdsi",
                           "SignatureValue": signature,
                           "UnsignedAttributes":
                               {"OBJECT IDENTIFIER": "signature-time-stamp",
                                "SET OF AttributeValue":
                                    " "
                                }
                           }
                      }
        # file = open(f"results\\signature {mark}.json", "w", encoding="utf-8")
        # json.dump(signature_, file, indent=4)
        # file.close()
        return signature_

    @staticmethod
    def read_out_file(path: str, mode: str):
        try:
            if mode == "msg":
                with open(path, "r", encoding="utf-8") as file:
                    result = file.read()
            elif mode == "en_msg":
                with open(path, "r", encoding="utf-8") as j_file:
                    result = json.load(j_file)['EncryptedContentInfo']["encryptedContent"]
            elif mode == "pb":
                with open(path, "r", encoding="utf-8") as j_file:
                    res = json.load(j_file)
                    result = [res["SubjectPublicKeyInfo"]["N"], res["SubjectPublicKeyInfo"]["publicExponent"]]
            elif mode == "sc":
                with open(path, "r", encoding="utf-8") as j_file:
                    res = json.load(j_file)
                    result = [res["prime1"], res["prime2"], res["privateExponent"]]
            else:
                raise ValueError("Incorrect mode")
        except Exception as err:
            logging.exception("Error in method read")
            raise err
        else:
            return result