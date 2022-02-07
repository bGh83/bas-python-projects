import genconmaps as pcr
import gendistmatrices as gdm
import genplots as gnp
import genmodels as gnm
import genfiles as gnf
# import gendag as gnd


'''
    read pcaps
    get connections/conversations
    refine data as needed
    get distances (dtw, ngram)
    generate model
    generate heatmap
    analyze results
'''         

conversations = pcr.getConversationMaps()
gnf.saveCoversations (conversations)
conversations = gnf.loadAllConversations()

gnp.genConvPlots(pcr.getConversations(conversations, ('46.4.36.120', '147.32.84.160'), 100))

samples = pcr.removeConversations(conversations)
samples = pcr.getRandomConversations(conversations, 10)

size, timestamp = pcr.getConversationStat(samples)
gnp.genPlot(size.values())

# gnp.genXYPlots(connections, 0)
# gnp.genXYPlots(connections, 2)

distAll = gdm.calculateDistances(samples)

projection = gnm.getTSNEProjection(distAll)
gnp.genScatterPlot(projection)

model = gnm.genHDBSCANModel(distAll)
gnm.getClusterStat(model)

#gnp.genCondensedTreePlot(model)
#gnp.genSingleLinkageTreePlot(mode l)

labels, inv_mapping, mapping, ipmapping, keys = gdm.getLabelsIPMappings(samples)
gnp.genScatterPlotWithModel(model, distAll, projection, labels, inv_mapping)

clusterfile = gnf.genClusterfile(model, labels, mapping, inv_mapping)

# dagfile = gnf.genRelationshipGraphfile(model, clusterfile)
# gnd.genRelationshipGraphs(dagfile, model)

gnp.genHeatMap(samples, mapping, keys, clusterfile)
  
import matplotlib.pyplot as plt
import numpy as np
c2 = pcr.getConversations(conversations, ('46.4.36.120', '147.32.84.160'), -1, 0)

plt.plot(c2[100:200])

#0 delta,                
#1 ip.len,
#2 sport,
#3 dport,
#4 ip.p,
#5 timestamp
    
