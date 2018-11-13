import numpy as np
from collections import defaultdict
from itertools import combinations

# path to dataset
path = "../../T10I4D100K.dat"

baskets_file = open(path, 'r')
i = 0
j = 0
s1 = {'350', '572', '411', '579'}
s2 = {'350', '572', '411', '579', '803'}
for line in baskets_file.readlines():
    items = set(line.split())
    if len(items.intersection(s1)) == len(s1):
        i += 1
    if len(items.intersection(s2)) == len(s2):
    	j += 1
print(str(sorted(s1)) + " -> " + str(sorted(s2-s1)) + " : " + str(j / float(i)))

