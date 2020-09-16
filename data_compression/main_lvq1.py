import pandas as pd
from sklearn import random_projection
from data_compression.compression import compression
from data_compression.lvq1 import lvq1
from datetime import datetime
import matplotlib.pyplot as plt


original_dataset = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', header=None)
n_p = 21

start = pd.Timestamp.now()
compression = compression(original_dataset)
choice = input('Normalizzare?[S/N]: ')
if choice == "S":
    norm = compression.normalized_dataset()
    lvq1 = lvq1(norm, n_p)
else:
    lvq1 = lvq1(original_dataset, n_p)
print("Esecuzione in corso!")

compression.set_strategy(lvq1)
prototypes = compression.do_compression()
end = datetime.now()
print("Timer algoritmo completo:")
timer = pd.Timestamp.now() - start
print(timer)
filename = "bandiera_100_21.json"
compression.create_json(prototypes, filename)
compression.draw_data()
lvq1.draw_prototypes(prototypes, 1.0)
plt.show()
