from sklearn.manifold import TSNE
import hdbscan

def getTSNEProjection(distm):         
    return TSNE(random_state=3072018).fit_transform(distm)

def genHDBSCANModel(size, samples):
    return hdbscan.HDBSCAN(
        min_cluster_size = size, 
        min_samples = samples, 
        cluster_selection_method='leaf', 
        metric='precomputed')