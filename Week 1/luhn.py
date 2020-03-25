import math

def luhn(s):
    idx = True
    sum = 0
    for c in s:
        if c.isdigit():
            val = int(c)
            if idx:
                if val < 5:
                    val = val*2
                else:
                    val = val*2 - 9
            sum += val
        idx = not idx
    closest = int(round(sum / 10.0)) * 10
    return closest == sum


def bruteforce(s):
    correct = -1
    for i in range(10):
        num = str(i)
        n = s.replace("X", num)
        if luhn(n):
            correct = i
    return correct


res = ""
for line in inp.splitlines():
    res += str(bruteforce(line))

print(res)
