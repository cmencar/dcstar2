import pandas as pd
import numpy as np
from data_compression.compression import compression
from data_compression.lvq1 import lvq1
from data_compression.fcm import fcm
from data_compression.misc import scatterPlot
from data_compression.misc import create_json
from datetime import datetime
import matplotlib.pyplot as plt
from seaborn import scatterplot as scatter
from data_compression.compression import normalized_dataset

colnames = ('f1', 'f2', 'species')
original_dataset = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', names=colnames)
n_p = 20

start = pd.Timestamp.now()
norm = normalized_dataset(original_dataset)
lvq1 = lvq1(norm, n_p)
# fcm = fcm(norm)
compression = compression(norm)
m_d = compression.get_minimum_boundary()
M_d = compression.get_maximum_boundary()
compression.set_strategy(lvq1)
prototypes = compression.do_compression()
# cluster_label, cluster_center = compression.do_compression()
end = datetime.now()
print("Timer algoritmo completo:")
print(pd.Timestamp.now() - start)
create_json(m_d, M_d, prototypes)
# fcm.draw_clusters(cluster_label, cluster_center)
scatterPlot(original_dataset, 0.4)
scatterPlot(prototypes, 0.8)
# plt.show()
