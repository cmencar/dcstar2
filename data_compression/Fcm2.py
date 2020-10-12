import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from seaborn import scatterplot as scatter
import skfuzzy as fuzz

from data_compression.Compression_strategy import Compression_strategy


class Fcm2(Compression_strategy):

    def __init__(self, data, n_p=3, n_epochs=100, m=1.7):

        super().__init__(data)
        self.n_c = int(n_p/self.get_n_class_data())
        self.n_epochs = n_epochs
        self.m = m

    def get_data_features(self, data):
        df_features = data.iloc[:, :-1]
        return df_features

    def get_n_class_data(self):
        n_classes = len(self.data.iloc[:, -1].unique())
        return n_classes

    def algorithm(self):
        start = pd.Timestamp.now()
        unique_y = self.data.iloc[:, -1].unique()
        prototypes = []
        for i in range(len(unique_y)):
            class_data = self.data.loc[self.data.iloc[:, -1] == unique_y[i]]
            data = class_data.T.values[:-1, :]
            # fit the fuzzy-c-means
            fcm_centers, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(data, self.n_c, 2, error=0.005, maxiter=1000, init=None)
            fcm_centers = fcm_centers.tolist()
            for z in range(len(fcm_centers)):
                fcm_centers[z].append(unique_y[i])
                prototypes.append(fcm_centers[z])
        prototypes = np.array(prototypes)
        print("Tempo esecuzione algoritmo")
        print(pd.Timestamp.now() - start)
        return prototypes

    def draw_clusters(self, cluster_label, cluster_center):
        X = self.data.iloc[:, :-1].to_numpy()
        f, axs = plt.subplots(1, 2, figsize=(11, 5))
        scatter(X[:, 0], X[:, 1], ax=axs[0])
        scatter(X[:, 0], X[:, 1], ax=axs[1], hue=cluster_label)
        scatter(cluster_center[:, 0], cluster_center[:, 1], ax=axs[1], marker=">", s=200)

    def draw_prototypes(self, prototypes, alpha):
        labels = set(prototypes[:, -1])
        labels = list(labels)
        data = pd.DataFrame(data=prototypes)
        for row in data.itertuples():
            if row[-1] == labels[0]:
                color = "red"
            elif row[-1] == labels[1]:
                color = "green"
            else:
                color = "blue"
            plt.scatter(row[1], row[2], color=color, alpha=alpha)
        plt.show()