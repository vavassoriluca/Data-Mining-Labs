import os
import io
import binascii
import random
from collections import defaultdict
from itertools import combinations
import numpy as np
import sys



class SimilarItems:


	def __init__(self, folder_path, shingle_sim=False, signature_sim=False, lsh_sim=True, k_shingles=5, num_hashes=30, bands=10, treshold=0.3):
		
		self.folder_path = folder_path									# path to the documents folder
		self.documents = os.listdir(self.folder_path)					# names of documents
		self.shingle_sim = shingle_sim 									# boolean: compute the similarity using shingles
		self.signature_sim =  signature_sim 							# boolean: compute the similarity using signatures
		self.lsh_sim = lsh_sim											# boolean: compute the similarity using lsh
		self.k_shingles = int(k_shingles)								# number of words in a shingle
		self.num_hashes = int(num_hashes)								# number of hashes in the MinHash step
		self.treshold = float(treshold)									# minimum similarity level to keep or discard pairs
		self.bands = int(bands)                                         # number of bands in the LSH step
		self.signature_matrix = [0 for i in range(self.num_hashes)]    	# matrix of signatures
		self.shingles = list() 											# list of sets of shingles 

	# Function to compute the set of k-shingles for a document
	def get_k_shingles(self, file_text):

		tokens = file_text.split()
		return sorted(set([binascii.crc32(str.encode("".join(tokens[i:i+self.k_shingles]))) & 0xffffffff for i in range(len(tokens) - self.k_shingles + 1)]))

	# Compare two sets of k-shingles using Jaccard Similarity
	def shingles_similarity(self, a, b):

		intersection = len(list(set(a).intersection(b)))
		union = (len(a) + len(b)) - intersection
		if union == 0:
			return 0.0
		return intersection / float(union)

	# Get as many pairs of parameters as the number of hash functions
	def get_hash_coefficients(self):

		max_interval = 2**32-1
		a = random.sample(range(0,max_interval+1),self.num_hashes)
		b = random.sample(range(0,max_interval+1),self.num_hashes)
		return a, b

	# Compute the signature out of a set of shingles
	def signature(self, shingles, a, b): 

		c = 4294967311 # prime number bigger than max_interval
		min_hash = c + 1
		signature = []

		for i in range(self.num_hashes):
			for shingle in shingles:
				hash_code = (a[i] * shingle + b[i]) % c 
				if hash_code < min_hash:
					min_hash = hash_code

			signature.append(min_hash)
			min_hash = c + 1

		return signature

	# Compare two signatures
	def compare_signatures(self, a, b):

		equal = 0		
		for i in range(len(a)):
			if(a[i]==b[i]):
				equal += 1

		return equal/len(a)

	# Implement the LSH algorithm and compare the documents using it
	def compare_lsh(self, matrix, b):

		similar_items = defaultdict(int)

		if self.treshold == None:
			self.treshold = (1/b)**(1/matrix.shape[0])
		r = int((matrix.shape[0] + b - 1) / b)

		# Check the value of the number of bands
		if b > matrix.shape[0]:
			b = matrix.shape[0]
		elif b < matrix.shape[0] and b > int((matrix.shape[0] + 1) / 2):
			b =  int((matrix.shape[0] + 1) / 2)
			print(b)

		for band in range(b):

			# Set the limit of the indices
			i = r*band if r*band <= matrix.shape[0] else matrix.shape[0]
			j = r*(band+1) if r*(band+1) <= matrix.shape[0] else matrix.shape[0]
			
			lsh_dict = defaultdict(list)

			# Hash the band
			for col in range(matrix.shape[1]):
				band_hash = binascii.crc32(str.encode("".join(matrix[i:j, col].astype("str"))))  & 0xffffffff
				lsh_dict[band_hash].append(col)

			# Filter the buckets with more than 1 document and count the occurencies of couples
			for v in lsh_dict.values():

				if len(v) > 1:
					candidates = combinations(v, 2)
					for c in candidates:
						similar_items[c] += 1			
		
		return {(self.documents[key[0]], self.documents[key[1]]):value/float(b) for (key,value) in similar_items.items() if value/float(b) > self.treshold}

	# Driver of the computation
	# Iterate over all document to computer shingles and signatures and call the comparison funcions
	def start(self):

		a,b = self.get_hash_coefficients()
		
		for filename in self.documents:
			file = open(self.folder_path + '/' + filename, 'r')
			try:
				shingle = self.get_k_shingles(file.read())
				if self.shingle_sim:
					self.shingles.append(shingle)
				if self.signature_sim or self.lsh_sim:
					self.signature_matrix = np.column_stack((self.signature_matrix, self.signature(shingle, a, b)))
			except:
				print("Can't read the file: " + filename)

		if (self.signature_sim or self.lsh_sim) and type(self.signature_matrix) is not list:
			self.signature_matrix = np.delete(self.signature_matrix,0,axis = 1)

		if self.lsh_sim:
			print("\n", "+++++ LSH +++++","\n")
			for p in self.compare_lsh(self.signature_matrix, self.bands).items():
				print(str(p[0]) + ": " + str(p[1]))

		if self.signature_sim:
			print("\n", "+++++ MIN-HASH +++++","\n")
			for i in range(self.signature_matrix.shape[1]):
				for j in range(self.signature_matrix.shape[1]):
					if i < j:
						value = self.compare_signatures(np.squeeze(self.signature_matrix[:,i]), np.squeeze(self.signature_matrix[:,j]))
						if value > self.treshold:
							print("(" + str(self.documents[i]) + "," + str(self.documents[j]) + "): " + str(value))

		if self.shingle_sim:
			print("\n", "+++++ SHINGLES +++++","\n")
			for i in range(len(self.shingles)):
				for j in range(len(self.shingles)):
					if i < j:
						value = self.shingles_similarity(self.shingles[i], self.shingles[j])
						if value > self.treshold:
							print("(" + str(self.documents[i]) + "," + str(self.documents[j]) + "): " + str(value))



def main():

	args = list()
	args.append("data/")
	args.append(False)
	args.append(False)
	args.append(True)
	args.append(5)
	args.append(30)
	args.append(10)
	args.append(0.3)

	i = 0

	for arg in sys.argv[1:]:
		if arg == "True":
			args[i] = True
		elif arg == "False":
			args[i] = False
		else:
			args[i] = arg 
		i += 1
		if i > 7:
			break

	SimilarItems(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7]).start()

if __name__ == "__main__":
    main()	










    