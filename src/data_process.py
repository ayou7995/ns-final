import sys
import time
import networkx
import graph_tool.all as gt
import numpy as np

def process_as_rel():
    asrels = {}
    lines = []
    with open('../dataset/201603.as-rel-geo.txt', 'r') as f:
        for line in f.readlines():
            token = line.strip().split()
            if token[0] != '#':
                lines.append(line)
    for i in range(len(lines)):
        asrel = {}
        try:
            token1 = lines[i].strip().split('|')
            # print(token1)
            asrel['AS0'] = token1[0]
            asrel['AS1'] = token1[1]
            asrel['method'] = []
            for method in token1[2:]:
                token2 = method.strip().split(',')
                rel = {}     
                rel['loc'] = token2[0]
                rel['source'] = token2[1:]
                asrel['method'].append(rel)
        except:
            print('{0}: {1}'.format(i, lines[i]))
        asrels[i] = asrel
    return asrels

def process_location():
    locs = {}
    lines = []
    with open('../dataset/201603.locations.txt', 'r') as f:
        for line in f.readlines():
            token = line.strip().split()
            if token[0] != '#':
                lines.append(line)
    for i in range(len(lines)):
        try:
            token = lines[i].strip().split('|')
            info = {}
            info['continent'] = token[1]
            info['country'] = token[2]
            info['regeon'] = token[3]
            info['city'] = token[4]
            info['latitude'] = token[5]
            info['longtitude'] = token[6]
            info['population'] = token[7]
            locs[token[0]] = info
        except:
            print('{0}: {1}'.format(i, lines[i]))
    return locs

def save_edgelsit(asrels, locs, attributes, name):

    path = '../dataset/{0}.txt'.format(name)
    with open(path, 'w') as w:
        for key, value in asrels.items():
            w.write('{0} {1}\n'.format(value['AS0'], value['AS1']))
        

if __name__ == '__main__':
    asrels = process_as_rel()
    locs = process_location()
    save_edgelsit(asrels, locs, [], 'asrel_simple_graph')
    # save_edgelsit(asrels, locs, ['continent', 'country', 'city'] 
