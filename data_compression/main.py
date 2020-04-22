from lvq1 import lvq1
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from lvq1 import scatterplot

dataSet = pd.read_csv('dataset_bidimensionali/bandiera(classiNum).csv', names=['feature1', 'feature2', 'classes'])
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
lr = 0.1
n_iter = 30
n_p = 20
tol = 5
lvq1 = lvq1(dataSet, n_p, n_iter, lr, tol)
norm, unique_y = lvq1.normalized_dataset(dataSet)
p_init = lvq1.init_prot(dataSet, n_p, unique_y)
results = lvq1.vector_quantization(dataSet, tol, p_init, n_iter, lr)
results = pd.DataFrame(results, columns=['feature1', 'feature2', 'classes'])
# results.to_json(r'test/Json_prototypes/bandiera_10.json', orient='records')
scatterplot(results)

