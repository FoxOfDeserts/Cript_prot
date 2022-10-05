import logging
import random

import socket
import json
import os
from Stribog import gost_256_512
from SHA import sha_256_512
from RSA import prime_num, gen_parent_element

my_name = "Bob"
my_user_id = 2605
protocol_flag = False
prime_mode = 0
alpha = 0
param_g = 0

lab_name = os.path.basename(os.getcwd())
final_password = b''
last_password = b''
amount_passwords = 0
users = {"Alice": 4932}


def welcome():
    print(f"Host Id: {my_user_id}")
    print(f"Host Name: {my_name}\n")


def find_name(id_: int):
    for name_, val_ in users.items():
        if val_ == id_:
            return name_


def password_verification(password: bytes, iteration: int = 1):
    now_password = password
    for _ in range(iteration):
        now_password = sha_256_512(bytes_msg=now_password, size=512)
    if now_password == last_password:
        return True
    else:
        return False


welcome()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as serv_sock:
    serv_sock.bind(("localhost", 7568))
    # 10.0.126.164
    print(f"Socket info: {serv_sock}")
    serv_sock.listen(1)

    while True:
        # Бесконечно обрабатываем входящие подключения
        client_sock, client_addr = serv_sock.accept()
        print(f'Connected with: {client_addr}.')
        result = b""
        count = 0
        while True:
            # Пока клиент не отключился, читаем передаваемые
            # им данные и отправляем их обратно
            data = client_sock.recv(1024)
            # print(data)

            if data == b"DataPut":
                try:
                    letter = json.loads(result.decode())
                    assert type(letter) is dict
                    if protocol_flag and "Alpha" in letter.keys():
                        alpha = letter["Alpha"]
                        prime_mode = letter["PrimeMode"]
                        param_g = letter["PrimaryElement"]

                        print(f"Alpha received: {alpha}")
                        print(f"Prime number received: {prime_mode}")
                        print(f"Value G received: {param_g}")

                        param_y = random.randint(2, prime_mode - 2)
                        beta = pow(param_g, param_y, prime_mode)
                        key = pow(alpha, param_y, prime_mode)

                        print(f"Value Y generated: {param_y}")
                        print(f"Value beta generated: {beta}")
                        print(f"Key generated: {key}")

                        letter = {"Beta": beta}
                        client_sock.sendall(json.dumps(letter).encode())

                    if "Final" in letter.keys():
                        final_password = bytes.fromhex(letter["Final"])
                        last_password = bytes.fromhex(letter["Final"])

                    # if "Id" in letter.keys() and letter['Id'] in users.values():
                    elif "Id" in letter.keys() and letter['Id'] in users.values():
                        name = find_name(letter['Id'])
                        print(f"User Id: {letter['Id']}")
                        print(f"Name: {name}")

                        if password_verification(password=bytes.fromhex(letter["Password"])):
                            last_password = bytes.fromhex(letter["Password"])

                            print(f"{insertion_tag} Iteration: {letter['Iteration']}")
                            print(f"{insertion_tag} Password: {letter['Password']}.")
                            print(f"{insertion_tag} Authentication passed.")

                            protocol_flag = True
                            client_sock.sendall(b"AuthenticationPassed")

                        else:
                            print(f"{insertion_tag} Authentication failed.")
                            client_sock.sendall(b"AuthenticationFailed")

                except Exception as err:
                    logging.exception("DataError")
                    print(f'{insertion_tag} {err}')
                    client_sock.sendall(b"DataError")
                break
            result += data
            client_sock.sendall(str(count).encode())
            count += 1
        print(f"Close connection with: {client_addr}.\n")
        client_sock.close()