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
from functools import reduce
S = 0
I = 1




global w1 
global w2 

w1 = 0.001
w2 = 0.00001

def load_data():
    f = open(sys.argv[2], 'r')
    n_list = []
    for line in f:
        line = line.split(' ')
        n_list.append([line[1],float(line[3][:-1])])
    n_list = sorted(n_list, key=lambda tup: tup[1], reverse=True)

    # n_list = list(map(lambda n : n[0], n_list))

    return n_list

class Split:
    def __init__(self, G, k = 3, m = 1, alpha = 0.02, topology = 'clique', v_list =[]):
        self.G = G.copy()
        self.alpha = alpha
        self.k = k
        self.m = m
        self.topology = topology
        self.v_list = v_list
    

    def loss_function(self, k, m, alpha):
        length = int(alpha*len(self.v_list))
        core = self.v_list[:length]
        V = len(core) * (k-1)
        Es = len(core) * k * (k-1) / 2
        Er = 0
        for n in core :
            Er += len(self.G.neighbors(n[0])) * (m-1)
        E =  Es + Er
        #suppose loss = [0,1]
        loss = w1 * V + w2 * E
        return loss
    
    def optimal_alpha(self, k, m, thres ):
        
        count = 1
        alpha = 0.32

        cost = self.loss_function(k, m, alpha )
        while abs(cost - thres) > 0.001:
            alpha -= np.sign(cost - thres) * np.power(0.5,count) * 0.32
            count += 1
            cost = self.loss_function(k, m, alpha )
            if count >= 20:
                break
        return alpha   
         
    def build_clique(self, node, k):
        H = nx.Graph()
        n_list = list(map(lambda i: node + '-' + str(i),  np.arange(k)))
        e_list = list(itertools.combinations(n_list, 2))
        for item in e_list:
            H.add_edge(str(item[0]), str(item[1]))
        return H

    def build_ring(self, node, k):
        H = nx.Graph()
        n_list = list(map(lambda i: node + '-' + str(i),  np.arange(k)))
        e_list = []
        for i in range(len(n_list)):
            e_list.append([n_list[i-1], n_list[i]])
        for item in e_list:
            H.add_edge(str(item[0]), str(item[1]))
        return H

    def build_star(self, node, k):
        H = nx.Graph()
        n_list = list(map(lambda i: node + '-' + str(i),  np.arange(k)))
        e_list = []
        for i in range(len(n_list)-1):
            e_list.append([n_list[0], n_list[i+1]])
        for item in e_list:
            H.add_edge(str(item[0]), str(item[1]))
        return H

    def build_tree(self, node, k):
        H = nx.Graph()
        n_list = list(map(lambda i: node + '-' + str(i),  np.arange(k)))
        e_list = []
        for i in range(1,len(n_list)):
            if i % 2 != 0 : 
                e_list.append([n_list[i], n_list[int((i-1)/2)]])
            else :
                e_list.append([n_list[i], n_list[int((i-2)/2)]])
        for item in e_list:
            H.add_edge(str(item[0]), str(item[1]))
        return H

    def join_graph(self, node, k , m):
        neighbors = self.G.neighbors(node)
        if len(neighbors) < k:
            return
        if self.topology == 'clique':
            H = self.build_clique(node, k)
        if self.topology == 'ring':
            H = self.build_ring(node, k)
        if self.topology == 'star':
            H = self.build_star(node, k)
        if self.topology == 'tree':
            H = self.build_tree(node, k)
        origins = list(filter(lambda n : n.find('-')  == -1,neighbors))
        spilteds = sorted(list(filter(lambda n : n.find('-') != -1,neighbors)))
        for i in range(k):
            s = int(len(origins)*i/k)
            e = int((len(origins)*(i+1)/k))
            sub = origins[s:e]
            for j in range (m):
                for n in sub :
                    self.G.add_edge(H.nodes()[ (i + j) % k], n)
        for i in range (len(spilteds)):
            self.G.add_edge(H.nodes()[i % k], spilteds[i])
        self.G.remove_node(node)
        self.G = nx.compose(self.G ,H) 

    def run(self):
        length = int(self.alpha*len(self.v_list))
        core = self.v_list[:length]

        cost = self.loss_function( self.k, self.m, self.alpha)
        print(cost)
        if self.k < self.m :
            raise ValueError('The replica = {0} most smaller than spilt = {1}'.format(self.m, self.k))
        for n in core:
            self.join_graph(n[0], self.k , self.m)

        return self.G

