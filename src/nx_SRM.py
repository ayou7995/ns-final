import matplotlib.pyplot as plt 
import sys
import numpy as np
import time
import csv
import time
import networkx as nx
import random
import operator
import numpy as np
import itertools
S = 0
I = 1





class Split:
    def __init__(self, G, k, alpha, m = 1, topology = 'clique'):
        self.G = G.copy()
        self.alpha = alpha
        self.k = k
        self.m = m
        self.topology = topology
        self.n_list = sorted(G.degree().items(), key=operator.itemgetter(1), reverse=True)

    def build_clique(self, node):
        H = nx.Graph()
        n_list = list(map(lambda i: node + '-' + str(i),  np.arange(self.k)))
        e_list = list(itertools.combinations(n_list, 2))
        for item in e_list:
            H.add_edge(str(item[0]), str(item[1]))
        return H

    def build_ring(self, node):
        H = nx.Graph()
        n_list = list(map(lambda i: node + '-' + str(i),  np.arange(self.k)))
        e_list = []
        for i in range(len(n_list)):
            e_list.append([n_list[i-1], n_list[i]])
        for item in e_list:
            H.add_edge(str(item[0]), str(item[1]))
        return H

    def build_star(self, node):
        H = nx.Graph()
        n_list = list(map(lambda i: node + '-' + str(i),  np.arange(self.k)))
        e_list = []
        for i in range(len(n_list)-1):
            e_list.append([n_list[0], n_list[i+1]])
        for item in e_list:
            H.add_edge(str(item[0]), str(item[1]))
        return H

    def build_tree(self, node):
        H = nx.Graph()
        n_list = list(map(lambda i: node + '-' + str(i),  np.arange(self.k)))
        e_list = []
        for i in range(1,len(n_list)):
            if i % 2 != 0 : 
                e_list.append([n_list[i], n_list[int((i-1)/2)]])
            else :
                e_list.append([n_list[i], n_list[int((i-2)/2)]])
        for item in e_list:
            H.add_edge(str(item[0]), str(item[1]))
        return H

    def join_graph(self, node):
        neighbors = self.G.neighbors(node)
        if len(neighbors) < self.k:
            return
        if self.topology == 'clique':
            H = self.build_clique(node)
        if self.topology == 'ring':
            H = self.build_ring(node)
        if self.topology == 'star':
            H = self.build_star(node)
        if self.topology == 'tree':
            H = self.build_tree(node)
        count  = 0
        for i in range(self.k):
            s = int(len(neighbors)*i/self.k)
            e = int((len(neighbors)*(i+1)/self.k))
            sub = neighbors[s:e]
            for j in range (self.m):

                for n in sub :
                    
                    count += 1
                    self.G.add_edge(H.nodes()[ (i + j) % self.k], n)
        self.G.remove_node(node)
        self.G = nx.compose(self.G ,H) 

    def run(self):
        length = int(self.alpha*len(self.n_list))
        core = self.n_list[:length]
        if self.k < self.m :
            raise ValueError('The replica = {0} most smaller than spilt = {1}'.format(self.m, self.k))
        for n in core:
            self.join_graph(n[0])
        return self.G
        

        

class percolation:
    def __init__(self, G, n_list):
        self.G = G.copy()
        self.n_list = n_list
        self.clusters = []
        self.giant = 0
        self.hist = []

        
    def run(self) :
        i = 0
        for n in self.n_list :
            i += 1
            new_c = [n]
            rm_c = [] 
            for c in self.clusters:
                for item in c:
                    if self.G.has_edge(n , item):
                         new_c = new_c + c
                         rm_c.append(c)
                         break
            for c in rm_c:
                self.clusters.remove(c)
            self.clusters.append(new_c)
            self.giant = max(self.giant, len(new_c))
            self.hist.append(self.giant)


                
                

    
if __name__ == "__main__" :


    G = nx.read_gml(sys.argv[1])
    print(G.number_of_edges())
    t0 = time.time() 
    u_list = G.nodes()
    np.random.shuffle(u_list)

    d_list = sorted(G.degree().items(), key=operator.itemgetter(1))
    d_list = list(map(lambda v : v[0], d_list))

    # model = percolation(G, d_list)
    # model.run()
    
    # origin = np.array(model.hist)

    # np.save(sys.argv[2], origin)
    # nx.write_gml(G, sys.argv[3])

    # plt.figure(figsize=(12,9)) 
    # plt.plot(np.linspace(0,1,len(before)), before/G.number_of_nodes(), label='before')
    # k_list = [2, 3, 4, 5 ,6]
    # a_list = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16]
    
    m_list = [1, 2, 3, 4, 5]
    # t_list = [ 'clique', 'ring', 'star','tree']
    for m in m_list:
        print(m)
        S = Split(G, k = 5, alpha = 0.02, m = m)

        H = S.run()
        print(H.number_of_edges())
        print(G.number_of_edges())
        # nx.write_gml(H, "../network/as06_T{0}_K{1}_R{2}_C{3}_M{4}.gml".format('c' , 5, 0.02, 'd', m))
        # print('Spit')
        # # u_list = H.nodes()
        # d_list = sorted(H.degree().items(), key=operator.itemgetter(1))
        # d_list = list(map(lambda v : v[0], d_list))
        # model = percolation(H, d_list)
        # after = model.run()
        # after = np.array(model.hist)
        # print('Percolation')
        # np.save( "../procedure/as06_T{0}_K{1}_R{2}_C{3}_M{4}.npy".format('c' , 5, 0.02, 'd', m), after)
        # plt.plot(np.linspace(0,1,len(after)), after/H.number_of_nodes(), label='alpha = ' + str(k))

    # plt.xlabel("Vertices remaining")
    # plt.ylabel("Size of giant component")
    # plt.legend(loc="upper left")
    # plt.savefig('percolation_degree_alpha.png') 
    # plt.clf()
