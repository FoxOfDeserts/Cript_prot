import random
import socket
import json
from STRIBOG import gost_256_512
from SHA import sha_256_512
from RSA import prime_num


my_name = "Alice"
user_id = 7777

users = {"Bob": 7778}

amount_passwords = 40
iteration = 1


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

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(("localhost", 7000))

    for block in package_blocks:
        client_sock.sendall(block)
        data = client_sock.recv(1024)
        if data.decode() == str(len(package_blocks) - 1):
            client_sock.sendall(b"DataPut")
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                result += data
    client_sock.close()

    return result


def generation_passwords(amount_passwords_: int):
    prime = prime_num(1024)
    secret_key = prime.to_bytes(byteorder="big", length=128)
    passwords_ = {'0': secret_key}

    for i in range(1, amount_passwords_ + 1):
        passwords_[f'{i}'] = sha_256_512(passwords_[f'{i - 1}'], 512)

    passwords_ = {f'{id_}': item_.hex() for id_, item_ in passwords_.items()}

    return passwords_

print("lab14")

print(f"Host Id: {user_id}")
print(f"Host Name: {my_name}")

passwords = generation_passwords(amount_passwords_=amount_passwords)
final_password = {"Final": passwords[f'{amount_passwords}']}

print(f"Passwords generated.")
client(final_password)

letter = {"Id": user_id, "Iteration": "", "Password": ""}

while True:
    choose = input(f"\nSend password to Bob? Y/N?: ")
    if choose.lower() == "y":
        print(f"Iteration: {iteration}")

        letter["Iteration"] = iteration
        letter["Password"] = passwords[f'{amount_passwords - iteration}']

        print(f"Submitted password: {letter['Password']}")

        answer = client(letter)

        if answer == b"AuthenticationPassed":
            iteration += 1
            print(f"Authentication passed.")
        elif answer == b"AuthenticationFailed":
            print(f"Authentication failed.")
            break

    elif choose.lower() == "n":
        print(f"Session ended.")
        break
    else:
        print(f"Incorrect input.")