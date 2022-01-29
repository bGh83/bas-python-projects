from sklearn.manifold import TSNE

def getTSNEProjection(distm):         
    return TSNE(random_state=3072018).fit_transform(distm)
    