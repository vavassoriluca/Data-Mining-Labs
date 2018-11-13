import numpy as np
from collections import defaultdict
from itertools import combinations

# path to dataset
path = "../../T10I4D100K.dat"

class FrequentItems:
    
    def __init__(self, file_path, min_support = 1):
        self.file_path = file_path          # path to the transactions folder
        self.min_support = float(min_support)       # minimum support in percentage
        self.transactions = 0               # total number of transactions
        self.candidates = []                # candidate itemsets
        self.singletons = []                # list of candidate singletons
        self.temp_k = 2                     # incremental k
        try:
            self.baskets_file = open(self.file_path, 'r')
        except:
          print("Can't read the file...")

    # Eliminates all candidates that fall under the support treshold
    def prune_candidates(self, itemset):

        treshold = (self.transactions / float(100)) * self.min_support
        return {k: v for k,v in itemset.items() if v >= treshold}

    # Return the set of elements of a list of tuples
    def flatten_tuples(self, tuples):

        return {item for t in tuples for item in t}

    # Given a list of tuples of length k, create all the possible tuples of length k+1 from the given ones
    # if the original tuples have at least k-1 common elements
    def create_k_itemset(self, tuples):
        
        k_itemset = set()

        for i in range(len(tuples)):
            for j in range(len(tuples)):
                if i < j:
                    a = {e for e in tuples[i]}
                    b = {e for e in tuples[j]}
                    intersection = a.intersection(b)
                    if len(intersection) == len(a) - 1:
                        union = sorted(a.union(b))
                        for c in combinations(union, len(a) + 1):
                            k_itemset.add(c)

        return k_itemset
                
    # Given the list of candidates with length k-1 from the previous step (parameter: source)
    # compute the candidates of the current step with lenght k using the a-priori algorithm
    # to output the candidates with a support greater or equal to the given min-support 
    # K = 1, no previous list of candidates
    # k = 2, special case, previous candidates are not tuples, faster implementation without the general k algorithm
    # k = n, n > 2 general case
    def k_itemset_candidates(self, source, k):
        
        k_candidates = defaultdict(int)
        self.baskets_file.seek(0)
    
        if k == 1:
            i = 0
            for line in self.baskets_file.readlines():
                items = line.split()
                self.transactions += 1
                for item in items:
                    k_candidates[item] += 1
                i += 1
            print("Number of transactions observed: " + str(self.transactions))
            print("Number of unique items observed: " + str(len(k_candidates.items())))
            self.candidates.append(self.prune_candidates(k_candidates))

        elif k == 2:
            source_set = set(source)
            for line in self.baskets_file.readlines():
                line_set = set(line.split())
                # Get the elements of the line with a support greater or equal to the min-support
                intersection = line_set.intersection(source_set)
                # Create all the couples from those elements if the length of the intersection is at least k (2)
                combs = combinations(sorted(intersection), k) if len(intersection) >= k else list()
                # Sum 1 to the counter of each combination
                for c in combs:
                    k_candidates[c] += 1
            self.candidates.append(self.prune_candidates(k_candidates))
        
        else :
            source_set = set(source)
            flat_source = self.flatten_tuples(source)
            for line in self.baskets_file.readlines():
                line_set = set(line.split())
                # Get the elements of the line with a support greater or equal to the min-support that are in the
                # elements the tuples of the previous step are made of
                pre_intersection = line_set.intersection(flat_source)
                # Create all the possible tuples of length k-1 from those elements
                pre_combs = combinations(sorted(pre_intersection), k-1) if len(pre_intersection) >= k  else list()
                # Intersect those tuples with the ones in the previous step to check if in this line there are tuples
                # from the candidates of the previous step
                intersection = set(pre_combs).intersection(source_set)
                if len(intersection) > 1:
                    # Implementation of a-priori with small modification, faster
                    combs = combinations(sorted(self.flatten_tuples(intersection)), k)
                    # Strict implementation of a-priori algorithm, but slower
                    #combs = self.create_k_itemset(list(intersection))
                    for c in combs:
                        k_candidates[c] += 1
            self.candidates.append(self.prune_candidates(k_candidates))
        
    # Start the genration of candidates
    def generate_apriori_candidates(self):

        i = 1
        while True:
            if i == 1:
                self.k_itemset_candidates(None, i)
            else :
                self.k_itemset_candidates(self.candidates[i - 2].keys(), i)
            print("\nStep " + str(i) + " candidates:", self.candidates[i - 1])

            if(len(self.candidates[i - 1].items()) == 0):
                print("\nEnd of computation. Number of steps performed: " + str(i), "\n\n\n\n")
                return self.candidates[:-1]
            i += 1 

class AssociationRules:

    def __init__(self, itemsets, confidence=10):

        self.itemsets = itemsets
        self.confidence = confidence / float(100)
        self.associations = dict()

    def find_associations(self):

        print("ASSOCIATION RULES\n")

        for i in range(len(self.itemsets) - 1):
            itemset = self.itemsets[::-1][i]
            for t in itemset.items():
                items = {s for s in t[0]}
                support = t[1]
                for j in range(len(items))[::-1][:-1]:
                    if j == 1:
                        combs = items
                    else:
                        combs = combinations(sorted(items), j)
                    for c in combs:
                        if j == 1:
                            subsetA = set()
                            subsetA.add(c)
                            supportA = self.itemsets[0][c]
                        else:
                            subsetA = {s for s in c}
                            supportA = self.itemsets[len(subsetA)-1][tuple(sorted(subsetA))]
                        subsetB = sorted(items - subsetA)
                        if j == len(items) - 1:
                            subsetB = list(subsetB)[0]
                        else:
                            subsetB = tuple(subsetB)
                        confidence = support / float(supportA)
                        if confidence >= self.confidence:
                            if len(subsetA) == 1:
                                subsetA = list(subsetA)[0]
                            else:
                                subsetA = tuple(subsetA)
                            string = str(subsetA) + " -> " + str(subsetB)
                            print(string + " : " + str(confidence))
                            self.associations[string] = confidence


a = FrequentItems(file_path=path, min_support=0.5)
AssociationRules(a.generate_apriori_candidates(), 90).find_associations()