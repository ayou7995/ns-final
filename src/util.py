import networkx as nx
import sys

def gml2edgelist(f):
    g = nx.read_gml(f)
    # print('number of node : {0}'.format(g.number_of_nodes()))
    # print('number of edge : {0}'.format(g.number_of_edges()))
    nx.write_edgelist(g, f.replace('gml','edgelist'))

def save_degree(g, path):
    degree = nx.degree(g)
    with open(path, 'w') as w:
        for key, value in degree.items():
            w.write('node: {0} centrality: {1}\n'.format(key, value))


if __name__ == '__main__':
    # gml2edgelist(sys.argv[1])
    g = nx.read_gml(sys.argv[1])
    save_degree(g, sys.argv[2])
