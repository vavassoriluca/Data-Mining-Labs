# TRIEST TRIangle Estimation from STreams
# @authors: Gabriele Prato & Luca Vavassori

# We are to implement the TRIEST-FD (Fully Dynamic)

import random
import sys
from collections import defaultdict

class Triest:

	def __init__(self, stream_path, M=6):

		self.M = M
		self.stream = open(stream_path, 'r')


	def reset(self):

		print("Resetting the variables: ")

		self.S = set()
		self.t = 0
		self.s = 0
		self.di = 0
		self.do = 0
		self.tau = 0
		self.tau_local = defaultdict(int)

		print("S: {}, t: {}, tau: {}".format(self.S, self.t, self.tau))


	def flip_biased_coin(self, p):

		return True if random.random() < p else False


	def sample_edge_base(self, edge):

		if self.t  <= self.M:

			return True

		elif self.flip_biased_coin(self.M / float(self.t)):

				remove = self.S.pop()
				self.S.remove(remove)
				self.update_counters("-", remove, False)
				return True

		return False


	def sample_edge_improved(self, edge):

		if self.t  <= self.M:

			return True

		elif self.flip_biased_coin(self.M / float(self.t)):

				#remove = random.sample(self.S, 1)[0]
				remove = self.S.pop()
				self.S.remove(remove)
				return True

		return False


	def sample_edge_fd(self, edge):

		if self.di + self.do == 0:

			if len(self.S) < self.M:

				self.S.add(edge)
				return True

			elif self.flip_biased_coin(self.M / float(self.t)):

				remove = self.S.pop()
				self.update_counters("-", remove, False)
				self.S.remove(remove)
				self.S.add(edge)
				return True

		elif self.flip_biased_coin(self.di / float(self.di + self.do)):

			self.S.add(edge)
			self.di -= 1
			return True

		else:

			self.do -= 1
			return False


	def get_neighbours(self, edge):

		neighbours_u = set()
		neighbours_v = set()

		for t in self.S:

			if t[0] == edge[0]:
				neighbours_u.add(t[1])
			if t[1] == edge[0]:
				neighbours_u.add(t[0])
			if t[0] == edge[1]:
				neighbours_v.add(t[1])
			if t[1] == edge[1]:
				neighbours_v.add(t[0])

		return neighbours_u, neighbours_v


	def update_counters(self, sign, edge, weighted):

		neighbours_u, neighbours_v = self.get_neighbours(edge)
		neighbours_intersection = neighbours_u & neighbours_v

		if weighted:
			weight = (self.t - 1)*(self.t - 2)/float((self.M * (self.M - 1)))

		for e in neighbours_intersection:

			if weighted:

				if weight < 1:
					weight = 1
				self.tau += weight
				self.tau_local[e] += weight
				self.tau_local[edge[0]] += weight
				self.tau_local[edge[1]] += weight

			else:

				self.tau = self.tau - 1 if sign == '-' else self.tau + 1
				self.tau_local[e] = self.tau_local[e] - 1 if sign == '-' else self.tau_local[e] + 1
				self.tau_local[edge[0]] = self.tau_local[edge[0]] - 1 if sign == '-' else self.tau_local[edge[0]] + 1
				self.tau_local[edge[1]] = self.tau_local[edge[1]] - 1 if sign == '-' else self.tau_local[edge[1]] + 1

			if self.tau_local[e] == 0:
				del self.tau_local[e]
			if self.tau_local[edge[0]] == 0:
				del self.tau_local[edge[0]]
			if self.tau_local[edge[1]] == 0:
				del self.tau_local[edge[1]]


	def base(self):

		self.stream.seek(0)
		self.reset()

		for line in self.stream.readlines():

			line = line.split()
			line = sorted([int(line[0]), int(line[1])])
			e = ('+', tuple(line))

			self.t += 1
			if self.sample_edge_base(e[1]):

					self.S.add(e[1])
					self.update_counters('+', e[1], False)

		epsilon = max(1, (self.t*(self.t-1)*(self.t-2))/(self.M*(self.M-1)*(self.M-2)))

		print("Global counter: ", self.tau*epsilon)
		#print("Local counters: ", self.tau_local)


	def improved(self):

		self.stream.seek(0)
		self.reset()

		for line in self.stream.readlines():

			line = line.split()
			line = sorted([int(line[0]), int(line[1])])
			e = ('+', tuple(line))
			self.t += 1
			self.update_counters('+', e[1], True)
			if self.sample_edge_improved(e[1]):

					self.S.add(e[1])

		epsilon = max(1, (self.t*(self.t-1)*(self.t-2))/(self.M*(self.M-1)*(self.M-2)))

		print("Global counter: ", self.tau*epsilon)
		#print("Local counters: ", self.tau_local)


	def full_dynamic(self):

		self.stream.seek(0)
		self.reset()

		for line in self.stream.readlines():

			sign = '+' if random.random() < 1 else '-'

			line = line.split()
			line = sorted([int(line[0]), int(line[1])])
			e = (sign, tuple(line))

			self.t += 1
			self.s = self.s - 1 if e[0] == '-' else self.s + 1
			if e[0] == '+': 

				if self.sample_edge_fd(e[1]):

					self.update_counters('+', e[1], False)

			elif e[1] in self.S:

				self.update_counters('-', e[1], False)
				self.S - set(e[1])
				self.di += 1

			else:

				self.do += 1

		epsilon = max(1, (self.t*(self.t-1)*(self.t-2))/(self.M*(self.M-1)*(self.M-2)))

		print("Global counter: ", self.tau*epsilon)
		#print("Local counters: ", self.tau_local)

def main():

    args = list()
    args.append("../../edges") # path to dataset 
    args.append(20)       # percentage to compute min_support
    args.append("all")      # precentage to compute confidence for rules

    i = 0

    for arg in sys.argv[1:]:
        args[i] = arg 
        i += 1
        if i > 2:
            break

    t = Triest(args[0], int(args[1]))

    print("TRIEST: Counting Triangles in Graphs\n\n")

    if args[2] == "all":

    	print("--------------------")
    	print("BASE")
    	print("--------------------")
    	print("\n")
    	t.base()
    	print("\n\n")

    	print("--------------------")
    	print("IMPROVED")
    	print("--------------------")
    	print("\n")
    	t.improved()
    	print("\n\n")

    	print("--------------------")
    	print("FULLY DYNAMIC")
    	print("--------------------")
    	print("\n")
    	t.full_dynamic()

    elif args[2] == "base":

    	print("--------------------")
    	print("BASE")
    	print("--------------------")
    	print("\n")
    	t.base()
    	print("\n\n")

    elif args[2] == "improved":

    	print("--------------------")
    	print("IMPROVED")
    	print("--------------------")
    	print("\n")
    	t.improved()
    	print("\n\n")

    elif args[2] == "fd":

    	print("--------------------")
    	print("FULLY DYNAMIC")
    	print("--------------------")
    	print("\n")
    	t.full_dynamic()
    	print("\n\n")


if __name__ == "__main__":
    main()








