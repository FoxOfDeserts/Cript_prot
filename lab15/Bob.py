import random
import socket
import json
from STRIBOG import gost_256_512
from SHA import sha_256_512
from RSA import prime_num, alg_euc
import math

mod_num = 0
param_v = 0
param_x = 0
param_y = 0

users = {"Alice": 7150}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as serv_sock:
    serv_sock.bind(("localhost", 6543))
    print(serv_sock)
    serv_sock.listen(1)

    while True:
        client_sock, client_addr = serv_sock.accept()
        print(f'Connected by', client_addr)
        result = b""
        count = 0
        while True:
            data = client_sock.recv(1024)
            print(data)
            if data == b"DataPut":
                try:
                    letter = json.loads(result.decode())
                    assert type(letter) is dict
                    if "N" in letter.keys():
                        mod_num = letter['N']
                        print(f'N received: {mod_num}.')

                    if "PublicParam" in letter.keys():
                        param_v = letter["PublicParam"]
                        print(f'V received: {param_v}.')

                    if "Param X" in letter.keys():
                        param_x = letter["Param X"]
                        print(f'X received: {param_x}.')

                        param_c = round(random.random())
                        answer = {"Param C": param_c}
                        answer = json.dumps(answer).encode()
                        client_sock.sendall(answer)
                        print(f'C sent: {param_c}.')

                    if "Param Y" in letter.keys():
                        param_y = letter["Param Y"]
                        print(f'Y received: {param_y}.')

                        if param_y != 0 and \
                                (param_y ** 2)%mod_num == \
                                pow(param_x * (param_v ** param_c), 1, mod_num):
                            answer_ = b"IterationSuccessful"
                        else:
                            answer_ = b"IterationNotSuccessful"
                        print("done")
                        client_sock.sendall(answer_)
                        print(f'Answer sent: {answer_}.')
                except Exception as err:
                    print(f'{err}')
                    client_sock.sendall(b"DataError")

                break
            result += data
            client_sock.sendall(str(count).encode())
            count += 1
        print(f"Close connection with {client_addr[0]}\n")
        client_sock.close()