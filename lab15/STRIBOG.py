import math
import sys

S_const = [252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77, 233,
           119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193, 249, 24,
           101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79, 5, 132, 2, 174, 227,
           106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31, 235, 52, 44, 81, 234, 200, 72,
           171, 242, 42, 104, 162, 253, 58, 206, 204, 181, 112, 14, 86, 8, 12, 118, 18, 191,
           114, 19, 71, 156, 183, 93, 135, 21, 161, 150, 41, 16, 123, 154, 199, 243, 145, 120,
           111, 157, 158, 178, 177, 50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195,
           189, 13, 87, 223, 245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185,
           3, 224, 15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74, 167, 151,
           96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65, 173, 69, 70, 146, 39, 94,
           85, 47, 140, 163, 165, 125, 105, 213, 149, 59, 7, 88, 179, 64, 134, 172, 29, 247, 48,
           55, 107, 228, 136, 217, 231, 137, 225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170,
           144, 202, 216, 133, 97, 32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229,
           108, 82, 89, 166, 116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182]

P_const = [0, 8, 16, 24, 32, 40, 48, 56, 1, 9, 17, 25, 33, 41, 49, 57, 2, 10, 18, 26, 34, 42, 50, 58,
           3, 11, 19, 27, 35, 43, 51, 59, 4, 12, 20, 28, 36, 44, 52, 60, 5, 13, 21, 29, 37, 45, 53,
           61, 6, 14, 22, 30, 38, 46, 54, 62, 7, 15, 23, 31, 39, 47, 55, 63]

L_const = [b'\x8e \xfa\xa7+\xa0\xb4p', b'G\x10}\xdd\x9bPZ8', b'\xad\x08\xb0\xe0\xc3(-\x1c',
           b'\xd8\x04Xp\xef\x14\x98\x0e', b'l\x02,8\xf9\nL\x07', b'6\x01\x16\x1c\xf2\x05&\x8d',
           b'\x1b\x8e\x0b\x0ey\x8c\x13\xc8', b'\x83G\x8b\x07\xb2F\x87d', b'\xa0\x11\xd3\x80\x81\x8e\x8f@',
           b'P\x86\xe7@\xceG\xc9 ', b'(C\xfd g\xad\xea\x10', b'\x14\xaf\xf0\x10\xbd\xd8u\x08',
           b'\n\xd9x\x08\xd0l\xb4\x04', b'\x05\xe2<\x04h6Z\x02', b'\x8cq\x1e\x024\x1b-\x01',
           b'F\xb6\x0f\x01\x1a\x83\x98\x8e', b'\x90\xda\xb5*8z\xe7o', b'Hm\xd4\x15\x1c=\xfd\xb9',
           b'$\xb8j\x84\x0e\x90\xf0\xd2', b'\x12\\5B\x07Hxi', b'\t.\x94!\x8d$<\xba', b'\x8a\x17J\x9e\xc8\x12\x1e]',
           b'E\x85%Od\t\x0f\xa0', b'\xac\xcc\x9c\xa92\x8a\x89P', b'\x9dM\xf0]_f\x14Q', b'\xc0\xa8x\xa0\xa13\n\xa6',
           b'`T<P\xde\x97\x05S', b'0*\x1e(o\xc5\x8c\xa7', b'\x18\x15\x0f\x14\xb9\xecF\xdd', b'\x0c\x84\x89\n\xd2v#\xe0',
           b'\x06B\xca\x05i;\x9fp', b'\x03!e\x8c\xba\x93\xc18', b"\x86']\xf0\x9c\xe8\xaa\xa8", b'C\x9d\xa0xNtUT',
           b"\xaf\xc0P<':\xa4*", b'\xd9`(\x1e\x9d\x1dR\x15', b'\xe20\x14\x0f\xc0\x80)\x84', b'q\x18\n\x89`@\x9aB',
           b'\xb6\x0c\x05\xca0 M!', b'[\x06\x8ce\x18\x10\xa8\x9e', b'El4\x88z8\x05\xb9', b'\xac6\x1aD=\x1c\x8c\xd2',
           b'V\x1b\r"\x90\x0eFi', b'+\x83\x88\x11H\x07#\xba', b'\x9b\xcfD\x86$\x8d\x9f]', b'\xc3\xe9"C\x12\xc8\xc1\xa0',
           b'\xef\xfa\x11\xaf\td\xeeP', b'\xf9}\x86\xd9\x8a2w(', b'\xe4\xfa T\xa8\x0b2\x9c', b'r}\x10*T\x8b\x19N',
           b"9\xb0\x08\x15*\xcb\x82'", b'\x92X\x04\x84\x15\xebA\x9d', b'I,\x02B\x84\xfb\xae\xc0',
           b'\xaa\x16\x01!B\xf3W`', b'U\x0b\x8e\x9e!\xf7\xa50', b'\xa4\x8bGO\x9e\xf5\xdc\x18', b'p\xa6\xa5n$@Y\x8e',
           b'8S\xdc7\x12 \xa2G', b'\x1c\xa7n\x95\t\x10Q\xad', b'\x0e\xdd7\xc4\x8a\x08\xa6\xd8', b'\x07\xe0\x95bE\x04Sl',
           b'\x8dp\xc41\xac\x02\xa76', b'\xc88b\x96V\x01\xdd\x1b', b'd\x1c1K+\x8e\xe0\x83']

