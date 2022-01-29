import genconmaps as pcr
import gendistmatrices as tfm
import genplots as gnp
import genmodels as gnm

thresh = 20
#connections =pcr.getConnectionMap(pr.getPcap ('ISCX_Botnet-Training.pcap'))
connections = pcr.getConnectionMap(pcr.getPcap ('virut2.pcap'))

connections = pcr.removeConnections(connections, thresh)
pcr.getConnectionStat(connections)

distSize = tfm.getEuclideanDistanceMatrix(connections, thresh, 2)
distDelta = tfm.getEuclideanDistanceMatrix(connections, thresh, 0)
distSport = tfm.getCosineDistanceMatrix(connections, thresh, 3)
distDport = tfm.getCosineDistanceMatrix(connections, thresh, 4)
distAll = tfm.getDistanceMatrix(distSize, distDelta, distSport, distDport)

gnp.genScatterPlot(gnm.getTSNEProjection(distAll))
