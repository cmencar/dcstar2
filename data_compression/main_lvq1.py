import pandas as pd
from sklearn import random_projection
from data_compression.compression import compression
from data_compression.lvq1 import lvq1
from datetime import datetime
import matplotlib.pyplot as plt


col_ionosphere = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10',
            'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19',
            'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28',
            'f29', 'f30', 'f31', 'f32', 'f33', 'label')
col_shuttle = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'label')
col_iris = ('f1', 'f2', 'f3', 'f4', 'label')
col_banana = ('f1', 'f2', 'label')
original_dataset = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', names=col_banana)
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
lvq1.create_json(prototypes, filename)
compression.draw_data()
lvq1.draw_prototypes(prototypes, 1.0)
plt.show()
