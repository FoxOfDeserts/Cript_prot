import json
import random
import os
import sympy
import socket

my_name = "Leader"
users = {
    "Alice": {"R": 0, "Port": 7777},
    "Bob": {"R": 0, "Port": 7778}
}

def fragmentation(data_to_send):
    if type(data_to_send) is dict:
        return [json.dumps(data_to_send).encode()[x:x + 1024] for x in
                range(0, len(json.dumps(data_to_send).encode()), 1024)]
    elif type(data_to_send) is bytes:
        return [data_to_send[x:x + 1024] for x in
                range(0, len(data_to_send), 1024)]

def client(data_to_send: dict or bytes, port):
    result = b""
    package_blocks = fragmentation(data_to_send)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect(("localhost", port))
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

def welcome():
    lab_name = os.path.basename(os.getcwd())
    print(f"Host Name: {my_name}\n")


def client_decor():
    for username in users:
        client(users[username], users[username]["Port"])


def gen_polynomial():
    polynomial_ = [[random.randint(1, prime_ - 1) for _ in range(deg_polynomial)] for _ in range(deg_polynomial)]

    for i in range(deg_polynomial):
        for j in range(deg_polynomial):
            polynomial_[j][i] = polynomial_[i][j]

    return polynomial_


def gen_user_polynomial(polynomial_: list, temp_r0: int):
    user_polynomial = []
    for i in range(deg_polynomial):
        temp = 0
        for j in range(deg_polynomial):
            temp += polynomial_[j][i] * pow(temp_r0, i)
        user_polynomial.append(temp % prime_)
    return user_polynomial

prime_ = prime_num(1024)
n = len(users)
print(f"N : {n}")
users["Alice"]["R"] = random.randint(1, prime_-1)
users["Bob"]["R"] = random.randint(1, prime_-1)

print(f"P : {prime_}")
print(f"r0 : {users['Alice']['R']}")
print(f"r1 : {users['Bob']['R']}")
deg_polynomial = 2 * n

welcome()

polynomial = gen_polynomial()

print(polynomial)

for user_name in users:
    users[user_name]['g(X)'] = gen_user_polynomial(polynomial, users[user_name]["R"])
    users[user_name]['OtherR'] = users["Bob"]["R"] if user_name == "Alice" else users["Alice"]["R"]
    users[user_name]['DegPolynomial'] = deg_polynomial
    users[user_name]['Prime'] = prime_

client_decor()