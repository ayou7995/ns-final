import matplotlib.pyplot as plt 
import sys
import numpy as np
import time
import csv
import time
import networkx as nx
import random
import operator

RATE = 10



class percolation:
    def __init__(self, G, v_list):
        self.G = G.copy()
        self.v_list = v_list
        self.hist = []
        
    def run(self) :
        for i in range(0, len(self.v_list), RATE):
            self.G.remove_nodes_from(self.v_list[i:i+RATE])
            try :
                giant = max(nx.connected_component_subgraphs(self.G), key=len).number_of_nodes()
                self.hist.append(giant)
            except:
                pass
        h = len (self.hist)
        for i in range(RATE*h, len(self.v_list), RATE):
            giant = 1
            self.hist.append(giant)
                

       
            

    
if __name__ == "__main__" :
    G = nx.read_gml(sys.argv[1])
    t0 = time.time()                                  
    print ("number of nodes :%s, time:%s" %(G.number_of_nodes(),time.time() - t0))
    t0 = time.time() 
    print ("number of edges :%s, time:%s" %(G.number_of_edges(),time.time() - t0))
    u_list = G.nodes()
    np.random.shuffle(u_list)
    model = percolation(G, u_list)
    model.run()
    uniform = model.hist
    uniform = uniform[::-1]
    print('unoform')

    d_list = sorted(G.degree().items(), key=operator.itemgetter(1), reverse=True)
    d_list = list(map(lambda v : v[0], d_list))
    model = percolation(G, d_list)
    model.run()
    degree = model.hist
    degree = degree[::-1]
    print('degree')

    c_list = sorted(nx.closeness_centrality(G).items(), key=operator.itemgetter(1), reverse=True)
    c_list = list(map(lambda v : v[0], c_list))
    model = percolation(G, c_list)
    model.run()
    closeness = model.hist
    closeness = closeness[::-1]
    print('closeness')

    b_list = sorted(nx.betweenness_centrality(G).items(), key=operator.itemgetter(1), reverse=True)
    b_list = list(map(lambda v : v[0], b_list))
    model = percolation(G, c_list)
    model.run()
    betweenness = model.hist
    betweenness = betweenness[::-1]
    print('betweenness')

    e_list = sorted(nx.eigenvector_centrality(G).items(), key=operator.itemgetter(1), reverse=True)
    e_list = list(map(lambda v : v[0], e_list))
    model = percolation(G, e_list)
    model.run()
    eigenvector = model.hist
    eigenvector = eigenvector[::-1]
    print('eigenvector')

    plt.figure(figsize=(12,9)) 
    plt.plot(RATE*np.arange(len(uniform)), uniform, label='uniform')
    plt.plot(RATE*np.arange(len(degree)), degree, label='degree')
    plt.plot(RATE*np.arange(len(eigenvector)), eigenvector, label='eigenvector')
    plt.plot(RATE*np.arange(len(closeness)), closeness, label='closeness')
    plt.plot(RATE*np.arange(len(betweenness)), betweenness, label='betweenness')
    plt.xlabel("Vertices remaining")
    plt.ylabel("Size of giant component")
    plt.legend(loc="lower right")
    plt.savefig('percolation2.png') 
    plt.clf()


