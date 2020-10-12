import pandas as pd
from data_compression.Compression import Compression
from data_compression.Fcm import Fcm
from data_compression.Fcm2 import Fcm2
from datetime import datetime
import matplotlib.pyplot as plt

original_dataset = pd.read_csv('dataset_bidimensionali/datasetSynt19.csv', header=None)
X = original_dataset.values[:, :-1]

compression = Compression(original_dataset)
# parameters
n_c = 3
m = 1.5

choice = input('Normalizzare?[S/N]: ')
if choice == "S":
    norm = compression.normalized_dataset()
    fcm = Fcm2(norm, n_p=24, m=2)
else:
    fcm = Fcm2(original_dataset, n_p=24, m=1.7)

start = pd.Timestamp.now()
print("Esecuzione in corso!")
compression.set_strategy(fcm)
prototypes = compression.do_compression()

end = datetime.now()
print("Timer algoritmo completo:")
print(pd.Timestamp.now() - start)
compression.draw_data()
fcm.draw_prototypes(prototypes=prototypes, alpha=1)
plt.show()
# print('Silhouette Coefficient: %0.3f' % metrics.silhouette_score(X, cluster_label))
