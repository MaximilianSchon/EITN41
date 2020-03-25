import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)

lower_a = ['a', 'b', 'c', 'd', 'e', 'f']
num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
name = "Jonathan"
grade = "5"
all = lower_a + num
signature = ['0']*20
char_times = []
iterations = 5
idx = 0
while True:
    for c in all:
        signature[idx] = c
        time = 0
        for _ in range(iterations):
            URL = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name={}&grade={}&signature={}".format(name, grade,
                                                                                                         ''.join(
                                                                                                             signature))
            r = requests.get(url=URL, verify=False)
            time += r.elapsed.total_seconds()
        char_stats = (''.join(signature[:idx]) + c, time/iterations)
        if len(char_times) == idx:
            char_times.append([])
        char_times[idx].append(char_stats)
    char_times[idx] = sorted(char_times[idx], key=lambda part: part[1], reverse=True)
    signature[:idx] = char_times[idx][0][0]
    print(char_times[idx][0])
    if idx == 19:
        iterations += 1
        char_times[idx] = []
    if idx == 0 or char_times[idx][0][1] > char_times[idx-1][0][1]:
        idx += 1
        iterations = 3 if iterations <= 3 else iterations-1
    else:
        i = 0
        while i < idx and char_times[idx][0][1] < char_times[idx-(1+i)][0][1]:
            iterations += 1
            i += 1
            char_times[idx-i] = []
        char_times[idx] = []
        idx -= i
