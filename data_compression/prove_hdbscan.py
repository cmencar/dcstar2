import hdbscan
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.datasets as data
import pandas as pd
from sklearn.datasets import make_blobs

sns.set_color_codes()
plot_kwds = {'alpha': 0.5, 's': 80, 'linewidths': 0}

dataset = pd.read_csv("dataset_ndimensionali/iris.csv", names=['1', '2', '3', '4', 'label'])

new_dataset = dataset.iloc[:, :-1]

X = new_dataset.values
data_normal = (X - X.min()) / (X.max() - X.min())

# plt.scatter(data_normal.T[0], data_normal.T[1])

clusterer = hdbscan.HDBSCAN(min_cluster_size=14, algorithm='best', alpha=1.0, approx_min_span_tree=True,
                            gen_min_span_tree=True, leaf_size=40, metric='euclidean')
clusterer.fit_predict(data_normal)

new_dataset = (new_dataset - new_dataset.min()) / (new_dataset.max() - new_dataset.min())
new_dataset['Cluster'] = clusterer.labels_

labels = set(clusterer.labels_)
labels = list(labels)
print(labels)
for row in new_dataset.itertuples():
    if row[-1] == labels[0]:
        color = "blue"
    elif row[-1] == labels[1]:
        color = "red"
    else:
        color = "black"
    """
    elif row[-1] == labels[2]:
        color = "yellow"
    elif row[-1] == labels[3]:
        color = "brown"
    elif row[-1] == labels[4]:
        color = "purple"
    elif row[-1] == labels[5]:
        color = "grey"
    """

    plt.scatter(row[1], row[2], color=color)

plt.show()