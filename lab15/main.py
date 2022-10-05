import random
import socket
import json
from STRIBOG import gost_256_512
from SHA import sha_256_512
from RSA import prime_num, alg_euc
import math

my_name = "Alice"
user_id = 7150

users = {"Bob": 9119}


def welcome():
    print(f"Host Id: {user_id}")
    print(f"Host Name: {my_name}\n")


def check_answer(answer_: bytes):
    try:
        letter_ = json.loads(answer_.decode())
        assert type(letter_) is dict
    except Exception as err:
        Exception("AnswerError")
        print(f'{err}')
        exit()
    else:
        if "Param C" in letter_.keys():
            return letter_['Param C']


def fragmentation(data_to_send):
    if type(data_to_send) is dict:
        return [json.dumps(data_to_send).encode()[x:x + 1024] for x in
                range(0, len(json.dumps(data_to_send).encode()), 1024)]
    elif type(data_to_send) is bytes:
        return [data_to_send[x:x + 1024] for x in
                range(0, len(data_to_send), 1024)]


def generation_secret_param(mod_num_: int):
    while True:
        param_s_ = random.randint(1, mod_num_ - 1)
        if math.gcd(param_s_, mod_num_) == 1:
            return param_s_


def client(data_to_send: dict or bytes):
    result = b""
    package_blocks = fragmentation(data_to_send)

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(("localhost", 6543))

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


welcome()
mod_num = prime_num(512) * prime_num(512)
save_ = {"N": mod_num}

print(f"Module N generated.")
client(save_)
print(f'N sent: {mod_num}.')

param_s = generation_secret_param(mod_num)
param_v = pow(param_s, 2, mod_num)

letter = {"PublicParam": param_v}
client(letter)
print(f'V sent: {param_v}.')

print(f"Basic parameters are set.\n")

counter = 0
for iter_numb in range(1, 11):
    param_z = random.randint(2, mod_num - 2)
    param_x = pow(param_z, 2, mod_num)

    letter = {"Param X": param_x}
    answer = client(letter)
    print(f'X sent: {param_x}.')

    param_c = check_answer(answer_=answer)
    print(f'C received: {param_c}.')

    param_y = pow(param_z * (param_s**param_c), 1, mod_num)

    letter = {'Param Y': param_y}
    print(f'Y sent: {param_y}.')

    answer = client(letter)
    print(f'Answer received: {answer}.')
    if answer == b"IterationSuccessful":
        counter += 1
        print(f"Iteration: {iter_numb} - Successful.\n")
    elif answer == b"IterationNotSuccessful":
        print(f"Authentication failed.")
        break

if counter == 10:
    print(f"Authentication passed.")