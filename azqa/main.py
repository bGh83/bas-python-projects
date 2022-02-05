import genconmaps as pcr
import gendistmatrices as gdm
import genplots as gnp
import genmodels as gnm
import genfiles as gnf
# import gendag as gnd


'''
    read pcaps
    get connections/conversations
    get distances (dtw, ngram)
    generate model
    generate heatmap
    
'''         

master = pcr.getConnectionMaps()
samples = pcr.removeConnections(master)
samples = pcr.getRandomConnections(master, 500)

size = pcr.getConnectionStat(samples)
gnp.genPlot(size)

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
  