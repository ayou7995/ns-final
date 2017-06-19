import matplotlib.pyplot as plt
import numpy as np
import glob
import sys
from os.path import join

global Nfilter
global Tfilter
global Kfilter
global Rfilter
global Cfilter
global Mfilter

proDir = '../procedure/'
figDir = '../figure/'

colors = ['black','brown','red','orange','yellow','green','blue','purple','gray','white','pink']
markers = ['.','o','x','+','*','D','^','s','p','h','8']

Nfilter = lambda obj: any(obj['N']==n for n in ['as06'])
Tfilter = lambda obj: any(obj['T']==t for t in ['c','s','r','t'])
Kfilter = lambda obj: any(obj['K']==k for k in [2,3,4,5,6])
Rfilter = lambda obj: any(obj['R']==r for r in [0.005, 0.01, 0.02, 0.04, 0.08, 0.16])
Cfilter = lambda obj: any(obj['C']==c for c in ['b','c','d'])
Mfilter = lambda obj: any(obj['M']==m for m in [1])

# def newDict():

def plot(objs, title, filename, topSize=3/5, includeOrigin=True):
    plt.figure()
    for i in range(len(objs)):
        _hist = objs[i]['hist'] / objs[i]['hist'].size 
        indexlist = [np.where(_hist==size)[0][-1] for size in objs[i]['thres']]
        indexlist = [-(_hist.size-idx) for idx in indexlist]
        _hist = _hist[int(_hist.size*topSize):] 
        label = 'T{0}_K{1}_R{2}_C{3}_M{4}'.format(objs[i]['T'],objs[i]['K'],
                                                  objs[i]['R'],objs[i]['C'],objs[i]['M'])
        plt.plot(np.linspace(topSize,1,_hist.size), _hist, label=label,
                 color=colors[i+1], marker=markers[i+1], markevery=indexlist)
        # print(label, ' : ', threshold(obj['hist'],[0.5, 0.25, 0.1, 0.01, 0.001]))
    if includeOrigin:
        label = 'origin'
        _origin = origin / origin.size
        _origin = _origin[int(_origin.size*topSize):]
        norm_origin = origin / origin.size
        indexlist = [np.where(norm_origin==size)[0][-1] for size in origin_thres]
        indexlist = [-(origin.size-idx) for idx in indexlist]
        plt.plot(np.linspace(topSize,1,_origin.size), _origin, label=label,
                 color=colors[0], marker=markers[0], markevery=indexlist)
        # print(label, ' : ', threshold(origin,[0.5, 0,25, 0.1, 0.01, 0.001]))
    plt.title(title)
    plt.legend()
    plt.savefig(join(figDir,filename))

def parse(paths, cost=False):
    data = []
    for path in paths:
        obj = {}
        token = path.replace(proDir,'').replace('.npy','').split('_')
        obj['N'] = token[0]
        obj['T'] = token[1][1]
        obj['K'] = int(token[2][1:])
        obj['R'] = float(token[3][1:])
        obj['C'] = token[4][1]
        obj['M'] = int(token[5][1:])
        obj['hist'] = np.load(path)
        obj['thres'] = threshold(obj['hist'], [0.5, 0.25, 0.1, 0.01, 0.001])
        data.append(obj)
    return data

def setFilter(nL, tL, kL, rL, cL, mL):
    global Nfilter
    global Tfilter
    global Kfilter
    global Rfilter
    global Cfilter
    global Mfilter
    Nfilter = lambda obj: any(obj['N']==n for n in nL)
    Tfilter = lambda obj: any(obj['T']==t for t in tL)
    Kfilter = lambda obj: any(obj['K']==k for k in kL)
    Rfilter = lambda obj: any(obj['R']==r for r in rL)
    Cfilter = lambda obj: any(obj['C']==c for c in cL)
    Mfilter = lambda obj: any(obj['M']==m for m in mL)

def sifter(objlist):
    filters = (Nfilter, Tfilter, Kfilter, Rfilter, Cfilter, Mfilter)
    return list(filter(lambda x: all(f(x) for f in filters), objlist))

def threshold(hist, thres):
    # hist = np.flip(hist,0)
    # wholeNum = hist
    hist = hist / hist.size
    temp = np.array([0. for i in range(len(thres))])
    j = 0
    for i in reversed(range(len(hist))):
        if hist[i] < thres[j]:
            temp[j] = hist[i]
            j+=1
            if j == len(thres):
                break
    return temp #/ hist.size

