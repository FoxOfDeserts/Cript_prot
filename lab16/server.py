import random
import socket
import json
import STRIBOG
import SHA
import RSA
from datetime import datetime
import math

my_name = "Bob"
my_user_id = 1488
users = {"Alice": 7150}
lab_name = "lab16"

sec_encrypt_key = json.load(open("privat_key.json", "r", encoding='utf-8'))


def welcome():
    print(f"Host Id: {my_user_id}")
    print(f"Host Name: {my_name}\n")


welcome()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as serv_sock:
    serv_sock.bind(("localhost", 1205))
    print(f"Socket info: {serv_sock}")
    serv_sock.listen(1)

    while True:
        client_sock, client_addr = serv_sock.accept()
        print(f'Connected with: {client_addr}.')
        result = b""
        count = 0
        while True:
            data = client_sock.recv(1024)
            if data == b"DataPut":
                try:
                    letter = json.loads(result.decode())
                    assert type(letter) is dict
                    if "EncryptedSessionKey" in letter.keys():
                        print(f'Session key received.')
                        encrypted_session_key = bytes.fromhex(letter["EncryptedSessionKey"])
                        decrypted_session_key = RSA.RSA.decrypt(sec_encrypt_key, encrypted_session_key)
                        decrypted_session_key = json.loads(decrypted_session_key)
                        print(f"Process signature verification.")
                        signature_value = decrypted_session_key["Signature"]["SignerInfos"]["SignatureValue"]
                        public_signature_key = decrypted_session_key["Signature"]["CertificateSet"]

                        hash_into_signature = RSA.RSA.decrypt(sec_key=public_signature_key,
                                                            encrypted_msg=bytes.fromhex(signature_value), mode=1)

                        body_signature = {"RecipientId": my_user_id, "SessionKey": decrypted_session_key["SessionKey"],
                                          "TimeMark": decrypted_session_key["TimeMark"]}
                        body_signature = json.dumps(body_signature).encode()

                        body_signature = SHA.sha_256_512(body_signature, 256)

                        if body_signature.hex() == hash_into_signature.hex():
                            print(f'Session key: {decrypted_session_key["SessionKey"]}.')
                            print(f'Session key is correct.')
                            client_sock.sendall(b"Correct")
                        else:
                            print(f'Session key: {decrypted_session_key["SessionKey"]}.')
                            print(f'Session key is incorrect.')
                            client_sock.sendall(b"Incorrect")

                except Exception as err:
                    print(f'{err}')
                    client_sock.sendall(b"DataError")

                break
            result += data
            client_sock.sendall(str(count).encode())
            count += 1
        print(f"Close connection with: {client_addr}.\n")
