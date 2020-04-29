import pandas as pd
import numpy as np
from data_compression.dataset import dataset
from sklearn.model_selection import train_test_split
from data_compression.lvq1 import lvq1
from data_compression.misc import scatterPlot
from timeit import default_timer as timer
from datetime import timedelta

original_dataset = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', names=['feature1', 'feature2', 'classes'])
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
n_p = 20
start = timer()
dataset = dataset(data=original_dataset)
norm = dataset.normalized_dataset()
lvq1 = lvq1(norm, n_p)
unique_y = dataset.get_unique_labels()
p_init = lvq1.init_prot(unique_y)
prototypes = lvq1.vector_quantization(p_init)
print(type(prototypes))
end = timer()
print(timedelta(seconds=end - start))
"""
results = pd.DataFrame(prototypes, columns=['feature1', 'feature2', 'classes'])

"""
# results.to_json(r'test/Json_prototypes/bandiera_10.json', orient='records')
# scatterPlot(results)

