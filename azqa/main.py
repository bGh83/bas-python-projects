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

samples = conversations
samples = pcr.removeConversations(conversations)
# samples = pcr.getRandomConversations(conversations, 10)

size, timestamp = pcr.getConversationStat(samples)
gnp.genPlot(size.values())

# ('46.4.36.120', '147.32.84.160')
# delta, ip.len, sport, dport, ip.p, timestamp
# rows, cols
c2 = pcr.getConversations(conversations, [], 10, 0)
gnp.genPlot(size.values(c2[1:100]))
gnp.genConvPlots(c2)

samples = c2

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

    
import numpy as np
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(2, 1)
# make a little extra space between the subplots
fig.subplots_adjust(hspace=0.5)


x = np.arange(1, len(c2.get(list(c2)[1]))                 
s1 = c2.get(list(c2)[1])
s2 = c2.get(list(c2)[1])

ax1.plot(c, s1, c, s2)
ax1.set_xlim(0, 5)
ax1.set_xlabel('time')
ax1.set_ylabel('s1 and s2')
ax1.grid(True)

cxy, f = ax2.csd(s1, s2, 256, 1. / dt)
ax2.set_ylabel('CSD (db)')
plt.show()

fig = plt.figure()
ax1 = fig.add_axes(s1)
ax2 = fig.add_axes(s2)
ax1.plot(x)
ax2.plot(x)


import secrets
secrets.token_hex(15)

