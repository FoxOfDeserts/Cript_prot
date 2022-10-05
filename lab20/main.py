import json
import pprint
import random
import os
import sympy

my_name = "Leader"

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
    art.tprint(lab_name, font="chiseled")
    print(f"Host Name: {my_name}\n")


def gen_polynomial(prime_, deg_polynomial):
    polynomial_ = [random.randint(1, prime_ - 1) for _ in range(deg_polynomial + 1)]
    return polynomial_


def func_at_x(poly: list, x: int, deg_polynomial):
    result = poly[0]
    for i in range(1, deg_polynomial + 1):
        result += (poly[i] * pow(x, i))
    return result


def gen_c_param(users_r_: list, prime_: int):
    c_params = []
    for i in range(len(users_r_)):
        temp_c = 1
        for j in range(len(users_r_)):
            if i != j:
                temp_c = temp_c * (users_r_[j] * gen_inverse_modulo(prime_, (users_r_[j] - users_r_[i]) % prime_))

        c_params.append(temp_c)
    return c_params


def work():
    prime_ = prime_num(512)
    n = 4
    deg_polynomial = 3
    polynomial = gen_polynomial(prime_, deg_polynomial)
    users_r = []
    while len(users_r) < n:
        r = random.randint(2, prime_ - 1)
        if r not in users_r:
            users_r.append(r)
    print(f"Poly: {polynomial}")
    print(f'R:    {users_r}')

    users_c = gen_c_param(users_r, prime_)

    s = polynomial[0]

    new_s = 0
    for i in range(len(users_r)):
        new_s += (func_at_x(polynomial, x=users_r[i], deg_polynomial=deg_polynomial) * users_c[i])

    print(f'S : {s}')
    print(f'S~: {round(new_s % prime_)}\n')

    if round(new_s % prime_) == s:
        return True

print(work())