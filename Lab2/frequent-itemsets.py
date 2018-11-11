import numpy as np
from collections import defaultdict

#path to dataset
path = "../../SharedData/T10I4D100K.dat"

class FrequentItems:

    def __init__(self, folder_path, support=1, k_itemset= 3):
        self.folder_path = folder_path  # path to the transactions folder
        self.support = float(support)  # minimum support in percentage
        self.k_itemset = k_itemset    # size of the itemsets
        self.transactions = 0        # total number of transactions
        self.candidates = None      # dict of candidate itemsets

    def createCandidates(self):
        # load dataset and count frequency of singletons
        self.candidates = defaultdict(int)
        for line in open(self.folder_path, 'r'):
            items = line.split(" ")
            for item in items:
                self.candidates[item] += 1
                self.transactions += 1
        print(self.candidates)
        print(self.transactions)
        return self.candidates

    def pruneCandidates(self):
        keys_to_prune = list()
        for pair in self.candidates.items():
            if pair[1] < (self.transactions / float(100)) * self.support:
                keys_to_prune.append(pair[0])
        for key in keys_to_prune:
            del self.candidates[key]
        # pruning special char
        del self.candidates['\n']
        print(self.candidates)
        return self.candidates


a = FrequentItems(folder_path=path, support=0.3, k_itemset=2)
a.createCandidates()
a.pruneCandidates()
