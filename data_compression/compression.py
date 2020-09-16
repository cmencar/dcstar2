import matplotlib.pyplot as plt
from data_compression.compression_strategy import compression_strategy
import json
import numpy as np


class compression:

    def __init__(self, data, strategy: compression_strategy = None):
        self.data = data
        self.features = data.iloc[:, :-1]
        self.labels = data.iloc[:, -1]
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    # It only takes the features from the dataset
    def get_features(self):
        return self.features

    # It only takes the labels from the dataset
    def get_labels(self):
        return self.labels

    # Delete duplicates from dataset labels to get unique labels
    def get_unique_labels(self):
        return self.data[:, -1].unique()

    def normalized_dataset(self):
        data_normal = (self.features - self.features.min()) / (self.features.max() - self.features.min())
        data_normal[-1] = self.labels
        return data_normal

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

    def do_compression(self):
        results = self._strategy.algorithm()
        return results

    def create_json(self, prototypes, filename):
        point_coordinates = prototypes[:, :-1].astype(np.float).tolist()
        point_labels = prototypes[:, -1].tolist()
        m_d = self.get_min_boundary(point_coordinates)
        M_d = self.get_max_boundary(point_coordinates)
        point_id = list()
        for i in point_coordinates:
            point_id.append(point_coordinates.index(i))

        data = {'points': [], 'm_d': m_d, 'M_d': M_d}
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
        minPrototype = np.amin(point_coordinates, axis=0)
        minDataset = self.normalized_dataset().min(axis=0)[:-1].tolist()
        return [a if a <= b else b for a, b in zip(minPrototype, minDataset)]

    def get_max_boundary(self, point_coordinates):
        maxPrototype = np.amax(point_coordinates, axis=0)
        maxDataset = self.normalized_dataset().max(axis=0)[:-1].tolist()
        return [a if a >= b else b for a, b in zip(maxPrototype, maxDataset)]
