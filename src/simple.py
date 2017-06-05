import networkx as nx
import sys
import utils as utils
import numpy as np

if __name__ == '__main__':

    g = nx.read_edgelist(sys.argv[1])

    print('number of nodes : {0}'.format(g.number_of_nodes()))
    print('number of edges : {0}'.format(g.number_of_edges()))

    degree, degree_hist = utils.distribution(g, 'asrel_distribution', True)
    betweenness = utils.read_betweenness_centrality('../dataset/centrality/asrel_betweenness.txt')
    closeness = utils.read_closeness_centrality('../dataset/centrality/asrel_closeness.txt')


