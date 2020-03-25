import hashlib
import math
import binascii
import re

mgfSeed = "" #(hexadecimal)
maskLen = 26 #(decimal)
M = ""
seed = ""
EM = """"""
L = ""


def i2osp(x, xLen):
    num = []
    if 256 ** xLen > x >= 0:
        while x:
            num.append(x % 256)
            x //= 256
        while len(num) < xLen:
            num.append(0)
        return bytes(num[::-1])


def mgf1(mgfseed, masklen):
    hlen = 20
    if masklen <= 2 ** 32 * hlen: # * 20?
        T = bytes()
        for counter in range(math.ceil(masklen / hlen)):
            C = i2osp(counter, 4)
            T += hashlib.sha1(bytes.fromhex(mgfseed) + C).digest()
        return binascii.hexlify(T[:masklen])


def encode(M, seed, L):
    k = 128
    hLen = 20     #Step a
    mLen = len(M) // 2
    lHash = hashlib.sha1(L.encode("ascii")).hexdigest()
    PS = "00" * (k - mLen - 2*hLen - 2) # Step b
    DB = "0x" + lHash + PS + "01" + M # Step c
    dbMask = mgf1(seed, k - hLen - 1) # Step e
    maskedDB = hex(int(DB, 16) ^ int(dbMask, 16))[2:].zfill(hLen*2) # Step f
    seedMask = mgf1(maskedDB, hLen) # Step g
    maskedSeed = hex(int(seed, 16) ^ int(seedMask, 16))[2:].zfill(hLen*2) # Step h
    EM = "00" + maskedSeed + maskedDB
    return EM


def decode(EM, L):
    EM = EM.replace('\r', '').replace('\n', '')
    k = 128
    lHash = hashlib.sha1(L.encode("ascii")).hexdigest()
    hLen = 20
    EM = EM[2:]
    maskedSeed = EM[:hLen*2]
    maskedDB = EM[hLen*2:]
    seedMask = mgf1(maskedDB, hLen)
    seed = hex(int(maskedSeed, 16) ^ int(seedMask, 16))[2:].zfill(hLen*2)
    dbMask = mgf1(seed, k - hLen - 1)
    DB = hex(int(maskedDB, 16) ^ int(dbMask, 16))[2:].zfill(hLen*2)
    return DB[hLen*2:].lstrip('0')[1:]

print(encode(M, seed, ""))
print(decode(EM, ""))