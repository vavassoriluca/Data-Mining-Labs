# Spectral Clustering
# @authors: Gabriele Prato & Luca Vavassori

import numpy as np
import scipy as sc
import networkx as nx
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import sys


class spectral_clustering:

	def __init__(self, stream_path):

		self.stream = open(stream_path, 'r')
		self.G = nx.Graph()


	def adjacency_mtrx(self):

		nodes = set()
		edges = list()

		for line in self.stream.readlines():

			line = [int(x) for x in line.strip().split(',')]
			nodes.add(line[0])
			nodes.add(line[1])
			edges.append((line[0], line[1]))

		self.nodes = sorted(list(nodes))
		self.n = len(self.nodes)
		self.G.add_nodes_from(self.nodes)
		self.G.add_edges_from(edges)

		adj_mtrx = np.zeros((self.n, self.n))

		self.stream.seek(0)

		for e in edges:

			idx = [self.nodes.index(int(x)) for x in e]
			adj_mtrx[idx[0], idx[1]] = 1
			adj_mtrx[idx[1], idx[0]] = 1

		nx.draw(self.G, node_size=30, pos=nx.spring_layout(self.G, k=0.05, iterations=20))
		plt.show()

		return adj_mtrx


	def laplacian(self, adj_mtrx):

		D_vector = adj_mtrx.sum(axis=1)
		D_sqrt = np.sqrt(D_vector)
		D = np.diag(D_sqrt)
		D_inverted = np.linalg.inv(D)
		L = np.matmul(np.matmul(D_inverted, adj_mtrx), D_inverted)

		return L


	def clustering(self):

		# Compute adjacency matrix
		adj_mtrx = self.adjacency_mtrx()

		# Compute laplacian
		laplacian = self.laplacian(adj_mtrx)

		# Compute eigenvalues & eigenvectors
		eigenvalues, eigenvectors = sc.linalg.eigh(laplacian)

		# Find optimal k
		k = np.argmin(np.ediff1d(np.flipud(eigenvalues))) + 1
		X = eigenvectors[:, self.n - k:]

		#Construct matrix Y by renormalizing X
		Y = np.divide(X, np.reshape(np.linalg.norm(X, axis=1), (X.shape[0], 1)))

		#Cluster rows of Y into k clusters using K-means
		kmeans = KMeans(n_clusters=k, random_state=0).fit(Y)

		#Assign original point i to the cluster of the row i of matrix Y
		print(len(kmeans.labels_), len(self.G))
		nx.draw(self.G, node_size=30, pos=nx.spring_layout(self.G, k=0.05, iterations=20), node_color=kmeans.labels_)
		plt.show()

		return kmeans


def main():

    args = list()
    args.append("../../example2.dat") # path to dataset 

    i = 0

    for arg in sys.argv[1:]:
        args[i] = arg 
        i += 1
        if i > 1:
            break

    spectral = spectral_clustering(args[0]).clustering()


if __name__ == "__main__":
    main()








