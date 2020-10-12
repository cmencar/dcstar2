import hdbscan
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.datasets as data
import pandas as pd
from sklearn.datasets import make_blobs

sns.set_color_codes()
plot_kwds = {'alpha': 0.5, 's': 80, 'linewidths': 0}

blobs, labels = make_blobs(n_samples=2000, n_features=10)

# plt.scatter(data_normal.T[0], data_normal.T[1])

clusterer = hdbscan.HDBSCAN()
clusterer.fit(blobs)

# new_dataset = (new_dataset - new_dataset.min()) / (new_dataset.max() - new_dataset.min())
# new_dataset['Cluster'] = clusterer.labels_

labels = set(clusterer.labels_)
labels = list(labels)
print(labels)
for row in blobs.itertuples():
    if row[-1] == labels[0]:
        color = "blue"
    elif row[-1] == labels[1]:
        color = "red"
    else:
        color = "black"
    """elif row[-1] == labels[2]:
        color = "yellow"
    elif row[-1] == labels[3]:
        color = "brown"
    elif row[-1] == labels[4]:
        color = "purple"
    elif row[-1] == labels[5]:
        color = "grey"""

    plt.scatter(row[1], row[2], color=color)

plt.show()