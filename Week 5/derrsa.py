import math
import base64


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


def encode(num):
    val = str(hex(num)[2:])
    if int(val[0], 16) >= 8:  # I initially had > 8
        val = "00" + val
    length = math.ceil(len(val) / 2)  # Do I need math.ceil?
    val = val.zfill(length*2)
    length = getHexLength(length)
    return "02" + length + val


def createkey(p, q, e = 65537):
    v = 0
    n = p*q
    d = mulinv(e, (p-1)*(q-1))
    e1 = d % (p-1)
    e2 = d % (q-1)
    coef = mulinv(q, p)
    key = encode(v) + encode(n) + encode(e) + encode(d) + encode(p) + encode(q) + encode(e1) + encode(e2) + encode(coef)
    length = getHexLength(math.ceil(len(key) / 2))
    seq = "30" + length + key
    return base64.b64encode(bytes.fromhex(seq)).decode("utf-8")


def getHexLength(length):
    if 256 > length > 127:
        length = "81" + str(hex(length)[2:]).zfill(2)
    elif length >= 256:
        length = "82" + str(hex(length)[2:]).zfill(4)
    else:
        length = str(hex(length)[2:]).zfill(2)
    return length


print(createkey(2530368937, 2612592767) == "MDwCAQACCFu+XQXUfXbXAgMBAAECCDZpw5W5z3MhAgUAltJdqQIFAJu5AH8CBHgJdgECBFlLQGkCBFjc97Q=")
p = 139721121696950524826588106850589277149201407609721772094240512732263435522747938311240453050931930261483801083660740974606647762343797901776568952627044034430252415109426271529273025919247232149498325412099418785867055970264559033471714066901728022294156913563009971882292507967574638004022912842160046962763
q = 141482624370070397331659016840167171669762175617573550670131965177212458081250216130985545188965601581445995499595853199665045326236858265192627970970480636850683227427420000655754305398076045013588894161738893242561531526805416653594689480170103763171879023351810966896841177322118521251310975456956247827719
print(createkey(p, q) == "MIIEogIBAAKCAQEAnJf2WUeCeb9wfIwgga8zCXgtw5D3o68JbhjOZRRlRHB9M8uAriE8+wZe3rvkkj0ShlsoP3cr0e4VOXlOYHuMD4dDDOa3dAji00c0x0b1kEcjy1+yuGhphKcI3LZK6rIds/9jO3/p2WbDlEqnV12OQJ/oj0k9Ia6S+OdkSJ89GKwUnRtpARO6Lsc2IYvDKJb41lTrKbW2T5tBcoUtbs2q1GynSGxq1A1ZkE7snqzp7VFuY6a+eUb/0kpoTIkcbwsIaV7nvgSFUw7yNxPmZfinLpirU8ygTILn8YSw9PcmshHg3K8c/i0oVg6108+crr7I1ocWITf5s2U4Hx2d8IRhDQIDAQABAoIBAHepJ/bRTkL6p1qFOdHfr4Bs9YucG6BZATvAePeEvl2uF/6cY5isjYzFMXnC2sdlI+LHhdn5luK0rENfDyVrQ3waQIJ7S3S/1ZTdtNcSwlOeCRw/5LJGF1vmyD7gjh8KPOhvH8U32drnTEzlPzrjovB/QZc8wBoc7PKG33sfM/DFXHmqdtJpzhqCzR8Pya7jd2zcZhOby4GiDdhqJqHsUOnB8WOrb9+q6iTOenwAKqcj8k1ZLnKrKD4PYuoQ2UPDDb6zYF4CRxOF/CDmh5uqDxZe0WLCCMuGB5HpWeOvLvwWRYy0brDxU9F7280FzPSN2m138ioZwTUjChMb4ot5iYECgYEAxvgv9izjz2PMgXtS6/gCGGgSeE8Sk11gSfpF1aCzLO4x7sYlvR41/VJoWb6akO+FTBzjJQ48TNHANh3HEVciSISIWMD/iZjHd5SgQE/3Vf13ikYlvG3eDwhUTjkRO3hlJouTb7jNO1JzQDTiDnU65nz3WVEeQp2jxw2YULixeEsCgYEAyXpamPVj7rJbLYYtLoweQApgH4LJQTipyysUU6dm8zxWt6mNFLU2rSH3bQj+W2hgNKwftyD5OOz0BrRM533WVt4gLGzku35XwcGEng81R7PB4wySOF7QQvNobsWqm6sr0dtczfWMZRDwx4czbyx0mEXWkZ4l7P1cWrVlSw3N5QcCgYBu1bQJ4umoDkTOX/9KGSY5qEeZoxqK4noP241pOhJ1Vd6UzuYY2ipjCbO9QlLhp7tOMc1KSArJFBKJUr8gZrRfRwyYvDHc2TFL6Iv4J1N1IDOl3/uHYoBPSWmFBX8W7LMT7K5djsksYXp36r1+JkmAOV6j72721s9zw5v0Y13gzwKBgEbvfypPa2nE/fkfPpUe3B+sB3/Qqk7+Rjmz5yo0zDhjTBzJ41QhISj/xn9rJTLFoumomFn/j/+M3bXmkRUH5wkal7VMeZPRvdAH9Es6C4Y9McxgxrJ2H1kTHfeyPIkmUP1IAHq7Mzz6I+v8HA3OVxatsAgA6FVyNqvxJcKxD4bNAoGAWyjxJZiszY/2COAdjT3QWCpCDtoCPdFxr98GYXQx3uIEtG50/ckMs5iAFd4Sz1f83fJ+1mqP4CvxDzS8461W0lhcwEe3wsRt1kuZ8hEICQ5vckKW5o0MvyzSXdfbBqf7iCygKDXNMXDX4qhcQ17ziptq2sIBSkmS+dY+NKw7Uys=")
