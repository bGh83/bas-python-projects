from sklearn.manifold import TSNE
import numpy as np
import hdbscan
from config import config

def getClusterStat(model):
    avg = 0.0
    for l in list(set(model.labels_)):
        if l !=-1:
            avg+= sum([(1 if x==l else 0) for x in model.labels_])    
    print("Cluster Cnt:", str(len(set(model.labels_))-1),
          "Avg cluster size:", str(float(avg)/float(len(set(model.labels_))-1)),
          "Samples in noise:", str(sum([(1 if x==-1 else 0) for x in model.labels_])))
                                    
def getTSNEProjection(distm):         
    return TSNE(random_state=config.TSNE_RANDOM_STATE).fit_transform(distm)

def genHDBSCANModel(distm):
    model = hdbscan.HDBSCAN(
        min_cluster_size = config.HDBSCAN_MIN_CLUSTER_SIZE, 
        min_samples = config.HDBSCAN_MIN_SAMPLES, 
        cluster_selection_method='leaf', 
        metric='precomputed')
    return model.fit(np.array([np.array(x) for x in distm]))