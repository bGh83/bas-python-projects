import dpkt, socket, glob, os, statistics, random
from time import perf_counter
import numpy as np
from config import config
from datetime import datetime

THRESHOLD = config.CONV_THRESHOLD
TIMESTAMP = config.EXP_TS
RESULTS_LOC= config.TEST_RESULTS_LOC
PCAP_LOC = config.PCAP_LOC

def getConversations (conversations, keys=[], rows=-1, col=-1):    
    conv = {}
    
    if (len(keys) == 0):
        for key, value in conversations.items():
            keys.append(key)

    for key in keys:
        if ((col == -1) & (rows == -1)):
            conv[key] = [x for x in conversations.get(key)]
        elif ((col > 0) & (rows == -1)):
            conv[key] = [x[col] for x in conversations.get(key)]
        elif ((col == -1) & (rows > 0)):
            conv[key] = [x for x in conversations.get(key)][:rows]
        else:
            conv[key] = [x[col] for x in conversations.get(key)][:rows]        
            
    return conv

def getRandomConversations (conversations, count):        
    samples = {}
    for key in random.sample(conversations.keys(), count):
        samples[key] = conversations[key]
    return samples

def getConversationStat(conversations):
    size = {}
    statfile = os.path.join(RESULTS_LOC,TIMESTAMP+'-con-stat.csv')        
    if not os.path.exists(RESULTS_LOC):
        os.mkdir(RESULTS_LOC)
    outfile = open(statfile, 'w')    
    outfile.write("covnum,connum,ip.src,ip.dst,delta,ip.len,sport,dport,ip.p,timestamp\n")
    
    delta = []
    iplen = []
    timestamp = []    
    cov = 1
    for key, value in conversations.items():
        size[key] = len(value)     
        con = 1
        for v in value:                       
            delta.append(v[0])
            iplen.append(v[1])
            timestamp.append(v[5])
            outfile.write(str(cov)+','+str(con)+','+','.join(key)+","+','.join([str(i) for i in v])+"\n")
            con = con + 1
        cov = cov+1
    
    print ("\nPCAP Stats")
    print("\nRecords from ",
          datetime.utcfromtimestamp(min(timestamp)).strftime('%m/%d/%Y %H:%M:%S %Z'),
          "to",
          datetime.utcfromtimestamp(max(timestamp)).strftime('%m/%d/%Y %H:%M:%S %Z'))    
    print("Conversations [",
          "Total:", len(conversations.values()),
          ";Avg:", round(np.mean(list(size.values()))),
          ";Min:", np.min(list(size.values())),
          ";Max:", np.max(list(size.values())), 
          ";Mode:", str(statistics.mode(list(size.values()))),
          "]")
    
    print("Delta [",
          "Avg:", round(np.mean(delta)),
          ";Min:", np.min(delta),
          ";Max:", np.max(delta), 
          ";Mode:", str(statistics.mode(delta)),
          "]")
    
    print("Bytes [",
          "Avg:", round(np.mean(iplen)),
          ";Min:", np.min(iplen),
          ";Max:", np.max(iplen), 
          ";Mode:", str(statistics.mode(iplen)),
          "]")
    
    print("\nTop 10 Conversations")
    for key, value in sorted(size.items(), key=lambda x: x[1], reverse=True)[:10]:
        print ("-",key[0],"->",key[1],":",value)
        
    outfile.close()
    return size, timestamp


def removeConversations(conversations):
    spkt = 0    
    keys = []
    print("\nRemoving conversations exceeding thresholds...")
    for key, value in conversations.items():        
        if(len(value) < THRESHOLD):
            keys.append(key)
            spkt = spkt+1
    for key in keys:
        del conversations[key]
    print("\nOK. Conversations deleted: ", spkt)
    return conversations

# difference btw current and last packet of same src & dst
def getConversationDelta(key, timestamp, lastTimeStamps):
    ts = datetime.utcfromtimestamp(timestamp)
    delta = 0
    if key in lastTimeStamps:
        delta = (ts - lastTimeStamps[key]).microseconds / 1000
    lastTimeStamps[key] = ts
    return delta, lastTimeStamps

def getConversationMaps():
    pcaps = glob.glob(PCAP_LOC+"/*.pcap")
    conversations = {}
    count = len(pcaps)
    print("\nTotal ",count," pcaps...")
    for pcap in pcaps:        
        name = os.path.basename(pcap)
        print("\nGenerating conversation map from [",name,"]...")
        if count == 1:
           name = ''
        file = open(pcap, 'rb')        
        conversations.update(getConversationMap(dpkt.pcap.Reader(file), name))
        file.close()        
    return conversations

def getConversationMap(pcap, name):
           
    start = perf_counter()
    skipped = 0  # skipped packets
    total = 0  # total packets
    conversations = {}
    lastTimeStamps = {}  # keeps a list of last timestamp of a conversation    
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
            delta, lastTimeStamps = getConversationDelta(
                key, timestamp, lastTimeStamps)

            # set value for map
            value = (
                delta,                
                ip.len,
                sport,
                dport,
                ip.p,
                timestamp)

            # add all to map
            if key not in conversations.keys():
                conversations[key] = []
            conversations[key].append(value)

        except Exception as e:
            print(e)
        total = total + 1

    print("OK. (", round(perf_counter()-start), "s ) Total Packets: ",
          total, "; Skipped Packets: ", skipped, "\n")
    return conversations
