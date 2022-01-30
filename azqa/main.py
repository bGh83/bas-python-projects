from config import CONFIG
import genconmaps as pcr
import gendistmatrices as gdm
import genplots as gnp
import genmodels as gnm
import genfiles as gnf
import gendag as gnd

#connections =pcr.getConnectionMap(pr.getPcap ('ISCX_Botnet-Training.pcap'))
connections = pcr.getConnectionMap(pcr.getPcap ('virut2.pcap'))

connections = pcr.removeConnections(connections, CONFIG.CONN_THRESHOLD)
pcr.getConnectionStat(connections)

distSize = gdm.getEuclideanDistanceMatrix(connections, CONFIG.CONN_THRESHOLD, 2)
distDelta = gdm.getEuclideanDistanceMatrix(connections, CONFIG.CONN_THRESHOLD, 0)
distSport = gdm.getCosineDistanceMatrix(connections, CONFIG.CONN_THRESHOLD, 3)
distDport = gdm.getCosineDistanceMatrix(connections, CONFIG.CONN_THRESHOLD, 4)
distAll = gdm.getDistanceMatrix(distSize, distDelta, distSport, distDport)

projection = gnm.getTSNEProjection(distAll)
gnp.genScatterPlot(projection)

model = gnm.genHDBSCANModel(distAll, CONFIG.HDBSCAN_MIN_CLUSTER_SIZE, CONFIG.HDBSCAN_MIN_SAMPLES)
gnm.getClusterStat(model)
#gnp.genCondensedTreePlot(model)
#gnp.genSingleLinkageTreePlot(model)
labels, inv_mapping, mapping, ipmapping, keys = gdm.getLabelsIPMappings(connections)
gnp.genScatterPlotWithModel(model, distAll, projection, labels, inv_mapping)

clusterfile = gnf.genClusterfile(model, labels, mapping, inv_mapping)
dagfile = gnf.genRelationshipGraphfile(model, clusterfile)
gnd.genRelationshipGraphs(dagfile, model)
gnp.genHeatMap(connections, mapping, keys, clusterfile, CONFIG.CONN_THRESHOLD)
