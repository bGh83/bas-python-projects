import csv
import os
from config import config

TIMESTAMP = config.EXP_TS
RESULTS_LOC = config.TEST_RESULTS_LOC

def genClusterfile(model, labels, mapping, inv_mapping):
    final_clusters = {}
    final_probs = {}
    for lab in set(model.labels_):
        occ = [i for i, x in enumerate(model.labels_) if x == lab]
        final_probs[lab] = [x for i, x in zip(
            model.labels_, model.probabilities_) if i == lab]
        print("cluster: " + str(lab) + " num items: " +
              str(len([labels[x] for x in occ])))
        final_clusters[lab] = [labels[x] for x in occ]

    clusterfile = os.path.join(RESULTS_LOC,TIMESTAMP+'-cluster-data.csv')
    outfile = open(clusterfile, 'w')
    outfile.write("clusnum,connnum,probability,class,filename,srcip,dstip\n")

    for n, clus in final_clusters.items():
        for idx, el in enumerate([inv_mapping[x] for x in clus]):
            ip = el.split('->')
            if '-' in ip[0]:
                classname = el.split('-')[1]
            else:
                classname = el.split('.pcap')[0]
                filename = el.split('.pcap')[0]
                outfile.write(str(n)+","+str(mapping[el])+","+str(final_probs[n][idx])+","+str(
                    classname)+","+str(filename)+","+ip[0]+","+ip[1]+"\n")
    outfile.close()
    return clusterfile


def genRelationshipGraphfile(model, clusterfile):
    print('Producing DAG with relationships between pcaps')
    clusters = {}
    numclus = len(set(model.labels_))
    with open(clusterfile, 'r') as f1:
        reader = csv.reader(f1, delimiter=',')
        for i, line in enumerate(reader):
            if i > 0:
                if line[4] not in clusters.keys():
                    clusters[line[4]] = []
                clusters[line[4]].append(
                    (line[3], line[0]))  # classname, cluster#

    f1.close()
    array = [str(x) for x in range(numclus-1)]
    array.append("-1")

    treeprep = dict()
    for filename, val in clusters.items():
        arr = [0]*numclus
        for fam, clus in val:
            ind = array.index(clus)
            arr[ind] = 1
        mas = ''.join([str(x) for x in arr[:-1]])
        famname = fam        
        if mas not in treeprep.keys():
            treeprep[mas] = dict()
        if famname not in treeprep[mas].keys():
            treeprep[mas][famname] = set()
        treeprep[mas][famname].add(str(filename))

    filename = os.path.join(RESULTS_LOC, TIMESTAMP+'-mas-details.csv')
    f2 = open(filename, 'w')
    for k, v in treeprep.items():
        for kv, vv in v.items():
            f2.write(str(k)+';'+str(kv)+';'+str(len(vv))+'\n')
    f2.close()
    return filename