import pandas as pd
import numpy as np
from data_compression.dataset import dataset
from data_compression.lvq1 import lvq1
from data_compression.FCM import FCM
from data_compression.misc import scatterPlot
from data_compression.misc import create_json
from datetime import datetime
import matplotlib.pyplot as plt
from data_compression.dataset import normalized_dataset

colnames = ('f1', 'f2', 'species')
original_dataset = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', names=colnames)
n_p = 42

start = pd.Timestamp.now()
norm = normalized_dataset(original_dataset)
print(norm)
lvq1 = lvq1(norm, n_p)
compression = dataset(norm)
m_d = compression.get_minimum_boundary()
M_d = compression.get_maximum_boundary()
compression.set_strategy(lvq1)
prototypes = compression.do_compression()
df = pd.DataFrame(prototypes, columns=colnames)
end = datetime.now()
print("Timer algoritmo completo:")
print(pd.Timestamp.now() - start)
create_json(m_d, M_d, prototypes)
scatterPlot(original_dataset, 0.4)
scatterPlot(df, 0.8)
plt.show()