class Split_d(Split):
    
    def __init__(self, G, d= 500, m = 1, topology = 'clique'):
        self.G = G.copy()
        self.d = d
        self.m = m
        self.topology = topology

    def loss_function(self, d, m):
        d_list = list(sorted(self.G.degree().items(), key=operator.itemgetter(1), reverse = True ))
        core = list(filter(lambda n : n[1] >= d , d_list)) 
        V = 0
        Er = 0
        Es = 0
        for n in core : 
            k = int(n[1]/d) +1
            V += (k-1)
            Es += k*(k-1)/2
            Er +=  n[1] * (min(m,k)-1)
        E = Er + Es 
        loss = w1 * V + w2 * E
        return loss

    def optimal_d(self, m, thres):
        count = 1
        d = 512
        cost = self.loss_function(d, m)
        while abs(cost - thres) > 0.001:
            d += np.sign(cost - thres) * np.power(0.5,count) * 512 
            count += 1
            cost = self.loss_function(d, m)
            if count > 9:
                break
        return d  

    def run(self):
        d_list = list(sorted(self.G.degree().items(), key=operator.itemgetter(1), reverse = True ))
        core = list(filter(lambda n : n[1] >= self.d , d_list)) 
        cost = self.loss_function(self.d, self.m)
        print(cost)
        for n in core : 
            k = int(n[1]/self.d) +1
            m = min(self.m ,k)
            self.join_graph(n[0], k, m)
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
    v_list = load_data()
    print ('load data')

    print(G.number_of_nodes())

    S = Split_d(G)

    cost = 8
    m_list = [16]
    for m in m_list:
        d = S.optimal_d(m, cost)
        t = 'clique'
        print('m:{0}, c:{1} ,d:{2}'.format(m,cost,d))
        S2 =  Split_d(G, d = d, m = m )
        H = S2.run()
        nx.write_gml(H, "../nonuniform/network/as06_T{0}_D{1}_M{2}_cost{3}.gml".format(t[0], d, m, cost ))
        print('Split')
        d_list = sorted(H.degree().items(), key=operator.itemgetter(1))
        d_list = list(map(lambda v : v[0], d_list))
        model = percolation(H, d_list)
        after = model.run()
        after = np.array(model.hist)
        print('Percolation')
        np.save( "../nonuniform/procedure/as06_T{0}_D{1}_M{2}_cost{3}.npy".format(t[0], d, m, cost ),after)

    # H = S.run()


    # print(a)
    # H, cost = S.run()
    # print(cost)
    # k_list = np.arange(8,9,2)
    # cost = 8
    # for k in k_list:
    #     for m in np.arange(1,k+1):
    #         a = S.optimal_alpha(k,m, cost)
    #         t = 'clique'
    #         print("k : {0}, m : {1}, a : {2:.3f}, cost : {3}".format(k ,m, a, cost))
    #         S2 = Split(G, k = k, alpha = a, m = m, topology = t, v_list = v_list)
    #         H = S2.run()
    #         nx.write_gml(H, "../optimize/network/as06_T{0}_K{1}_R{2:.3f}_C{3}_M{4}_cost{5}.gml".format(t[0], k, a, 'd', m, cost))
    #         print('Split')
    #         d_list = sorted(H.degree().items(), key=operator.itemgetter(1))
    #         d_list = list(map(lambda v : v[0], d_list))
    #         model = percolation(H, d_list)
    #         after = model.run()
    #         after = np.array(model.hist)
    #         print('Percolation')
    #         np.save( "../optimize/procedure/as06_T{0}_K{1}_R{2:.3f}_C{3}_M{4}_cost{5}.npy".format(t[0], k, a, 'd', m, cost), after)

