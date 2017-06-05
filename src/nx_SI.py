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




class SI_model:
    def __init__(self, G, beta, mode = "uniform"):
        self.G = G.copy()
        nx.set_node_attributes(self.G, 'state', S)
        self.beta = beta
        self.mode = mode
        self.i_list = []
        self.s_list = list(self.G.nodes())
        self.hist = []
    
    def checkstate(self, node):

        if node["state"] == I:
            return False
        else:
            return True 

    def propogation(self, neighbor):
        if not neighbor:
            return
        suspected = list(filter(lambda n: self.checkstate(self.G.node[n]) ,neighbor))
        if not suspected:
            return
        if self.mode == "uniform":
            for s in suspected:
                if np.random.rand() < self.beta :
                    self.infected(s)
        if self.mode == "degree":
            suspected = sorted(self.G.degree(suspected).items(), key=operator.itemgetter(1), reverse=True)
            k = 0 
            for i in range(len(suspected)):
                s = suspected[k][0]
                if np.random.rand() < self.beta :
                    self.infected(s)
                if not self.checkstate(self.G.node[s]):
                    k += 1 
        return
    def infected(self, target):
        if  self.G.node[target]['state'] == I :
            return
        self.G.node[target]['state'] = I
        self.s_list.remove(target)
        self.i_list.append(target)

        
    def run(self) :
        target = random.choice(self.s_list)
        self.infected(target)
        i = 0 
        while len(self.s_list) > 0: 
            neighbors = list(map(lambda i : self.G.neighbors(i), self.i_list))
            for n in neighbors : 
                self.propogation(n)
            self.hist.append([i,len(self.s_list),len(self.i_list)])
            print(i,len(self.s_list),len(self.i_list))
            i += 1



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
    G = nx.read_gml(sys.argv[1])
    t0 = time.time() 
    u_list = G.nodes()
    np.random.shuffle(u_list)

    d_list = sorted(G.degree().items(), key=operator.itemgetter(1))
    d_list = list(map(lambda v : v[0], d_list))

    model = percolation(G, d_list)
    model.run()
    
    before = np.array(model.hist)

    plt.figure(figsize=(12,9)) 
    plt.plot(np.linspace(0,1,len(before)), before/G.number_of_nodes(), label='before')
    k_list = [2,3,4,5]
    a_list = [0.005, 0.01, 0.02, 0.04, 0.08]
    for a in a_list:
        print(a)
        S = Split(G, a, 3)
        H = S.run()
        d_list = sorted(H.degree().items(), key=operator.itemgetter(1))
        d_list = list(map(lambda v : v[0], d_list))
        model = percolation(H, d_list)
        after = model.run()
        after = np.array(model.hist)
        plt.plot(np.linspace(0,1,len(after)), after/G.number_of_nodes(), label='alpha =' + str(a))

    plt.xlabel("Vertices remaining")
    plt.ylabel("Size of giant component")
    plt.legend(loc="lower right")
    plt.savefig('percolation1.png') 
    plt.clf()
