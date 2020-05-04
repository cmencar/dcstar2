import pandas as pd
import numpy as np
from data_compression.dataset import dataset
from data_compression.lvq1 import lvq1
from data_compression.K_means import K_means
from data_compression.misc import scatterPlot
from data_compression.misc import create_json
from timeit import default_timer as timer
from datetime import timedelta
import matplotlib.pyplot as plt
from data_compression.dataset import normalized_dataset

original_dataset = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', names=['feature1', 'feature2', 'classes'])
n_p = 20

start = timer()
norm = normalized_dataset(original_dataset)
lvq1 = lvq1(norm, n_p)
compression = dataset(norm)
m_d = compression.get_minimum_boundary()
M_d = compression.get_maximum_boundary()
compression.set_strategy(lvq1)
prototypes = compression.do_compression()
end = timer()
print(timedelta(seconds=end - start))
create_json(m_d, M_d, prototypes)
scatterPlot(norm, m_d, M_d)
scatterPlot(prototypes, m_d, M_d)
plt.show()
