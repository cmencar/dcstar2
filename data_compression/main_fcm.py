import pandas as pd
from sklearn.metrics import silhouette_score
from data_compression.compression import compression
from data_compression.fcm import fcm
import numpy as np
from datetime import datetime

colnames = ('f1', 'f2', 'species')
original_dataset = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', names=colnames)
X = original_dataset.values[:, :-1]

start = pd.Timestamp.now()
compression = compression(original_dataset)
# parameters
n_c = 3
m = 1.5

choice = input('Normalizzare?[S/N]: ')
if choice == "S":
    norm = compression.normalized_dataset()
    X = norm.values[:, :-1]
    fcm = fcm(norm, n_clusters=n_c, m=m)
else:
    fcm = fcm(original_dataset, n_clusters=n_c, m=m)
    X = original_dataset.values[:, :-1]

print("Esecuzione in corso!")
compression.set_strategy(fcm)
cluster_label, cluster_center = compression.do_compression()

filename = "bandiera_3_cluster.json"
fcm.create_json(cluster_center, cluster_label, filename)

end = datetime.now()
print("Timer algoritmo completo:")
print(pd.Timestamp.now() - start)
fcm.draw_clusters(cluster_label, cluster_center)

silhouette_avg = silhouette_score(X, cluster_label)
print("The average silhouette_score is :", silhouette_avg)
