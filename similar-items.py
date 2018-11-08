import os
import binascii
import random

class Shingling:

	def k_shingles(k, file_text):

		tokens = file_text.split()
		return sorted(set([binascii.crc32(str.encode("".join(tokens[i:i+k]))) & 0xffffffff for i in range(len(tokens) - k + 1)]))

class CompareSets:

	def similarity(a, b):

		intersection = len(list(set(a).intersection(b)))
		union = (len(a) + len(b)) - intersection
		return intersection / union

class MinHashing:

	def getHashCoefficients(k):

		maxShingleID = 2**32-1
		a = random.sample(range(0,maxShingleID+1),k)
		b = random.sample(range(0,maxShingleID+1),k)
		return a, b

	def signature(shingles, k, a, b): 

		c = 4294967311
		minHash = c + 1
		signature = []

		for i in range(k):
			for shingle in shingles:
				hashCode = (a[i] * shingle + b[i]) % c 
				if hashCode < minHash:
					minHash = hashCode

			signature.append(minHash)

		return signature

class CompareSignatures:

	def compare(a,b):

		equal = 0		
		for i in range(len(a)):
			if(a[i]==b[i]):
				equal += 1

		return equal/len(a)


def compareDocs(a,b, k_shingles, num_hashes):

	shingles_a = Shingling.k_shingles(k_shingles,a)
	shingles_b = Shingling.k_shingles(k_shingles,b)

	coeff_a, coeff_b = MinHashing.getHashCoefficients(num_hashes)
	sign_a = MinHashing.signature(shingles_a, num_hashes, coeff_a, coeff_b)
	sign_b = MinHashing.signature(shingles_b, num_hashes, coeff_a, coeff_b)

	return CompareSignatures.compare(sign_a,sign_b)



#class LSH:

	# t = (1/b)**(1/r)
	# n = b*r


#folder_path = "../20_newsgroups/rec.sport.baseball" 
folder_path = "../custom_documents/"
file_path_a = os.listdir(folder_path)[2]
file_path_b = os.listdir(folder_path)[1]
file_a = open(folder_path + "/" + file_path_a, "r")
file_b = open(folder_path + "/" + file_path_b, "r")
a = file_a.read()
b = file_b.read()
file_a.close()
file_b.close()

print(compareDocs(a,b,5,100))
print(CompareSets.similarity(Shingling.k_shingles(5,a),Shingling.k_shingles(5,b)))


    