C_const = [
    b'\xb1\x08[\xda\x1e\xca\xda\xe9\xeb\xcb/\x81\xc0e|\x1f/jvC.E\xd0\x16qN\xb8\x8du\x85\xc4\xfcK|\xe0\x91\x92gi\x01\xa2B*\x08\xa4`\xd3\x15\x05vt6\xcctM#\xdd\x80eY\xf2\xa6E\x07',
    b'o\xa3\xb5\x8a\xa9\x9d/\x1aO\xe3\x9dF\x0fp\xb5\xd7\xf3\xfe\xear\n#+\x98a\xd5^\x0f\x16\xb5\x011\x9a\xb5\x17k\x12\xd6\x99X\\\xb5a\xc2\xdb\n\xa7\xcaU\xdd\xa2\x1b\xd7\xcb\xcdV\xe6y\x04p!\xb1\x9b\xb7',
    b'\xf5t\xdc\xac+\xce/\xc7\n9\xfc(j=\x845\x06\xf1^_R\x9c\x1f\x8b\xf2\xeau\x14\xb1){{\xd3\xe2\x0f\xe4\x905\x9e\xb1\xc1\xc9:7`b\xdb\t\xc2\xb6\xf4C\x86z\xdb1\x99\x1e\x96\xf5\n\xba\n\xb2',
    b'\xef\x1f\xdf\xb3\xe8\x15f\xd2\xf9H\xe1\xa0]q\xe4\xddH\x8e\x85~3\\<}\x9dr\x1c\xadh^5?\xa9\xd7,\x82\xed\x03\xd6u\xd8\xb7\x133\x93R\x03\xbe4S\xea\xa1\x93\xe87\xf1"\x0c\xbe\xbc\x84\xe3\xd1.',
    b"K\xeak\xac\xadGG\x99\x9a?A\x0cl\xa9#c\x7f\x15\x1c\x1f\x16\x86\x10J5\x9e5\xd7\x80\x0f\xff\xbd\xbf\xcd\x17G%:\xf5\xa3\xdf\xff\x00\xb7#'\x1a\x16zV\xa2~\xa9\xeac\xf5`\x17X\xfd|l\xfeW",
    b'\xaeO\xae\xae\x1d:\xd3\xd9o\xa4\xc3;z09\xc0-f\xc4\xf9QB\xa4l\x18\x7f\x9a\xb4\x9a\xf0\x8e\xc6\xcf\xfa\xa6\xb7\x1c\x9a\xb7\xb4\n\xf2\x1ff\xc2\xbe\xc6\xb6\xbfq\xc5r6\x90O5\xfah@zFd}n',
    b'\xf4\xc7\x0e\x16\xee\xaa\xc5\xecQ\xac\x86\xfe\xbf$\tT9\x9e\xc6\xc7\xe6\xbf\x87\xc9\xd3G>3\x19z\x93\xc9\t\x92\xab\xc5-\x82,7\x06Gi\x83(J\x05\x045\x17EL\xa2<J\xf3\x88\x86VM:\x14\xd4\x93',
    b'\x9b\x1f[BM\x93\xc9\xa7\x03\xe7\xaa\x02\x0cnAAN\xb7\xf8q\x9c6\xde\x1e\x89\xb4D;M\xdb\xc4\x9a\xf4\x89+\xcb\x92\x9b\x06\x90i\xd1\x8d+\xd1\xa5\xc4/6\xac\xc25YQ\xa8\xd9\xa4\x7f\r\xd4\xbf\x02\xe7\x1e',
    b'7\x8fZT\x161"\x9b\x94L\x9a\xd8\xec\x16_\xde:}:\x1b%\x89B$<\xd9U\xb7\xe0\r\t\x84\x80\nD\x0b\xdb\xb2\xce\xb1{+\x8a\x9a\xa6\x07\x9cT\x0e8\xdc\x92\xcb\x1f*`raDQ\x83#Z\xdb',
    b'\xab\xbe\xde\xa6\x80\x05oR8*\xe5H\xb2\xe4\xf3\xf3\x89A\xe7\x1c\xff\x8ax\xdb\x1f\xff\xe1\x8a\x1b3a\x03\x9f\xe7g\x02\xafi3Kz\x1el0;vR\xf46\x98\xfa\xd1\x15;\xb6\xc3t\xb4\xc7\xfb\x98E\x9c\xed',
    b'{\xcd\x9e\xd0\xef\xc8\x89\xfb0\x02\xc6\xcdcZ\xfe\x94\xd8\xfak\xbb\xeb\xab\x07a \x01\x80!\x14\x84fy\x8a\x1dq\xef\xeaH\xb9\xca\xef\xba\xcd\x1d}Gn\x98\xde\xa2YJ\xc0o\xd8]k\xca\xa4\xcd\x81\xf3-\x1b',
    b'7\x8e\xe7g\xf1\x161\xba\xd2\x13\x80\xb0\x04I\xb1z\xcd\xa4<2\xbc\xdf\x1dw\xf8 \x12\xd40!\x9f\x9b]\x80\xef\x9d\x18\x91\xcc\x86\xe7\x1d\xa4\xaa\x88\xe1(R\xfa\xf4\x17\xd5\xd9\xb2\x1b\x99H\xbc\x92J\xf1\x1b\xd7 ']


