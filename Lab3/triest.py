# TRIEST TRIangle Estimation from STreams
# @authors: Gabriele Prato & Luca Vavassori

# We are to implement the TRIEST-FD (Fully Dynamic)

import random

class Triest:

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


	def sample_edge_base(self, edge):

		if self.t  <= self.M:

			return True

		elif self.flip_biased_coin(self.M / float(self.t)):

				remove = random.sample(self.S, 1)
				self.S = self.S - set(remove)
				self.update_counters("-", remove[0], False)
				self.S.add(edge)
				return True

		return False


	def sample_edge_improved(self, edge):

		if self.t  <= self.M:

			return True

		elif self.flip_biased_coin(self.M / float(self.t)):

				remove = random.sample(self.S, 1)
				self.S = self.S - set(remove)
				self.S.add(edge)
				return True

		return False


	def sample_edge_fd(self, edge):

		if self.di + self.do == 0:

			if len(self.S) < self.M:

				print(self.t)
				self.S.add(edge)
				return True

			elif self.flip_biased_coin(self.M / float(self.t)):

				remove = random.sample(self.S, 1)
				self.update_counters("-", remove[0], False)
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


	def update_counters(self, sign, edge, weighted):

		if len(edge) < 2:
			print(edge, len(edge), type(edge))

		neighbours_intersection = self.get_neighbours(edge[0]).intersection(self.get_neighbours(edge[1]))

		for e in neighbours_intersection:

			if weighted:
				self.tau += max(1, (self.t - 1)*(self.t - 2)/float((self.M * (self.M - 1))))
			else:
				self.tau = self.tau - 1 if sign == '-' else self.tau + 1


	def base(self):

		for line in self.stream.readlines():

			e = ('+', tuple(line.split()))

			self.t += 1
			if self.sample_edge_base(e[1]):

					self.S.add(e[1])
					self.update_counters('+', e[1], False)

		print("Final Counter: ", self.tau)


	def improved(self):

		for line in self.stream.readlines():

			e = ('+', tuple(line.split()))

			self.t += 1
			self.update_counters(e[0], e[1], True)

			if self.sample_edge_base(e[1]):

					self.S.add(e[1])

		print("Final Counter: ", self.tau)


	def full_dynamic(self):

		for line in self.stream.readlines():

			sign = '+' if random.random() < 0.2 else '-'
			e = (sign, tuple(line.split()))

			self.t += 1
			self.s = self.s - 1 if e[0] == '-' else self.s + 1
			if e[0] == '+': 

				if self.sample_edge_fd(e[1]):

					print(self.t)
					self.update_counters('+', e[1], False)

			elif e[1] in self.S:

				self.update_counters('-', e[1], False)
				self.S - e[1]
				self.di += 1

			else:

				self.do += 1

		print("Final Counter: ", self.tau)


Triest("../../edges", M=20).improved()









