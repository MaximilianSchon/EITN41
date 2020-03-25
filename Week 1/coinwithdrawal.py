import random
import hashlib
from functools import reduce


def generate(n, k, id):
    coin = [{"a": random.randint(1, n),
            "c": random.randint(1, n),
            "d": random.randint(1, n),
            "r": generate_r()}
            for _ in range(2*k)]
    B = [computeb(coin[i], id, n) for i in range(2*k)]
    return B, coin


def generate_r():
    r = n
    while mulinv(r, n) is None:
        r = random.randint(1, n-1)
    return r


def computeb(coin, id, n):
    return pow(coin["r"], e, n) * computef(coin, id) % n


def computef(coin, id):
    x = hashlib.sha1(bytearray(coin["a"] + coin["c"])).hexdigest()
    y = hashlib.sha1(bytearray(coin["a"] ^ id + coin["d"])).hexdigest()
    return int(hashlib.sha3_256(bytearray.fromhex(x) + bytearray.fromhex(y)).hexdigest(), 16)


def egcd(a, b):  # https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x


def mulinv(a, b):  # https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
    g, x, _ = egcd(a, b)
    if g == 1:
        return x % b


p, q = 167, 22787 # Two primes
n = p*q
e = 3
totient = (p-1)*(q-1)
bank_priv = mulinv(e, totient)
k = 100
id = 1  # Alice's ID
B, coin_alice = generate(n, k, id)  # Alice blind signature and 2k quads
R = random.sample(range(2*k), k)  # Bank picks k indices
coin_bank = [coin_alice[i] for i in R if B[i] == computeb(coin_alice[i], id, n)]  # Bank gets access to the picked indices and verifies that the values are valid
if len(coin_bank) == k:  # If bank can verify that all of the coins belong to Alice
    signature = pow(reduce(lambda x, y: x*y, [B[i] for i in range(2*k) if i not in R]) % n, bank_priv, n) # Bank computes signature from remaining R
    serial_number = (signature * mulinv(reduce(lambda x, y: x*y, [coin_alice[i]['r'] for i in range(2*k) if i not in R]), n)) % n # Alice calculates the inverse of the product of R so we can multiply (effectively divide with R) with the inverse to receive the product of the signature.
    actual_serial_number = pow(reduce(lambda x, y: x*y, [computef(coin_alice[i], id) for i in range(2*k) if i not in R]), bank_priv, n) # Computes signature only using f (not blindly)
    print("The blind serial number is the same as the not blind one") if serial_number == actual_serial_number else print("The blind serial number is not the same the not blind one")