if __name__ == '__main__':

    origin = np.load(join(proDir,'as06_origin.npy'))
    origin_thres = threshold(origin, [0.5, 0.25, 0.1, 0.01, 0.001])
    print('origin_thres')
    print(origin_thres)
    plot([], 'origin', 'origin')

    paths = [p for p in glob.glob(join(proDir,'*.npy')) if 'origin' not in p]
    objlist = parse(paths)

    #####################################################################
    # as06_Tx_K3_R0.02_Cd_M1
    setFilter(['as06'],['c','s','t','r'],[3],[0.02],['d'],[1])
    data = sorted(sifter(objlist), key=lambda obj: obj['T'])
    plot(data, 'as06 - topology', 'as06_Tx_K3_R0.02_Cd_M1.png', 4/5)
    
    # as06_Tx_K4_R0.02_Cd_M1
    setFilter(['as06'],['c','s','t','r'],[4],[0.02],['d'],[1])
    data = sorted(sifter(objlist), key=lambda obj: obj['T'])
    plot(data, 'as06 - topology', 'as06_Tx_K4_R0.02_Cd_M1.png', 4/5)
    
    # as06_Tx_K5_R0.02_Cd_M1
    setFilter(['as06'],['c','s','t','r'],[5],[0.02],['d'],[1])
    data = sorted(sifter(objlist), key=lambda obj: obj['T'])
    plot(data, 'as06 - topology', 'as06_Tx_K5_R0.02_Cd_M1.png', 4/5)
    
    # as06_Tx_K6_R0.02_Cd_M1
    setFilter(['as06'],['c','s','t','r'],[6],[0.02],['d'],[1])
    data = sorted(sifter(objlist), key=lambda obj: obj['T'])
    plot(data, 'as06 - topology', 'as06_Tx_K6_R0.02_Cd_M1.png', 4/5)

    ##########################################################################
    # as06_Tc_Kx_R0.005_Cd_M1
    setFilter(['as06'],['c'],[2,3,4,5,6],[0.005],['d'],[1])
    data = sorted(sifter(objlist), key=lambda obj: obj['K'])
    plot(data, 'as06 - # of Split Nodes', 'as06_Tc_Kx_R0.005_Cd_M1.png', 4/5)

    # as06_Tc_Kx_R0.01_Cd_M1
    setFilter(['as06'],['c'],[2,3,4,5,6],[0.01],['d'],[1])
    data = sorted(sifter(objlist), key=lambda obj: obj['K'])
    plot(data, 'as06 - # of Split Nodes', 'as06_Tc_Kx_R0.01_Cd_M1.png', 4/5)

    # as06_Tc_Kx_R0.02_Cd_M1
    setFilter(['as06'],['c'],[2,3,4,5,6],[0.02],['d'],[1])
    data = sorted(sifter(objlist), key=lambda obj: obj['K'])
    plot(data, 'as06 - # of Split Nodes', 'as06_Tc_Kx_R0.02_Cd_M1.png', 4/5)

    # as06_Tc_Kx_R0.04_Cd_M1
    setFilter(['as06'],['c'],[2,3,4,5,6],[0.04],['d'],[1])
    data = sorted(sifter(objlist), key=lambda obj: obj['K'])
    plot(data, 'as06 - # of Split Nodes', 'as06_Tc_Kx_R0.04_Cd_M1.png', 4/5)

    # as06_Tc_Kx_R0.08_Cd_M1
    setFilter(['as06'],['c'],[2,3,4,5,6],[0.08],['d'],[1])
    data = sorted(sifter(objlist), key=lambda obj: obj['K'])
    plot(data, 'as06 - # of Split Nodes', 'as06_Tc_Kx_R0.08_Cd_M1.png', 4/5)

    # as06_Tc_Kx_R0.16_Cd_M1
    setFilter(['as06'],['c'],[2,3,4,5,6],[0.16],['d'],[1])
    data = sorted(sifter(objlist), key=lambda obj: obj['K'])
    plot(data, 'as06 - # of Split Nodes', 'as06_Tc_Kx_R0.16_Cd_M1.png', 4/5)

    ###########################################################################
    # as06_Tc_K2_R0.02_Cd_Mx
    setFilter(['as06'],['c'],[2],[0.02],['d'],[1,2])
    data = sorted(sifter(objlist), key=lambda obj: obj['M'])
    plot(data, 'as06 - replicate', 'as06_Tc_K2_R0.02_Cd_Mx.png', 3/5)

    # as06_Tc_K3_R0.02_Cd_Mx
    setFilter(['as06'],['c'],[3],[0.02],['d'],[1,2,3])
    data = sorted(sifter(objlist), key=lambda obj: obj['M'])
    plot(data, 'as06 - replicate', 'as06_Tc_K3_R0.02_Cd_Mx.png', 3/5)

    # as06_Tc_K4_R0.02_Cd_Mx
    setFilter(['as06'],['c'],[4],[0.02],['d'],[1,2,3,4])
    data = sorted(sifter(objlist), key=lambda obj: obj['M'])
    plot(data, 'as06 - replicate', 'as06_Tc_K4_R0.02_Cd_Mx.png', 3/5)

    # as06_Tc_K5_R0.02_Cd_Mx
    setFilter(['as06'],['c'],[5],[0.02],['d'],[1,2,3,4,5])
    data = sorted(sifter(objlist), key=lambda obj: obj['M'])
    plot(data, 'as06 - replicate', 'as06_Tc_K5_R0.02_Cd_Mx.png', 3/5)

    # as06_Tc_K6_R0.02_Cd_Mx
    setFilter(['as06'],['c'],[6],[0.02],['d'],[1,2,3,4,5,6])
    data = sorted(sifter(objlist), key=lambda obj: obj['M'])
    plot(data, 'as06 - replicate', 'as06_Tc_K6_R0.02_Cd_Mx.png', 3/5)
