import hashlib
import random
import matplotlib.pyplot as plt 


K = 2 ** 16


def hash(s, bits): # Hashes and truncates hash to decided amount of bits.
    return hex(int(bin(int(hashlib.sha1(s.encode('utf-8')).hexdigest(), 16))[2:bits+2], 2))[2:]


def bruteforce(h, X): # Returns the matching values for a specific hash
    return [(v, k) for v in [0, 1] for k in range(K) if hash(str(v) + str(k), X) == h] # It would be more efficient to replace with lookups in computed table


probabilities1 = []
probabilities2 = []
for i in range(5, 35):
    hashes = [[hash('0' + str(k), i) for k in range(K)], [hash('1' + str(k), i) for k in range(K)]] # Calculate a table of hashes according to specification
    probabilities1.append(0) if set(hashes[0]).isdisjoint(set(hashes[1])) else probabilities1.append(1) # Probability is either 100 % or 0 % because we can choose optimal pairs if they exist
    v = random.randint(0, 1)
    k = random.randint(0, K)
    probabilities2set = []
    for a in range(25):
        possibilities = bruteforce(hashes[v][k], i)
        probabilities2set.append((len([k1 for (v1, k1) in possibilities if v1 == v])/len(possibilities)))
    probabilities2.append(sum(probabilities2set)/len(probabilities2set))
plt.plot(range(5, 35), probabilities1)
plt.ylabel("Probabilities")
plt.title("Probability of finding two different commitments with the same hash")
plt.show()
plt.plot(range(5, 35), probabilities2)
plt.ylabel("Probabilities")
plt.title("Probability of finding the correct value of a commitment through bruteforcing")
plt.show()

