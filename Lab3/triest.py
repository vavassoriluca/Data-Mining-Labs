# TRIEST TRIangle Estimation from STreams
# @authors: Gabriele Prato & Luca Vavassori

# We are to implement the TRIEST-FD (Fully Dynamic)

import random
import operator

class TriestFD:

	def __init__(self, stream_path, M=6):

		self.M = M
		self.S = set()
		self.t = 0
		self.s = 0
		self.di = 0
		self.do = 0
		self.tau = 0

		self.stream = open(stream_path, 'r')


	def flip_biased_coin(self, p):

		return True if random.random() < p else False



	def sample_edge(self, edge):

		if self.di + self.do == 0:

			if len(self.S) < self.M:

				print(self.t)
				self.S.add(edge)
				return True

			elif self.flip_biased_coin(self.M / float(self.t)):

				print("HO SOSTITUITO")
				remove = random.sample(self.S, 1)
				self.update_counters("-", remove[0])
				self.S = self.S - set(remove)
				self.S.add(edge)
				return True

		elif self.flip_biased_coin(self.di / float(self.di + self.do)):

			self.S.add(edge)
			self.di -= 1
			return True

		else:

			self.do -= 1
			return False


	def get_neighbours(self, vertex):

		neighbours = set()

		for t in self.S:

			if vertex in t:

				neighbours.add(t[0])
				neighbours.add(t[1])

		return neighbours - set(vertex)


	def update_counters(self, sign, edge):

		if len(edge) < 2:
			print(edge, len(edge), type(edge))

		neighbours_intersection = self.get_neighbours(edge[0]).intersection(self.get_neighbours(edge[1]))

		for e in neighbours_intersection:

			self.tau = self.tau - 1 if sign == '-' else self.tau + 1


	def start(self):

		for line in self.stream.readlines():

			sign = '+' if random.random() < 0.5 else '-'
			e = (sign, tuple(line.split()))

			self.t += 1
			self.s = self.s - 1 if e[0] == '-' else self.s + 1
			if e[0] == '+': 

				if self.sample_edge(e[1]):

					print(self.t)
					self.update_counters('+', e[1])

			elif e[1] in self.S:

				self.update_counters('-', e[1])
				self.S - e[1]
				self.di += 1

			else:

				self.do += 1

		print("FINISH: ", self.tau)


TriestFD("../../edges").start()








