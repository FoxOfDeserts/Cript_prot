import random
import logging
import socket
import json
import STRIBOG
import SHA
import RSA
from datetime import datetime
import math

def keys(size):
    keys = RSA.RSA.key_gen(size)
    print(keys)
    with open("public_key.json", "w") as file:
        json.dump(keys[0], file)
    with open("privat_key.json", "w") as file:
        json.dump(keys[1], file)

def gen_signature(msg: bytes, hash_, pub_key: dict, sec_key: dict, size_: int = 256):
    try:
        hash_msg, hash_name = hash_(msg, size_)
        hash_type = hash_name + str(size_)
    except Exception:
        raise ValueError("Incorrect hash object")
    print(f"Signature in progress.")
    try:
        user_signature = RSA.RSA.encrypt(pub_key, hash_msg)
    except ValueError:
        logging.exception("SignatureError")

    else:
        time_mark = str(datetime.now())[2:-7].replace(" ", "-").replace(":", "-")
        sign_dict = RSA.RSA.PKCS_7_CAdES(msg.hex(), user_signature.hex(),
                                       hash_type, pub_key, time_mark)

        return sign_dict

def welcome():
    print(f"Host Id: {my_user_id}")
    print(f"Host Name: {my_name}\n")

def fragmentation(data_to_send):
    if type(data_to_send) is dict:
        return [json.dumps(data_to_send).encode()[x:x + 1024] for x in
                range(0, len(json.dumps(data_to_send).encode()), 1024)]
    elif type(data_to_send) is bytes:
        return [data_to_send[x:x + 1024] for x in
                range(0, len(data_to_send), 1024)]

def client(data_to_send: dict or bytes):
    result = b""
    package_blocks = fragmentation(data_to_send)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect(("localhost", 1205))
        for block in package_blocks:
            s.sendall(block)
            data = s.recv(1024)
            if data.decode() == str(len(package_blocks) - 1):
                s.sendall(b"DataPut")
                while True:
                    data = s.recv(1024)
                    if not data:
                        break
                    result += data


    return result

def new_signature(recipient_id: int, session_key_: bytes, time_mark_: str):
    body_signature = {"RecipientId": recipient_id, "SessionKey": session_key_.hex(), "TimeMark": time_mark_}
    body_signature = json.dumps(body_signature).encode()
    pub_signature_key = json.load(open("public_key.json", "r", encoding='utf-8'))
    sec_signature_key = json.load(open("privat_key.json", "r", encoding='utf-8'))
    signature_ = gen_signature(body_signature, SHA.sha_256_512, pub_key=pub_signature_key, sec_key=sec_signature_key)
    return signature_


my_name = "Alice"
my_user_id = 7150

users = {"Bob": 1488}
keys(128)
welcome()

session_key = RSA.prime_num(256).to_bytes(32, "big")
print(f"Session key generated: {session_key.hex()}")

time_mark = str(datetime.now())[2:-7].replace(" ", "-").replace(":", "-")
print(f"Time mark generated: {time_mark}")

recipient_ID = users["Bob"]
signature = new_signature(recipient_id=recipient_ID, session_key_=session_key, time_mark_=time_mark)

body_encrypt = {"SessionKey": session_key.hex(), "TimeMark": time_mark, "Signature": signature}
body_encrypt = json.dumps(body_encrypt).encode()

pub_encrypt_key = json.load(open("public_key.json", "r", encoding='utf-8'))
sec_encrypt_key = json.load(open("privat_key.json", "r", encoding='utf-8'))

encrypted_session_key = RSA.RSA.encrypt(pub_encrypt_key, body_encrypt)

print(f"Session key encrypted: {encrypted_session_key.hex()}")

letter = {"EncryptedSessionKey": encrypted_session_key.hex()}
print(f'Session key sent.')
answer = client(letter)
print(f'Session key received.')
if answer == b"Correct":
    print(f'Session key is correct.')
elif answer == b"Incorrect":
    print(f'Session key is incorrect.')
else:
    print(f'Session key is not received: {answer}.')
