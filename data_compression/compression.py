import random
from matplotlib import colors
import matplotlib.pyplot as plt
from data_compression.compression_strategy import compression_strategy


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

    def get_minimum_boundary(self, data):
        minValues = data.min()
        m_d = tuple()
        for i in (range(len(minValues) - 1)):
            m_d = m_d + (minValues[i],)
        return m_d

    def get_maximum_boundary(self, data):
        maxValues = data.max()
        M_d = tuple()
        for i in (range(len(maxValues) - 1)):
            M_d = M_d + (maxValues[i],)
        return M_d

    def normalized_dataset(self):
        data_normal = (self.features - self.features.min()) / (self.features.max() - self.features.min())
        data_normal['label'] = self.labels
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
