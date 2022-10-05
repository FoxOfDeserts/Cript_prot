H_256 = [
    0x6a09e667,
    0xbb67ae85,
    0x3c6ef372,
    0xa54ff53a,
    0x510e527f,
    0x9b05688c,
    0x1f83d9ab,
    0x5be0cd19
]
H_512 = [
    0x6a09e667f3bcc908,
    0xbb67ae8584caa73b,
    0x3c6ef372fe94f82b,
    0xa54ff53a5f1d36f1,
    0x510e527fade682d1,
    0x9b05688c2b3e6c1f,
    0x1f83d9abfb41bd6b,
    0x5be0cd19137e2179
]
K_256 = [
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,
    0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
    0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC,
    0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7,
    0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
    0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3,
    0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5,
    0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208,
    0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2
]
K_512 = [
    0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
    0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
    0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
    0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694,
    0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
    0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
    0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4,
    0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70,
    0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
    0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
    0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30,
    0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
    0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
    0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
    0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
    0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
    0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
    0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
    0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
    0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817
]


def ch(x: int, y: int, z: int) -> int:
    return (x & y) ^ (~x & z)


def Maj(x: int, y: int, z: int) -> int:
    return (x & y) ^ (x & z) ^ (y & z)


def E_0_256(x: int) -> int:
    return int(right_rotate(x, 2, 32), 2) ^ int(right_rotate(x, 13, 32), 2) ^ int(right_rotate(x, 22, 32), 2)


def E_0_512(x: int) -> int:
    return int(right_rotate(x, 28, 64), 2) ^ int(right_rotate(x, 34, 64), 2) ^ int(right_rotate(x, 39, 64), 2)


def E_1_256(x: int) -> int:
    return int(right_rotate(x, 6, 32), 2) ^ int(right_rotate(x, 11, 32), 2) ^ int(right_rotate(x, 25, 32), 2)


def E_1_512(x: int) -> int:
    return int(right_rotate(x, 14, 64), 2) ^ int(right_rotate(x, 18, 64), 2) ^ int(right_rotate(x, 41, 64), 2)


def sig_0_256(x: int) -> int:
    return int(right_rotate(x, 7, 32), 2) ^ int(right_rotate(x, 18, 32), 2) ^ (x >> 3)  # int(x, 2) >> 3


def sig_0_512(x: int) -> int:
    return int(right_rotate(x, 1, 64), 2) ^ int(right_rotate(x, 8, 64), 2) ^ (x >> 7)


def sig_1_256(x: int) -> int:
    return int(right_rotate(x, 17, 32), 2) ^ int(right_rotate(x, 19, 32), 2) ^ (x >> 10)  # int(x, 2) >> 10


def sig_1_512(x: int) -> int:
    return int(right_rotate(x, 19, 64), 2) ^ int(right_rotate(x, 61, 64), 2) ^ (x >> 6)


