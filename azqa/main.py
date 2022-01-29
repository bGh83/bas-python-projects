import pcapreader as pr
import transform as tf

thresh = 20
#connections =pr.getConnectionMap(pr.getPcap ('ISCX_Botnet-Training.pcap'))
connections =pr.getConnectionMap(pr.getPcap ('virut2.pcap'))

connections =pr.removeConnections(connections, thresh)
pr.getConnectionStat(connections)

#distSize = cr.getEuclideanDistanceMatrix(connections, thresh, 2)
#distDelta = cr.getCosineDistanceMatrix(connections, thresh, 0)
#distSport = cr.getCosineDistanceMatrix(connections, thresh, 3)
distDport = tf.getCosineDistanceMatrix(connections, thresh, 4)
    