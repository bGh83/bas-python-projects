from datetime import datetime as dt
import os

class config:
    EXP_TS = dt.now().strftime("%d%m%y-%H%M%S")
    CONV_THRESHOLD = 4
    TSNE_RANDOM_STATE=3072018
    PCAP_LOC=os.path.join(os.getcwd(), 'pcaps')
    CONV_LOC=os.path.join(os.getcwd(), 'convs')
    TEST_RESULTS_LOC = os.path.join(os.getcwd(), 'results')
    HDBSCAN_MIN_CLUSTER_SIZE = 7
    HDBSCAN_MIN_SAMPLES = 7
    