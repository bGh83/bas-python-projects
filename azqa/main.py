from config import config
import genconmaps as pcr
import gendistmatrices as gdm
import genplots as gnp
import genmodels as gnm
import genfiles as gnf
import gendag as gnd
import threading
import json


#connections =pcr.getConnectionMap(pr.getPcap ('ISCX_Botnet-Training.pcap'))
connections = pcr.getConnectionMaps()

temp = connections

connections = pcr.removeConnections(connections, 20, 250)
size = pcr.getConnectionStat(connections)

#gnp.genXYPlots(connections, config.CONN_THRESHOLD, 0)
#gnp.genXYPlots(connections, config.CONN_THRESHOLD, 2)

distSize = gdm.getEuclideanDistanceMatrix(connections, config.CONN_THRESHOLD, 2)
with open('out.json', 'w') as outfile:
    json.dump(distSize, outfile)
    
distDelta = gdm.getEuclideanDistanceMatrix(connections, config.CONN_THRESHOLD, 0)
    
distSport = gdm.getCosineDistanceMatrix(connections, config.CONN_THRESHOLD, 3)
distDport = gdm.getCosineDistanceMatrix(connections, config.CONN_THRESHOLD, 4)
distAll = gdm.getDistanceMatrix(distSize, distDelta, distSport, distDport)

projection = gnm.getTSNEProjection(distAll)
gnp.genScatterPlot(projection)

model = gnm.genHDBSCANModel(distAll, config.HDBSCAN_MIN_CLUSTER_SIZE, config.HDBSCAN_MIN_SAMPLES)
gnm.getClusterStat(model)
#gnp.genCondensedTreePlot(model)
#gnp.genSingleLinkageTreePlot(model)
labels, inv_mapping, mapping, ipmapping, keys = gdm.getLabelsIPMappings(connections)
gnp.genScatterPlotWithModel(model, distAll, projection, labels, inv_mapping)

clusterfile = gnf.genClusterfile(model, labels, mapping, inv_mapping)
dagfile = gnf.genRelationshipGraphfile(model, clusterfile)
gnd.genRelationshipGraphs(dagfile, model)
gnp.genHeatMap(connections, mapping, keys, clusterfile, config.CONN_THRESHOLD)

def hi():
    print ("Hi")
def bye():
    print("Bye")

t1 = threading.Thread(target=hi, name='t1')
t2 = threading.Thread(target=bye, name='t2') 
  
# starting threads
t1.start()
t2.start()
  
# wait until all threads finish
t1.join()
t2.join()
    