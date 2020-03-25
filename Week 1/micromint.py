import random
import statistics

# c = coins to generate
# u = number of bits in a bin
# k = collision threshold


def generatecoins(c, u, k):
    buckets = [0] * 2 ** u
    generated = 0
    iterations = 0
    while generated < c:
        bucket = random.randint(0, len(buckets)-1)
        buckets[bucket] += 1
        iterations += 1
        if buckets[bucket] == k:
            generated += 1
    return iterations


def calculateinterval(data):
    l = 3.66
    s = statistics.stdev(data)
    n = len(data)
    mean = statistics.mean(data)
    return [mean - l*s/statistics.sqrt(n), mean + l*s/statistics.sqrt(n)]


amt_sim = 0
c = 0
u = 0
k = 0
ciwidth = 0
res = []
width = ciwidth + 1    # Whatever value over ciwidth
while width >= ciwidth:
    res += [generatecoins(c, u, k)]
    if len(res) > 1:
        interval = calculateinterval(res)
        width = interval[1] - interval[0]

print(round(statistics.mean(interval)))
