import pandas as pd
import numpy as np
from data_compression.dataset import dataset
from sklearn.model_selection import train_test_split
from data_compression.lvq1 import lvq1
from data_compression.misc import scatterPlot
from timeit import default_timer as timer
from datetime import timedelta

dataSet = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', names=['feature1', 'feature2', 'classes'])
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
lr = 0.1
n_iter = 10
n_p = 20
tol = 5
lvq1 = lvq1(dataSet, n_p, n_iter, lr, tol)
dataset = dataset(data=dataSet)

start = timer()
norm = dataset.normalized_dataset()
unique_y = dataset.get_unique_labels()
p_init = lvq1.init_prot(norm, n_p, unique_y)
prototypes = lvq1.vector_quantization(norm, tol, p_init, n_iter, lr)
results = pd.DataFrame(prototypes, columns=['feature1', 'feature2', 'classes'])
end = timer()
print(timedelta(seconds=end - start))

# results.to_json(r'test/Json_prototypes/bandiera_10.json', orient='records')
# scatterPlot(results)

