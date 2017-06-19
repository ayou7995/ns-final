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
global costfilter

basDir = '../basic/procedure/'
optDir = '../optimize/procedure/'
nonDir = '../nonuniform/procedure/'
figDir = '../figure/'

colors = ['black','brown','red','orange','yellow','green','blue','purple',
          'gray','white','pink','gold','lime','lightgreen','lightblue',
          'lavender','tan','navy','salmon','cyan','magenta','orchid']
markers = ['.','o','x','+','*','D','^','s','p','h',
           '8','1','2','3','4','|','_',',','>','<',
           'v']
thresholds = [0.5, 0.25, 0.1, 0.01]

Nfilter = lambda obj: any(obj['N']==n for n in ['as06'])
Tfilter = lambda obj: any(obj['T']==t for t in ['c','s','r','t'])
Kfilter = lambda obj: any(obj['K']==k for k in [2,3,4,5,6])
Rfilter = lambda obj: any(obj['R']==r for r in [0.005, 0.01, 0.02, 0.04, 0.08, 0.16])
Cfilter = lambda obj: any(obj['C']==c for c in ['b','c','d'])
Mfilter = lambda obj: any(obj['M']==m for m in [1])
costfilter = lambda obj: any(obj['cost']==co for co in [1,2,4,8])

def plot(types, objs, title, filename, topSize=3/5, includeOrigin=True):
    plt.figure()
    for i in range(len(objs)):
        _hist = objs[i]['hist'] / objs[i]['hist'].size 
        # indexlist = objs[i]['thres'] - int(topSize * _hist.size)
        # print(indexlist)
        # _hist = _hist[int(_hist.size*topSize):] 
        if types == 'basic':
            label = 'T{0}_K{1}_R{2}_C{3}_M{4}'.format(
                objs[i]['T'],objs[i]['K'],objs[i]['R'],objs[i]['C'],objs[i]['M'])
        elif types == 'optimize':
            label = 'T{0}_K{1}_R{2}_C{3}_M{4}_cost{5}'.format(
                objs[i]['T'],objs[i]['K'],objs[i]['R'],objs[i]['C'],objs[i]['M'],objs[i]['cost'])
        elif types == 'nonuniform':
            label = 'T{0}_D{1}_M{2}_cost{3}'.format(
                objs[i]['T'],objs[i]['D'],objs[i]['M'],objs[i]['cost'])
    
        plt.plot(np.linspace(topSize,1,_hist.size), _hist, label=label,
                 color=colors[i+1])
    plt.plot([0.75,1],[0.25, 0.25], color='grey')
    if includeOrigin:
        label = 'origin'
        _origin = origin / origin.size
        _origin = _origin[int(_origin.size*topSize):]
        norm_origin = origin / origin.size
        # indexlist = origin['thres'] - int(topSize * origin.size)
        # print(indexlist)
        plt.plot(np.linspace(topSize,1,_origin.size), _origin, label=label,
                 color=colors[0])
    plt.title(title)
    plt.legend(loc='upper left')
    if types == 'basic':
        plt.savefig(join(figDir+'basic/',filename))
    elif types == 'optimize':
        plt.savefig(join(figDir+'optimize/',filename))
    elif types == 'nonuniform':
        plt.savefig(join(figDir+'nonuniform/',filename))

def parse(paths, types):
    data = []
    if types == 'basic' or types == 'optimize':
        for path in paths:
            obj = {}
            if types == 'basic':
                token = path.replace(basDir,'').replace('.npy','').split('_')
            elif types == 'optimize':
                token = path.replace(optDir,'').replace('.npy','').split('_')
                obj['cost'] = int(token[6][4:])
            obj['N'] = token[0]
            obj['T'] = token[1][1]
            obj['K'] = int(token[2][1:])
            obj['R'] = float(token[3][1:])
            obj['C'] = token[4][1]
            obj['M'] = int(token[5][1:])
            obj['hist'] = np.load(path)
            obj['thres'] = threshold(obj['hist'], thresholds)
            data.append(obj)
    elif types == 'nonuniform':
        for path in paths:
            obj = {}
            token = path.replace(nonDir,'').replace('.npy','').split('_')
            obj['N'] = token[0]
            obj['T'] = token[1][1]
            obj['D'] = int(float(token[2][1:]))
            obj['M'] = int(token[3][1:])
            obj['cost'] = int(token[4][4:])
            obj['hist'] = np.load(path)
            obj['thres'] = threshold(obj['hist'], thresholds)
            data.append(obj)
    return data

def setBasicFilter(nL, tL, kL, rL, cL, mL):
    global Nfilter, Tfilter, Kfilter, Rfilter, Cfilter, Mfilter
    Nfilter = lambda obj: any(obj['N']==n for n in nL)
    Tfilter = lambda obj: any(obj['T']==t for t in tL)
    Kfilter = lambda obj: any(obj['K']==k for k in kL)
    Rfilter = lambda obj: any(obj['R']==r for r in rL)
    Cfilter = lambda obj: any(obj['C']==c for c in cL)
    Mfilter = lambda obj: any(obj['M']==m for m in mL)

