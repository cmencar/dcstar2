import pandas as pd
import numpy as np
from data_compression.dataset import dataset
from data_compression.lvq1 import lvq1
from data_compression.K_means import K_means
from data_compression.misc import scatterPlot
from data_compression.misc import create_json
from datetime import datetime
import matplotlib.pyplot as plt
from data_compression.dataset import normalized_dataset

original_dataset = pd.read_csv('dataset_bidimensionali/banana.csv', names=['feature1', 'feature2', 'classes'])
n_p = 20

start = pd.Timestamp.now()
norm = normalized_dataset(original_dataset)
lvq1 = lvq1(original_dataset, n_p)
compression = dataset(original_dataset)
m_d = compression.get_minimum_boundary()
M_d = compression.get_maximum_boundary()
compression.set_strategy(lvq1)
prototypes = compression.do_compression()
end = datetime.now()
print("Timer algoritmo completo:")
print(pd.Timestamp.now() - start)
create_json(m_d, M_d, prototypes)
# scatterPlot(original_dataset, m_d, M_d)
# scatterPlot(prototypes, m_d, M_d)
plt.show()

