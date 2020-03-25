x = 1
func = 6 + 12*x + 7*x**2 + 0*x**3 + 0*x**4

points = [func, 38, 12, 50]
mypoint = sum(points)

sums = [
    -1, mypoint, -1, 585, 953, -1, -1 # The first point will never be valid
]


def domath():
    members = [i for i in range(len(sums)) if sums[i] != -1]
    sum = 0
    print(members)
    for i in members:
        prod = sums[i] # f(i)
        for j in members:
            if j != i: # set of t without i
                prod *= j/(j - i) # product of all j:s except i
        sum += prod
    print(sum)


domath()