def setOptimizeFilter(nL, tL, kL, cL, mL, coL):
    global Nfilter, Tfilter, Kfilter, Rfilter, Cfilter, Mfilter, costfilter
    Nfilter = lambda obj: any(obj['N']==n for n in nL)
    Tfilter = lambda obj: any(obj['T']==t for t in tL)
    Kfilter = lambda obj: any(obj['K']==k for k in kL)
    # Rfilter = lambda obj: any(obj['R']==r for r in rL)
    Cfilter = lambda obj: any(obj['C']==c for c in cL)
    Mfilter = lambda obj: any(obj['M']==m for m in mL)
    costfilter = lambda obj: any(obj['cost']==co for co in coL)

def setNonuniformFilter(nL, tL, mL, coL):
    global Nfilter, Tfilter, Mfilter, costfilter
    Nfilter = lambda obj: any(obj['N']==n for n in nL)
    Tfilter = lambda obj: any(obj['T']==t for t in tL)
    Mfilter = lambda obj: any(obj['M']==m for m in mL)
    costfilter = lambda obj: any(obj['cost']==co for co in coL)

def sifter(types, objlist):
    if types == 'basic':
        filters = (Nfilter, Tfilter, Kfilter, Rfilter, Cfilter, Mfilter)
    elif types == 'optimize':
        filters = (Nfilter, Tfilter, Kfilter, Cfilter, Mfilter, costfilter)
    elif types == 'nonuniform':
        filters = (Nfilter, Tfilter, Mfilter, costfilter)
    return list(filter(lambda x: all(f(x) for f in filters), objlist))

def threshold(hist, thres):
    j = 0
    hist = hist / hist.shape[0]
    temp = np.array([0. for i in range(len(thres))])
    for i in reversed(range(len(hist))):
        if hist[i] < thres[j]:
            temp[j] = i /hist.shape[0]
            j+=1
            if j == len(thres):
                break
    return temp #/ hist.size

if __name__ == '__main__':

    # origin percolation data
    origin = np.load(join(basDir,'as06_origin.npy'))
    origin_thres = threshold(origin, thresholds)
    plot('basic', [], 'origin', 'as06_origin')

    # basiclist  
    paths = [p for p in glob.glob(join(basDir,'*.npy')) if 'origin' not in p]
    basiclist = parse(paths, 'basic')

    # optimizelist  
    paths = [p for p in glob.glob(join(optDir,'*.npy')) if 'origin' not in p]
    optimizelist = parse(paths, 'optimize')
    # nonunilist  
    paths = [p for p in glob.glob(join(nonDir,'*.npy')) if 'origin' not in p]
    nonunilist = parse(paths, 'nonuniform')

    # x represents the list including all the element.
    # y represents the changing variable. 
    ########################################################################################
    # BASIC : as06_Tx_Ky_R0.02_Cd_M1
    # for i in range(2,7):
        # setBasicFilter(['as06'],['c','s','t','r'],[i],[0.02],['d'],[1])
        # data = sorted(sifter('basic',basiclist), key=lambda obj: obj['T'])
        # plot('basic', data, 'as06 - topology', 'as06_Tx_K{0}_R0.02_Cd_M1.png'.format(i), 4/5)
    ########################################################################################
    # BASIC : as06_Tc_Kx_Ry_Cd_M1
    # for i in [0.005, 0.01, 0.02, 0.04, 0.08, 0.16]:
        # setBasicFilter(['as06'],['c'],[2,3,4,5,6],[i],['d'],[1])
        # data = sorted(sifter('basic',basiclist), key=lambda obj: obj['K'])
        # plot('basic', data, 'as06 - # of Split Nodes', 'as06_Tc_Kx_R{0}_Cd_M1.png'.format(i), 4/5)
    ########################################################################################
    # BASIC : as06_Tc_Ky_R0.02_Cd_Mx
    # for i in range(2,7):
        # setBasicFilter(['as06'],['c'],[i],[0.02],['d'],list(range(1,i+1)))
        # data = sorted(sifter('basic',basiclist), key=lambda obj: obj['M'])
        # plot('basic', data, 'as06 - replicate', 'as06_Tc_K{0}_R0.02_Cd_Mx.png'.format(i), 3/5)
    ########################################################################################
    # OPTIMIZE : as06_Tc_Kx_R*_Cd_Mx_costy
    for i in [1,2,4,8]:
        setOptimizeFilter(['as06'],['c'],[2,4,6,8],['d'],list(range(1,9)), [i])
        # data = sorted(sifter('optimize',optimizelist), key=lambda obj: (obj['K'],obj['M']))
        data = sorted(sifter('optimize',optimizelist), key=lambda obj: obj['thres'][1])
        data = data[:3] + data[-3:]
        plot('optimize', data, 'as06 - optimize (cost = {0})'.format(i), 
             'as06_Tc_Kx_Cd_Mx_cost{0}.png'.format(i), 73/100)
