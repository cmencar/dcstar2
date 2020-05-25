import pandas as pd
from data_compression.compression import compression
from data_compression.fcm import fcm
from datetime import datetime

colnames = ('f1', 'f2', 'species')
original_dataset = pd.read_csv('dataset_bidimensionali/datacerchiconcentrici_3classi(pieni)(classiNum).csv', names=colnames)

start = pd.Timestamp.now()
compression = compression(original_dataset)
choice = input('Normalizzare?[S/N]: ')
if choice == "S":
    norm = compression.normalized_dataset()
    fcm = fcm(norm)
else:
    fcm = fcm(original_dataset)
print("Esecuzione in corso!")
compression.set_strategy(fcm)
cluster_label, cluster_center = compression.do_compression()
end = datetime.now()
print("Timer algoritmo completo:")
print(pd.Timestamp.now() - start)
fcm.draw_clusters(cluster_label, cluster_center)
