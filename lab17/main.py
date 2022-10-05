import logging
import random

import socket
import json
import os
from Stribog import gost_256_512
from SHA import sha_256_512
from RSA import prime_num, gen_parent_element


lab_name = "lab18"

my_name = "Alice"
user_id = 4932
users = {"Bob": 2605}

amount_passwords = 40
iteration = 1

path_iteration_counter = "source/iteration_counter.json"
json.dump(iteration, open(path_iteration_counter, "w"), indent=4)


def welcome():
    print(f"Host Id: {user_id}")
    print(f"Host Name: {my_name}\n")


def fragmentation(data_to_send):
    if type(data_to_send) is dict:
        return [json.dumps(data_to_send).encode()[x:x + 1024] for x in
                range(0, len(json.dumps(data_to_send).encode()), 1024)]
    elif type(data_to_send) is bytes:
        return [data_to_send[x:x + 1024] for x in
                range(0, len(data_to_send), 1024)]


def client(data_to_send: dict or bytes) -> bytes:
    result = b""
    package_blocks = fragmentation(data_to_send)

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(("localhost", 7568))

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


def generation_passwords(amount_passwords_: int) -> dict:
    prime = prime_num(1024)
    secret_key = prime.to_bytes(byteorder="big", length=128)
    passwords_ = {'0': secret_key}

    for i in range(1, amount_passwords_ + 1):
        passwords_[f'{i}'] = sha_256_512(passwords_[f'{i - 1}'], 512)

    passwords_ = {f'{id_}': item_.hex() for id_, item_ in passwords_.items()}

    return passwords_


def name_find(id_: int):
    if id_ in users.values():
        for user_name, user_id_ in users.items():
            if user_id_ == id_:
                return user_name
    else:
        return None


def authenticator(passwords_: dict):
    iteration_ = json.load(open(path_iteration_counter, "r"))
    letter = {"Id": user_id, "Iteration": iteration_, "Password": passwords_[f'{amount_passwords - iteration_}']}
    answer = client(letter)

    if answer == b"AuthenticationPassed":
        iteration_ += 1
        print(f"Authentication with Bob: Passed.")
        json.dump(iteration, open(path_iteration_counter, "w"), indent=4)
        return True
    elif answer == b"AuthenticationFailed":
        print(f"Authentication with Bob: Failed.")
        return False


def terminal_choice() -> str:
    while True:
        choose = input(f"1. g - Primary element | 2. g - h(w), w - shared password : ")
        if choose == "1":
            return choose
        elif choose == "2":
            return choose
        else:
            print(f"Incorrect input.")


def gen_param_g(prime_mode_: int):
    choice = terminal_choice()
    if choice == "1":
        return gen_parent_element(prime_mode_)
    else:
        hash_from_password = sha_256_512(bytes_msg=bytes.fromhex(passwords[f'{amount_passwords}']), size=512)
        return pow(int.from_bytes(hash_from_password, "big"), 1, prime_mode_)


passwords = generation_passwords(amount_passwords_=amount_passwords)
final_password = {"Final": passwords[f'{amount_passwords}']}
client(final_password)

if authenticator(passwords):
    print(f"Diffie-Hellman protocol started.")

    prime_mode = prime_num(1024)
    param_g = gen_param_g(prime_mode)
    param_x = random.randint(2, prime_mode - 2)
    alpha = pow(param_g, param_x, prime_mode)

    print(f"Prime number generated: {prime_mode}")
    print(f"Value X generated: {param_x}")
    print(f"Value alpha generated: {alpha}")
    print(f"Alpha sent.")

    answer = client(
        {"Alpha": alpha, "PrimeMode": prime_mode, "PrimaryElement": param_g}
    )

    print(f"Alpha has arrived.")
    try:
        letter = json.loads(answer.decode())
        beta = letter["Beta"]
        key = pow(beta, param_x, prime_mode)
    except Exception as err:
        logging.exception("BetaError")
    else:
        print(f"Beta received: {beta}.")
        print(f"Key generated: {key}")

else:
    exit()