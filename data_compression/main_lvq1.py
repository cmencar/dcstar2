import pandas as pd
from data_compression.Compression import Compression
from data_compression.Lvq1 import Lvq1
from datetime import datetime
import matplotlib.pyplot as plt


original_dataset = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', header=None)
n_p = 21

start = pd.Timestamp.now()
compression = Compression(original_dataset)
choice = input('Normalizzare?[S/N]: ')
if choice == "S":
    norm = compression.normalized_dataset()
    lvq1 = Lvq1(norm, n_p)
else:
    lvq1 = Lvq1(original_dataset, n_p)
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
compression.draw_prototypes(prototypes, 1.0)
plt.show()
