import numpy as np
from collections import defaultdict
from itertools import combinations

# path to dataset
path = "../../T10I4D100K.dat"

baskets_file = open(path, 'r')
i = 0
s = {'411', '579', '803'}
for line in baskets_file.readlines():
    items = set(line.split())
    if len(items.intersection(s)) == len(s):
        i += 1
print(i)

