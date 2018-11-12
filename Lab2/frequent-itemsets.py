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
        self.temp_k = 2           # incremental k
        self.pruned = []         # eliminated items
        self.fatherArray = []   # saving variable for progress



    def createCandidates(self):
        # load dataset and count frequency of singletons
        self.candidates = defaultdict(int)
        returnSet = []
        for line in open(self.folder_path, 'r'):
            items = line.split(" ")
            self.transactions += 1
            for item in items:
                self.candidates[item] += 1
        print(self.candidates)
        print(self.transactions)
        del self.candidates["\n"]
        for key in self.candidates:
            temp = []
            temp.append(key)
            returnSet.append(temp)
            returnSet.append(self.candidates[key])
            temp = []
        self.singletons = list(self.candidates.keys())
        return returnSet



    def generateFrequentItems(self, candidateList):
        # start generalizing to k steps using sets
        frequents = []
        print("trying new cycle!")
        for i in range(len(candidateList)):
            if i%2 != 0:
                if candidateList[i] >= (self.transactions / float(100)) * self.support:
                    frequents.append(candidateList[i-1])
                    frequents.append(candidateList[i])
                else:
                    self.pruned.append(candidateList[i-1])
        for element in frequents:
            self.fatherArray.append(element)
        if len(frequents) == 2 or len(frequents) == 0:
            # print("This will be returned")
            return self.fatherArray
        else:
            print("frequent ItemsSets:  " + "\n")
            print(frequents)
            self.createKCandidates(frequents)



    def createKCandidates(self, frequents):
        elementKeys = []
        combinations = []
        candidateSet = []
        for element in range(len(frequents)):
            if element % 2 == 0:
                elementKeys.append(frequents[element])
        for item in elementKeys:
            temp = []
            k = elementKeys.index(item)
            for i in range(k + 1, len(elementKeys)):
                for j in item:
                    if j not in temp:
                        temp.append(j)
                for m in elementKeys[i]:
                    if m not in temp:
                        temp.append(m)
                combinations.append(temp)
                temp = []
        sortedCombinations = []
        uniqueCombinations = []
        for i in combinations:
            sortedCombinations.append(sorted(i))
        for i in sortedCombinations:
            if i not in uniqueCombinations:
                uniqueCombinations.append(i)
        combinations = uniqueCombinations
        for tuples in combinations:
            counter = 0
            for line in open(self.folder_path, 'r'):
                items = line.split(" ")
                if set(tuples).issubset(set(items)):
                    counter += 1
                if counter != 0:
                    candidateSet.append(tuples)
                    candidateSet.append(counter)
        print("candidate sets:  " + "\n")
        print(candidateSet)
        self.generateFrequentItems(candidateSet)



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




    '''
    def createPowerSets(self, candidates):
        # create a powerset of order k_itemset
        num = len(candidates)
        powerset = []
        for i in range(1, 1 << num):
            list = [candidates[j] for j in range(num) if (i & (1 << j))]
            if len(list) == self.temp_k:
                powerset.append(list)
        print(powerset)
        return powerset


    def countKsupport(self, powerset, candidates):
        for item in powerset:
            for line in open(self.folder_path, 'r'):
                items = line.split(" ")
                self.createPowerSets(items)





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
'''

a = FrequentItems(folder_path=path, support=2, k_itemset=2)
first_step = a.createCandidates()
a.generateFrequentItems(first_step)
