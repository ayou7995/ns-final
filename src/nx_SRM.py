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
    def __init__(self, G, alpha, k):
        self.G = G.copy()
        self.alpha = alpha
        self.k = k
        self.n_list = sorted(G.degree().items(), key=operator.itemgetter(1), reverse=True)

    def build_clique(self, node):
        H = nx.Graph()
        n_list = list(map(lambda i: node + '-' + str(i),  np.arange(self.k)))
        e_list = list(itertools.combinations(n_list, 2))
        for item in e_list:
            H.add_edge(str(item[0]), str(item[1]))
        return H

    def join_graph(self, node):
        neighbors = self.G.neighbors(node)
        if len(neighbors) < self.k:
            return
        H = self.build_clique(node)
        for i in range(self.k):
            s = int(len(neighbors)*i/self.k)
            e = int((len(neighbors)*(i+1)/self.k))
            sub = neighbors[s:e]
            for n in sub :
                self.G.add_edge(H.nodes()[i], n)
        self.G.remove_node(node)
        self.G = nx.compose(self.G ,H) 

    def run(self):
        length = int(self.alpha*len(self.n_list))
        core = self.n_list[:length]
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
    hist = np.load(sys.argv[1])
    print(hist)
    # G = nx.read_gml(sys.argv[1])
    # t0 = time.time() 
    # u_list = G.nodes()
    # np.random.shuffle(u_list)

    # d_list = sorted(G.degree().items(), key=operator.itemgetter(1))
    # d_list = list(map(lambda v : v[0], d_list))

    # model = percolation(G, d_list)
    # model.run()
    
    # origin = np.array(model.hist)

    # np.save(sys.argv[2], origin)
    # nx.write_gml(G, sys.argv[3])

    # plt.figure(figsize=(12,9)) 
    # plt.plot(np.linspace(0,1,len(before)), before/G.number_of_nodes(), label='before')
    # # k_list = [2,3,4,5]
    # k_list = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16]
    # for k in k_list:
    #     print(k)
    #     S = Split(G, k, 3)
    #     H = S.run()
    #     # u_list = H.nodes()
    #     d_list = sorted(H.degree().items(), key=operator.itemgetter(1))
    #     d_list = list(map(lambda v : v[0], d_list))
    #     model = percolation(H, d_list)
    #     after = model.run()
    #     after = np.array(model.hist)
    #     plt.plot(np.linspace(0,1,len(after)), after/H.number_of_nodes(), label='alpha = ' + str(k))

    # plt.xlabel("Vertices remaining")
    # plt.ylabel("Size of giant component")
    # plt.legend(loc="upper left")
    # plt.savefig('percolation_degree_alpha.png') 
    # plt.clf()
