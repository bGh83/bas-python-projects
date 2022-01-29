import matplotlib.pyplot as plt

def genScatterPlot(projection):
    plt.scatter(*projection.T)
    plt.show()
