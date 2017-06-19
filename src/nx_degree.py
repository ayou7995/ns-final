import matplotlib.pyplot as plt 
import sys
import numpy as np
import networkx as nx

import glob

    
if __name__ == "__main__" :
    f_list = glob.glob(sys.argv[1] + "*.gml")
    for f in f_list :
        G=nx.read_gml(f) 

        filepath = '../figure/distribution/' + f.split('/')[1] + '/' + f.split('/')[-1][:-4]+'_log.png'
        print( f.split('/')[-1][:-3])
        degree = list(G.degree().values())
        d_list = []
        for d in  set(degree):
            d_list.append([d, degree.count(d)])
        d_list = np.asarray(d_list)
        plt.scatter(d_list[:,0],d_list[:,1], s=20, c = 'b')
        plt.savefig(filepath)
        plt.clf()