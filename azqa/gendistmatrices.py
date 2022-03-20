from fastdtw import fastdtw
# from dtaidistance import dtw
# from dtaidistance import dtw_visualisation as dtwvis
# import numpy as np
from scipy.spatial.distance import euclidean, cosine
from time import perf_counter
import runThreads as rt
from config import config
# import array

thresh = config.CONV_THRESHOLD

def genDistDelta(conversations):
    global distDelta    
    distDelta = getEuclideanDistanceMatrix(conversations, 0)

def genDistBytes(conversations):
    global distBytes
    distBytes = getEuclideanDistanceMatrix(conversations, 1)   

def genDistSport(conversations):
    global distSport
    distSport = getCosineDistanceMatrix(conversations, 2)
    
def genDistDport(conversations):
    global distDport   
    distDport = getCosineDistanceMatrix(conversations, 3)

def calculateDistances(conversations):
    print("\nCalculating distances ...") 
    rt.startThreads([genDistDelta, genDistBytes, genDistSport, genDistDport], conversations)
    return getDistanceMatrix(distBytes, distDelta, distSport, distDport)

def getLabelsIPMappings(conversations):
    mapping = {}
    meta = {}
    labels = []
    ipmapping = []
    fno = 0;
    for i, v in conversations.items():      
        name = i[0] + "->" + i[1]
        if(len(i) == 3):
            name = i[0].split('.')[0] + "|" + i[1] + "->" + i[2]            
        mapping[name] = fno
        fno += 1
        meta[name] = v
    keys = list(meta.keys())   
    inv_mapping = {v:k for k,v in mapping.items()} 
    for x in range(len(conversations.values())):
        labels.append(mapping[keys[x]])
        ipmapping.append((mapping[keys[x]], inv_mapping[mapping[keys[x]]])) 
    return labels, inv_mapping, mapping, ipmapping, keys

def getNormalizedDistance (distm):
    ndistm = []
    minx = min(min(distm))
    maxx = max(max(distm))
    for x in range(len(distm)):
        ndistm.append([])
        for y in range(len(distm)):
            normed = (distm[x][y] - minx) / (maxx-minx)
            ndistm[x].append(normed)
    return ndistm
 
#fill matrix with -1           
def initializeMatrix (values):
    distm = [-1] * len(values)
    distm = [[-1] * len(values) for i in distm]
    return distm
 
def getEuclideanDistanceMatrix(conversations, col):    
    start = perf_counter()    
    values = conversations.values()
    distm = initializeMatrix(values)
    total = len(values)
    
    for x in range(total):            
        for y in range(x+1):    
            i = [pos[col] for pos in list(values)[x]][:thresh]
            j = [pos[col] for pos in list(values)[y]][:thresh]
            if len(i) == 0 or len(j) == 0: continue
            distm[x][y] = 0.0
            if x != y:     
                
                dist, _ = fastdtw(i, j, dist=euclidean)
#                s1 = array.array('d',i)
#                s2 = array.array('d',j)
#                dist = dtw.distance_fast(s1, s2)                
                distm[x][y] = dist
                distm[y][x] = dist
        # print('\r{}'.format(x),"/",len(values), end='\r')        
    ndistm = getNormalizedDistance(distm)    
    print("\nOK. (", round(perf_counter()-start), "s )\n")            
    return ndistm


def getCosineDistanceMatrix(conversations, col): 
    start = perf_counter()        
    values = conversations.values()
    distm = initializeMatrix(values)
        
    ngrams = []
    for x in range(len(values)):
        profile = dict()
        dat = [pos[col] for pos in list(values)[x]][:thresh]
        li = zip(dat, dat[1:], dat[2:])
        for b in li:
            if b not in profile.keys():
                profile[b] = 0            
            profile[b] += 1                    
        ngrams.append(profile)
    
    assert len(ngrams) == len(values)
    for x in range(len(ngrams)):
        for y in range(x+1):            
            distm[x][y] = 0.0
            if x != y:                                
                i = ngrams[x]
                j = ngrams[y]
                ngram_all = list(set(i.keys()) | set(j.keys()))
                i_vec = [(i[item] if item in i.keys() else 0) for item in ngram_all]
                j_vec = [(j[item] if item in j.keys() else 0) for item in ngram_all]
                dist = cosine(i_vec, j_vec)
                distm[x][y] = dist
                distm[y][x] = dist
        # print('\r{}'.format(x),"/",len(values), end='\r')

    ndistm = []
    for a in range(len(distm)):
        ndistm.append([])
        for b in range(len(distm)):
            ndistm[a].append(distm[a][b])
            
    print("OK. (", round(perf_counter()-start), "s )\n")            
    return ndistm

def getDistanceMatrix(distBytes, distDelta, distSport, distDport):
    distm = []
    for x in range(len(distBytes)):
        distm.append([])
        for y in range(len(distBytes)):
            distm[x].append((distBytes[x][y]+distDelta[x][y]+distSport[x][y]+distDport[x][y])/4.0)
            #if((distBytes[x][y]+distDelta[x][y]+distSport[x][y]+distDport[x][y]) == 0):
                #print("\nHi")
    return distm