def xor_(vec_1: bytes, vec_2: bytes, byteorder=sys.byteorder):
    int_enc = int.from_bytes(vec_2, byteorder) ^ int.from_bytes(vec_1, byteorder)
    return int_enc.to_bytes(len(vec_1), byteorder)


def ps_trans(msg: bytes) -> bytes:
    result = bytearray(64)
    for i in range(64):
        result[P_const[i]] = S_const[msg[i]]
    return bytes(result)


def l_trans(p_result: bytes) -> bytes:
    result = []
    PS_vector = [p_result[x:x + 8] for x in range(0, len(p_result), 8)]
    for vector in PS_vector:
        xor_vector = b'\x00' * 8
        ind__ = 0
        for ind_ in range(len(vector)):
            for bit_shift in range(8):
                if (vector[ind_] >> (7 - bit_shift)) & 1:
                    xor_vector = xor_(xor_vector, L_const[ind__])
                ind__ += 1
        result.append(xor_vector)
    return b"".join(result)


def LPS(msg: bytes) -> bytes:
    return l_trans(ps_trans(msg))


def E_trans(k1: bytes, msg: bytes) -> bytes:
    k = [k1]
    for i in range(1, 13):
        k.append(LPS(xor_(k[i - 1], C_const[i - 1])))
    for j in range(13):
        if j == 12:
            msg = xor_(k[j], msg)
            break
        msg = LPS(xor_(k[j], msg))
    return msg


def compression_function(hash_: bytes, msg: bytes, n_vector: bytes) -> bytes:
    ' k1 = LPS(XOR_(hash_, n_vector))'
    'e_res = E_trans(k1, msg)'
    'hash_ = XOR_(XOR_(E_trans(LPS(XOR_(hash_, n_vector)), msg), hash_), msg)'
    return xor_(xor_(E_trans(LPS(xor_(hash_, n_vector)), msg), hash_), msg)


def gost_256_512(bytes_msg: bytes, size: int):
    big_lit = "big"
    msg = bytearray(bytes_msg)
    msg.reverse()

    data = bytes(msg)
    size = size // 8

    if size != 32 and size != 64:
        raise ValueError("Size got 512 or 256")

    hash_ = 64 * (b'\x00' if size == 64 else b'\x01')

    __n_vector = b'\x00' * 64
    __e_vector = b'\x00' * 64
    while True:
        if len(data) < 64:
            len_msg = len(data)
            data = (b"\x00" * (63 - len_msg)) + b"\x01" + data
            hash_ = compression_function(hash_, data, __n_vector)

            n_num = (int.from_bytes(__n_vector, big_lit) + (len_msg * 8)) % pow(2, 512)
            mp = n_num.to_bytes(math.ceil(math.log2(n_num) / 8), big_lit)
            __n_vector = (b"\x00" * (64 - len(mp))) + mp

            e_num = (int.from_bytes(__e_vector, big_lit) + int.from_bytes(data,
                                                                          big_lit)) % pow(2, 512)
            mp = e_num.to_bytes(math.ceil(math.log2(e_num) / 8), big_lit)
            __e_vector = (b"\x00" * (64 - len(mp))) + mp

            zero_vector = b'\x00' * 64
            hash_ = compression_function(compression_function(hash_, __n_vector, zero_vector),
                                         __e_vector, zero_vector)[:size]

            result = bytearray(hash_)
            result.reverse()
            return bytes(result).hex()

        else:
            mp_msg = data
            mod_pr = len(data)
            data = mp_msg[mod_pr - 64:]

            hash_ = compression_function(hash_, data, __n_vector)

            n_num = (int(__n_vector.hex(), 16) + 512) % pow(2, 512)
            mp = n_num.to_bytes(math.ceil(math.log2(n_num) / 8), big_lit)
            __n_vector = (b"\x00" * (64 - len(mp))) + mp

            e_num = (int(__e_vector.hex(), 16) + int(data.hex(), 16)) % pow(2, 512)
            mp = e_num.to_bytes(math.ceil(math.log2(e_num) / 8), big_lit)
            __e_vector = (b"\x00" * (64 - len(mp))) + mp

            data = mp_msg[:mod_pr - 64]