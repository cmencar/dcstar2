import pandas as pd
import numpy as np
from data_compression.dataset import dataset
from data_compression.lvq1 import lvq1
from data_compression.misc import scatterPlot
from timeit import default_timer as timer
from datetime import timedelta
import matplotlib.pyplot as plt

original_dataset = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', names=['feature1', 'feature2', 'classes'])
n_p = 20

start = timer()
dataset = dataset(data=original_dataset)
norm = dataset.normalized_dataset()
m_d, M_d = dataset.get_boundary(norm)
lvq1 = lvq1(norm, n_p)
unique_y = dataset.get_unique_labels()
p_init = lvq1.init_prot(unique_y)
prototypes = lvq1.vector_quantization(p_init)
end = timer()
print(timedelta(seconds=end - start))
lvq1.create_json(prototypes, m_d, M_d)
scatterPlot(norm, m_d, M_d)
scatterPlot(prototypes, m_d, M_d)
plt.show()
