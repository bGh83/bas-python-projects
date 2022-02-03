import dpkt, datetime, socket, glob, os
from time import perf_counter
import numpy as np
from config import config

PCAP_LOC= config.PCAP_LOC

def getConnectionStat(connections):
    size = []
    for key, value in connections.items():
        size.append(len(value))
    print("Connection Stat [",
          " Cnt: ", len(connections.values()),
          "; Avg: ", round(np.mean(size)),
          "; Min: ", np.min(size),
          "; Max: ", np.max(size), "]")


def removeConnections(connections, threshold):
    spkt = 0
    keys = []
    print("\nRemoving connections below threshold [", threshold, "]...")
    for key, value in connections.items():
        if(len(value) < threshold):
            keys.append(key)
            spkt = spkt+1
    for key in keys:
        del connections[key]
    print("\nOK. Connections deleted: ", spkt)
    return connections

# difference btw current and last packet of same src & dst
def getConnectionDelta(key, timestamp, lastTimeStamps):
    ts = datetime.datetime.utcfromtimestamp(timestamp)
    delta = 0
    if key in lastTimeStamps:
        delta = (ts - lastTimeStamps[key]).microseconds / 1000
    lastTimeStamps[key] = ts
    return delta, lastTimeStamps

def getConnectionMaps():
    pcaps = glob.glob(PCAP_LOC+"/*.pcap")    
    connections = {}
    count = len(pcaps)
    print("\nTotal ",count," pcaps...")
    for pcap in pcaps:        
        name = os.path.basename(pcap)
        print("\nGenerating connection map from [",name,"]...")
        if count == 1:
            name = ''
        connections = (getConnectionMap(getPcap(pcap), name))
    return connections

def getConnectionMap(pcap, name):
           
    start = perf_counter()
    skipped = 0  # skipped packets
    total = 0  # total packets
    connections = {}
    lastTimeStamps = {}  # keeps a list of last timestamp of a connection    
    for (timestamp, packet) in pcap:
        try:

            eth = dpkt.ethernet.Ethernet(packet)
            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                skipped = skipped + 1
                continue

            ip = eth.data

            # get ports
            sport = 0
            dport = 0
            try:
                if ip.p in (dpkt.ip.IP_PROTO_TCP, dpkt.ip.IP_PROTO_UDP):
                    sport = ip.data.sport
                    dport = ip.data.dport
            except:
                skipped = skipped + 1
                continue

            # get ips
            ipsrc = socket.inet_ntoa(ip.src)
            ipdst = socket.inet_ntoa(ip.dst)

            # set key for map (filename, src, dst)
            if(name == ''):
                key = (ipsrc, ipdst)
            else:
                key = (name, ipsrc, ipdst)

            # get delta and update lastTimeStamps with latest timestamp
            delta, lastTimeStamps = getConnectionDelta(
                key, timestamp, lastTimeStamps)

            # set value for map
            value = (
                delta,
                ip.p,
                ip.len,
                sport,
                dport)

            # add all to map
            if key not in connections.keys():
                connections[key] = []
            connections[key].append(value)

        except Exception as e:
            print(e)
        total = total + 1
    print("OK. (", round(perf_counter()-start), "s ) Total Packets: ",
          total, "; Skipped Packets: ", skipped, "\n")
    return connections


def getPcap(filename):
    pcap = dpkt.pcap.Reader(open(filename, 'rb'))
    return pcap
