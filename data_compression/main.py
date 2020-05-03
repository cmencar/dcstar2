import pandas as pd
import numpy as np
from data_compression.dataset import dataset
from data_compression.lvq1 import lvq1
from data_compression.K_means import K_means
from data_compression.misc import scatterPlot
from timeit import default_timer as timer
from datetime import timedelta
import matplotlib.pyplot as plt

original_dataset = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', names=['feature1', 'feature2', 'classes'])
n_p = 20
"""
start = timer()
dataset = dataset(original_dataset)
norm = dataset.normalized_dataset()
m_d, M_d = dataset.get_boundary(norm)
compression = lvq1(norm, n_p)
unique_y = dataset.get_unique_labels()
prototypes = compression.algorithm(unique_y)
end = timer()
print(timedelta(seconds=end - start))
compression.create_json(prototypes, m_d, M_d)
scatterPlot(norm, m_d, M_d)
scatterPlot(prototypes, m_d, M_d)
plt.show()
"""
lvq1 = lvq1(original_dataset, n_p)
k_means = K_means()
compression = dataset(original_dataset)
compression.set_strategy(k_means)
compression.compression()

compression.set_strategy(lvq1)
compression.compression()
