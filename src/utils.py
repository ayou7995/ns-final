import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def plotdistribution(data, name):
 
    title = ["Original Degree Distribution", 
             "Logscale Degree Distribution"]
    xlabel = ["Degree", "log(Degree)"]
    ylabel = ["# of Degree", "log(# of Degree)"]
    fig = plt.figure(figsize=(20,10))
    for i in range (len(data)): 
        ax = fig.add_subplot(1, 2 ,i+1) 
        d = data[i]
        ax.scatter(d[0,:],d[1,:], s=20, c='b')
        ax.set_title(title[i], fontsize=32)
        ax.set_xlabel(xlabel[i], fontsize=20)
        ax.set_ylabel(ylabel[i], fontsize=20)
        plt.tight_layout(pad=3.0, w_pad=5.0)
    fig.savefig('../img/{0}_distribution.png'.format(name)) 

def distribution(graph, name, plot=False):
    degree = list(graph.degree().values())
    distribution = []
    deg, hist = [], []
    for d in set(degree):
        deg.append(d)
        hist.append(degree.count(d))
    deg, hist = zip(*sorted(zip(deg, hist)))
    distribution.append(deg)
    distribution.append(hist)

    # orgin degree dirstribution 
    distribution = np.asarray(distribution)
    # log scale
    distribution_log = np.log10(distribution)

    data = []
    data.append(distribution)
    data.append(distribution_log)

    if plot:
        plotdistribution(data, name)

    return deg, hist

def read_betweenness_centrality(path):
    betweenness = {} 
    with open(path, 'r') as f:
        for line in f.readlines():
            token = line.strip().split()
            betweenness[token[1]] = token[3]
    return betweenness

def read_closeness_centrality(path):
    closeness = {} 
    with open(path, 'r') as f:
        for line in f.readlines():
            token = line.strip().split()
            closeness[token[1]] = token[3]
    return closeness

__all__ = [distribution, read_betweenness_centrality, read_closeness_centrality]
