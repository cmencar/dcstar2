import matplotlib.pyplot as plt
from data_compression.CompressionStrategy import CompressionStrategy
from seaborn import scatterplot as scatter
import pandas as pd
import json
import numpy as np


class Compression:

    def __init__(self, data, strategy: CompressionStrategy = None):
        self.data = data
        self.features = data.iloc[:, :-1]
        self.labels = data.iloc[:, -1]
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def get_strategy(self):
        return self._strategy

    # It only takes the features from the dataset
    def get_features(self):
        return self.features

    # It only takes the labels from the dataset
    def get_labels(self):
        return self.labels

    # Delete duplicates from dataset labels to get unique labels
    def get_unique_labels(self):
        return self.data[:, -1].unique()

    # Normalize the dataset
    def normalized_dataset(self):
        data_normal = (self.features - self.features.min()) / (self.features.max() - self.features.min())
        data_normal[-1] = self.labels
        return data_normal

    # Create the original dataset chart
    def draw_data(self):
        labels = set(self.labels)
        labels = list(labels)
        for row in self.normalized_dataset().itertuples():
            if row[-1] == labels[0]:
                color = "red"
            elif row[-1] == labels[1]:
                color = "green"
            else:
                color = "blue"
            plt.scatter(row[1], row[2], color=color, alpha=0.2)

    # Create the graph of the prototypes derived from the original dataset
    @staticmethod
    def draw_prototypes(prototypes, alpha):
        # Inserting labels into a set
        labels = set(prototypes[:, -1])
        # Transformation of the set into a list
        labels = list(labels)
        # Creation of a DataFrame containing the prototypes
        data = pd.DataFrame(data=prototypes)
        # 
        for row in data.itertuples():
            if row[-1] == labels[0]:
                color = "red"
            elif row[-1] == labels[1]:
                color = "green"
            else:
                color = "blue"
            plt.scatter(row[1], row[2], color=color, alpha=alpha)

    def draw_clusters(self, cluster_label, cluster_center):
        X = self.data.iloc[:, :-1].to_numpy()
        f, axs = plt.subplots(1, 2, figsize=(11, 5))
        scatter(X[:, 0], X[:, 1], ax=axs[0])
        scatter(X[:, 0], X[:, 1], ax=axs[1], hue=cluster_label)
        scatter(cluster_center[:, 0], cluster_center[:, 1], ax=axs[1], marker=">", s=200)

    def do_compression(self):
        results = self._strategy.algorithm()
        return results

    def create_json(self, prototypes, filename):
        point_coordinates = prototypes[:, :-1].astype(np.float).tolist()
        point_labels = prototypes[:, -1].tolist()
        min_d = self.get_min_boundary(point_coordinates)
        max_d = self.get_max_boundary(point_coordinates)
        # min_d = self.get_min_boundary_only_ds()
        # max_d = self.get_max_boundary_only_ds()
        point_id = list()
        for i in point_coordinates:
            point_id.append(point_coordinates.index(i))

        data = {'points': [], 'min_d': min_d, 'max_d': max_d}
        for i in range(len(point_coordinates)):
            coordinates = point_coordinates[i]
            data['points'].append({
                'coordinates': coordinates,
                'class': point_labels[i],
                'name': "point" + str(point_id[i] + 1)
            })

        with open(filename, 'w') as output:
            json.dump(data, output, indent=1)

    def get_min_boundary(self, point_coordinates):
        min_prototype = np.amin(point_coordinates, axis=0)
        min_dataset = self.normalized_dataset().min(axis=0)[:-1].tolist()
        return [a if a <= b else b for a, b in zip(min_prototype, min_dataset)]

    def get_max_boundary(self, point_coordinates):
        max_prototype = np.amax(point_coordinates, axis=0)
        max_dataset = self.normalized_dataset().max(axis=0)[:-1].tolist()
        return [a if a >= b else b for a, b in zip(max_prototype, max_dataset)]

    def get_min_boundary_only_ds(self):
        min_dataset = self.normalized_dataset().min(axis=0)[:-1].tolist()
        return min_dataset

    def get_max_boundary_only_ds(self):
        max_dataset = self.normalized_dataset().max(axis=0)[:-1].tolist()
        return max_dataset
