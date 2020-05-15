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

X = original_dataset.iloc[:, :-1].to_numpy()

start = pd.Timestamp.now()
norm = normalized_dataset(original_dataset)
lvq1 = lvq1(norm, n_p)
fcm = fcm(norm)
compression = compression(norm)
m_d = compression.get_minimum_boundary()
M_d = compression.get_maximum_boundary()
compression.set_strategy(fcm)
# prototypes = compression.do_compression()
cluster_label, cluster_center = compression.do_compression()
print(type(cluster_center))
print(type(cluster_label))
# df = pd.DataFrame(prototypes, columns=colnames)
end = datetime.now()
print("Timer algoritmo completo:")
print(pd.Timestamp.now() - start)
# fcm.create_json(m_d, M_d, cluster_label, cluster_center)
f, axs = plt.subplots(1, 2, figsize=(11, 5))
scatter(X[:, 0], X[:, 1], ax=axs[0])
scatter(X[:, 0], X[:, 1], ax=axs[1], hue=cluster_label)
scatter(cluster_center[:, 0], cluster_center[:, 1], ax=axs[1], marker=">", s=200)
plt.show()
# scatterPlot(original_dataset, 0.4)
# scatterPlot(df, 0.8)
# plt.show()
