import pandas as pd
from data_compression.compression import compression
from data_compression.lvq1 import lvq1
from data_compression.misc import scatterPlot
from datetime import datetime
import matplotlib.pyplot as plt

colnames = ('f1', 'f2', 'species')
original_dataset = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', names=colnames)
n_p = 3

start = pd.Timestamp.now()
compression = compression(original_dataset)
choice = input('Normalizzare?[S/N]: ')
if choice == "S":
    norm = compression.normalized_dataset()
    m_d = compression.get_minimum_boundary(norm)
    M_d = compression.get_maximum_boundary(norm)
    lvq1 = lvq1(norm, n_p)
else:
    m_d = compression.get_minimum_boundary(original_dataset)
    M_d = compression.get_maximum_boundary(original_dataset)
    lvq1 = lvq1(original_dataset, n_p)
    print("Esecuzione in corso!")

compression.set_strategy(lvq1)
prototypes = compression.do_compression()
end = datetime.now()
print("Timer algoritmo completo:")
timer = pd.Timestamp.now() - start
print(timer)
lvq1.create_json(m_d, M_d, prototypes)
scatterPlot(original_dataset, 0.4)
lvq1.draw_prototypes(prototypes, 0.8)
plt.show()
