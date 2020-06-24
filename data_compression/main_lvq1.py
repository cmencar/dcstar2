import pandas as pd
from data_compression.compression import compression
from data_compression.lvq1 import lvq1
from data_compression.misc import scatterPlot
from datetime import datetime
import matplotlib.pyplot as plt


col_ionosphere = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10',
                  'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19',
                  'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28',
                  'f29', 'f30', 'f31', 'f32', 'f33', 'label')
col_shuttle = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'label')
col_iris = ('f1', 'f2', 'f3', 'f4', 'label')
col_bandiera = ('f1', 'f2', 'label')

original_dataset = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', names=col_bandiera)
n_p = 21

start = pd.Timestamp.now()
compression = compression(original_dataset)
choice = input('Normalizzare?[S/N]: ')
if choice == "S":
    norm = compression.normalized_dataset()
    scatterPlot(norm, 0.4)
    lvq1 = lvq1(norm, n_p)
else:
    scatterPlot(original_dataset, 0.4)
    lvq1 = lvq1(original_dataset, n_p)
print("Esecuzione in corso!")

compression.set_strategy(lvq1)
prototypes = compression.do_compression()
end = datetime.now()
print("Timer algoritmo completo:")
timer = pd.Timestamp.now() - start
print(timer)
lvq1.create_json(prototypes, filename="prove.json")
lvq1.draw_prototypes(prototypes, 0.8)
plt.show()
