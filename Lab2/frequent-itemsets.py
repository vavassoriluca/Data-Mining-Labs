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
        self.candidates = None      # candidate itemsets
        self.singletons = []       # list of candidate singletons



    def createCandidates(self):
        # load dataset and count frequency of singletons
        self.candidates = defaultdict(int)
        for line in open(self.folder_path, 'r'):
            items = line.split(" ")
            self.transactions += 1
            for item in items:
                self.candidates[item] += 1
        print(self.candidates)
        print(self.transactions)
        self.singletons = list(self.candidates.keys())
        return self.candidates



    def pruneCandidates(self):
        # eliminates all candidates that fall under the support treshold
        keys_to_prune = list()
        for pair in self.candidates.items():
            if pair[1] < (self.transactions / float(100)) * self.support:
                keys_to_prune.append(pair[0])
        for key in keys_to_prune:
            del self.candidates[key]
        # pruning special char
        del self.candidates['\n']
        self.candidates = list(self.candidates.keys())
        print(self.candidates)
        return self.candidates



    def createPowerSets(self):
        # create a powerset of order k_itemset
        num = len(self.candidates)
        powerset = []
        for i in range(1, 1 << num):
            list = [self.candidates[j] for j in range(num) if (i & (1 << j))]
            if len(list) == self.k_itemset:
                powerset.append(list)
        print(powerset)
        return powerset



    def hasFrequentSubsets(self):
        # check if all subsets of the itemset are also frequent
        subsets = self.createPowerSets()
        for subset in subsets:
            frequent_subset = False
            for item in self.candidates:
                if set(subset) == set(item[0].split(",")):
                    frequent_subset = True
                    print(frequent_subset)
                    break
                if frequent_subset == False:
                    print(frequent_subset)
                    return False
        return True


    def generateAprioriCandidates(self):
        C = []
        for l1 in self.singletons:
            for l2 in self.singletons:
                first_itemlist = l1[0].split(",")
                second_itemlist = l2[0].split(",")
                i = 0
                flag = True
                while i <= self.k_itemset - 2 - 1:
                    if first_itemlist[i] != second_itemlist[i]:
                        flag = False
                        break
                    i += 1
                if not first_itemlist[self.k_itemset - 1 - 1] < second_itemlist[self.k_itemset - 1 - 1]:
                    flag = False
                if flag == True:
                    c = sorted(set(first_itemlist) | set(second_itemlist))
                    self.k_itemset = self.k_itemset - 1
                    if self.hasFrequentSubsets():
                        C.append(",".join(list(c)))
        print(C)
        return C


a = FrequentItems(folder_path=path, support=1, k_itemset=5)
a.createCandidates()
a.pruneCandidates()
a.generateAprioriCandidates()
