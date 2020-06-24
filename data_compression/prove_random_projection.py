import numpy as np
from matplotlib.pyplot import scatter
import matplotlib.pyplot as plt
from sklearn import random_projection
import pandas as pd
from sklearn.random_projection import johnson_lindenstrauss_min_dim

ionosphere = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10',
              'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19',
              'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28',
              'f29', 'f30', 'f31', 'f32', 'f33', 'label')
original_dataset = pd.read_csv('dataset_ndimensionali/ionosphere.csv', names=ionosphere)

X = original_dataset.values[:, :-1]

data_normal = (X - X.min()) / (X.max() - X.min())

size = original_dataset.size
print(size)

n_components = johnson_lindenstrauss_min_dim(n_samples=size, eps=0.9)

print(n_components)

transformer = random_projection.GaussianRandomProjection(n_components=2)

X_new = transformer.fit_transform(data_normal)

new_data_normal = (X_new - X_new.min()) / (X_new.max() - X_new.min())

scatter(new_data_normal[:, 0], new_data_normal[:, 1])

plt.show()