def hex_to_bin_v3(mess_bytes: bytes, choose) -> int or str:  # mess.encode("utf-8")
    if choose == 1:
        if len(bin(int.from_bytes(mess_bytes, "big"))[2:].zfill((len(mess_bytes.hex()) // 2) * 8)) > 2 ** 64:
            return -1
    elif choose == 2:
        if len(bin(int.from_bytes(mess_bytes, "big"))[2:].zfill((len(mess_bytes.hex()) // 2) * 8)) > 2 ** 128:
            return -1
    return bin(int.from_bytes(mess_bytes, "big"))[2:].zfill((len(mess_bytes.hex()) // 2) * 8)


def right_rotate(num_: int, step: int, mode: int) -> str:
    return bin(num_)[2:].zfill(mode)[mode - step:] + bin(num_)[2:].zfill(mode)[:mode - step]


def __sha_256(bytes_msg: bytes):
    H = H_256.copy()
    bin_mess = hex_to_bin_v3(bytes_msg, 1)
    if bin_mess == -1:
        raise ValueError("Bytes so large.")
    l = len(bin_mess)
    bin_mess += "1" + ("0" * ((448 - l - 1) % 512)) + bin(l)[2:].zfill(64)

    bin_mess = [bin_mess[x:x + 512] for x in range(0, len(bin_mess), 512)]

    for i in range(len(bin_mess)):

        w_t = [int(bin_mess[i][x:x + 32], 2) for x in range(0, 512, 32)]

        #
        for j in range(48):
            w_t.append(0)
        for t in range(16, 64):
            w_t[t] = ((sig_1_256(w_t[t - 2]) + w_t[t - 7] + sig_0_256(w_t[t - 15]) + w_t[t - 16]) % (2 ** 32))
        a = H[0]
        b = H[1]
        c = H[2]
        d = H[3]
        e = H[4]
        f = H[5]
        g = H[6]
        h = H[7]
        for t in range(64):
            temp1 = (h + E_1_256(e) + ch(e, f, g) + K_256[t] + w_t[t]) % (2 ** 32)
            temp2 = (E_0_256(a) + Maj(a, b, c)) % (2 ** 32)
            h = g
            g = f
            f = e
            e = (d + temp1) % (2 ** 32)
            d = c
            c = b
            b = a
            a = (temp1 + temp2) % (2 ** 32)
        H[0] = (H[0] + a) % (2 ** 32)  # pow((H[0] + a), 1, pow(2, 32))
        H[1] = (H[1] + b) % (2 ** 32)  # pow((H[1] + b), 1, pow(2, 32))
        H[2] = (H[2] + c) % (2 ** 32)  # pow((H[2] + c), 1, pow(2, 32))
        H[3] = (H[3] + d) % (2 ** 32)  # pow((H[3] + a), 1, pow(2, 32))
        H[4] = (H[4] + e) % (2 ** 32)
        H[5] = (H[5] + f) % (2 ** 32)
        H[6] = (H[6] + g) % (2 ** 32)
        H[7] = (H[7] + h) % (2 ** 32)
    return b"".join([bytes.fromhex(hex(x)[2:].zfill(8)) for x in H])


def __sha_512(bytes_msg: bytes):
    H = H_512.copy()
    bin_mess = hex_to_bin_v3(bytes_msg, 2)

    if bin_mess == -1:
        raise ValueError("Bytes so large.")

    len_bin_mess = len(bin_mess)
    bin_mess += "1" + ("0" * ((896 - len_bin_mess - 1) % 1024)) + bin(len_bin_mess)[2:].zfill(128)

    bin_mess = [bin_mess[x:x + 1024] for x in range(0, len(bin_mess), 1024)]

    for i in range(len(bin_mess)):

        w_t = [int(bin_mess[i][x:x + 64], 2) for x in range(0, 1024, 64)]

        for _ in range(64):
            w_t.append(0)
        for t in range(16, 80):
            w_t[t] = ((sig_1_512(w_t[t - 2]) + w_t[t - 7] + sig_0_512(w_t[t - 15]) + w_t[t - 16]) % (2 ** 64))
        a = H[0]
        b = H[1]
        c = H[2]
        d = H[3]
        e = H[4]
        f = H[5]
        g = H[6]
        h = H[7]
        for t in range(80):
            temp1 = (h + E_1_512(e) + ch(e, f, g) + K_512[t] + w_t[t]) % (2 ** 64)
            temp2 = (E_0_512(a) + Maj(a, b, c)) % (2 ** 64)
            h = g
            g = f
            f = e
            e = (d + temp1) % (2 ** 64)
            d = c
            c = b
            b = a
            a = (temp1 + temp2) % (2 ** 64)
        H[0] = (H[0] + a) % (2 ** 64)
        H[1] = (H[1] + b) % (2 ** 64)
        H[2] = (H[2] + c) % (2 ** 64)
        H[3] = (H[3] + d) % (2 ** 64)
        H[4] = (H[4] + e) % (2 ** 64)
        H[5] = (H[5] + f) % (2 ** 64)
        H[6] = (H[6] + g) % (2 ** 64)
        H[7] = (H[7] + h) % (2 ** 64)

    return b"".join([bytes.fromhex(hex(x)[2:].zfill(16)) for x in H])


def sha_256_512(bytes_msg: bytes, size: int):
    if size == 256:
        return __sha_256(bytes_msg), "SHA"
    elif size == 512:
        return __sha_512(bytes_msg), "SHA"
    else:
        raise ValueError("Incorrect size")