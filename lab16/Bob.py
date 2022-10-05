import logging
import json
import random
import socket
import os

my_name = "Bob"

lab_name = "lab19"


def gen_key(my_polynomial: list, deg_polynomial_: int, other_r: int):
    temp_ = 0
    for i in range(deg_polynomial_):
        temp_ += my_polynomial[i] * pow(other_r, i)
    return temp_


def welcome():
    print(f"Host Name: {my_name}\n")


welcome()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as serv_sock:
    serv_sock.bind(("localhost", 7778))
    print(f"Socket info: {serv_sock}")
    serv_sock.listen(1)

    while True:
        client_sock, client_address = serv_sock.accept()
        print(f'Connected with: {client_address}.')
        result = b""
        count = 0
        while True:
            data = client_sock.recv(1024)
            if data == b"DataPut":
                try:
                    letter = json.loads(result.decode())
                    assert type(letter) is dict
                    key = gen_key(my_polynomial=letter['g(X)'], deg_polynomial_=letter['DegPolynomial'],
                                  other_r=letter['OtherR']) % letter["Prime"]

                    print(letter)
                    print(f"Key: {key}")
                except Exception as err:
                    logging.exception("DataError")
                    print(f'{err}')
                    client_sock.sendall(b"DataError")
                break
            result += data
            client_sock.sendall(str(count).encode())
            count += 1
        print(f"Close connection with: {client_address}.\n")
        client_sock.close()