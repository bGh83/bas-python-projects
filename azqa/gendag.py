import csv, os
from config import config
from collections import deque


TIMESTAMP = config.EXP_TS
RESULTS_LOC = config.TEST_RESULTS_LOC
DOT_LOC = os.path.join(RESULTS_LOC, TIMESTAMP+'-relation-tree.dot')
DAG_LOC = os.path.join(RESULTS_LOC, TIMESTAMP+'-DAG.png')

def difference(str1, str2):
    return sum([str1[x]!=str2[x] for x in range(len(str1))])

def genRelationshipGraphs(filename, model):
    with open(filename, 'rU') as f3:
        
        csv_reader = csv.reader(f3, delimiter=';')
        graph = {}
        names = {}
        numclus = len(set(model.labels_))
        
        for line in csv_reader:
            graph[line[0]] = set()
            if line[0] not in names.keys():
                names[line[0]] = []
            names[line[0]].append(line[1]+"("+line[2]+")")

        zeros = ''.join(['0']*(numclus-1))
        if zeros not in graph.keys():
            graph[zeros] = set()

        ulist = graph.keys()
        covered = set()
        next = deque()

        specials = []

        next.append(zeros)

        while(len(next) > 0):
            l1 = next.popleft()
            covered.add(l1)
            for l2 in ulist:
                if l2 not in covered and difference(l1, l2) == 1:
                    graph[l1].add(l2)
                    if l2 not in next:
                        next.append(l2)

        val = set()
        for v in graph.values():
            val.update(v)

        notmain = [x for x in ulist if x not in val]
        notmain.remove(zeros)
        nums = [sum([int(y) for y in x]) for x in notmain]
        notmain = [x for _, x in sorted(zip(nums, notmain))]
        specials = notmain
        extras = set()

        for nm in notmain:
            comp = set()
            comp.update(val)
            comp.update(extras)

            mindist = 1000
            minli1, minli2 = None, None
            for l in comp:
                if nm != l:
                    diff = difference(nm, l)
                    if diff < mindist:
                        mindist = diff
                        minli = l

            diffbase = difference(nm, zeros)
            if diffbase <= mindist:
                mindist = diffbase
                minli = zeros
            num1 = sum([int(s) for s in nm])
            num2 = sum([int(s) for s in minli])
            if num1 < num2:
                graph[nm].add(minli)
            else:
                graph[minli].add(nm)

            extras.add(nm)

        val = set()
        for v in graph.values():
            val.update(v)
            f2 = open(DOT_LOC, 'w')
            f2.write("digraph dag {\n")
            f2.write("rankdir=LR;\n")
            num = 0
            for idx, li in names.items():
                text = ''               
                name = str(idx)+'\n'

                for l in li:
                    name += l+',\n'
                if idx not in specials:
                    text = str(idx) + " [label=\""+name+"\" , shape=box;]"
                else:
                    text = str(idx) + " [shape=box label=\""+name+"\"]"

                f2.write(text)
                f2.write('\n')
            for k, v in graph.items():
                for vi in v:
                    f2.write(str(k)+"->"+str(vi))
                    f2.write('\n')
            f2.write("}")
            f2.close()

        # Rendering DAG
        print('Rendering DAG -- needs graphviz dot')
        try:
            os.system('dot -Tpng ' +DOT_LOC+' -o '+DAG_LOC)
            print('Done')
        except:
            print('Failed')
            pass
