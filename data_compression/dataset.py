from sklearn import preprocessing
import pandas as pd
import numpy as np
from data_compression.compression_strategy import compression_strategy


class dataset:

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
        return self.data["species"].unique()

    def get_minimum_boundary(self):
        minValues = self.data.min()
        m_d = tuple()
        for i in (range(len(minValues) - 1)):
            m_d = m_d + (minValues[i],)
        return m_d

    def get_maximum_boundary(self):
        maxValues = self.data.max()
        M_d = tuple()
        for i in (range(len(maxValues) - 1)):
            M_d = M_d + (maxValues[i],)
        return M_d

    def do_compression(self):
        results = self._strategy.algorithm(self.get_unique_labels())
        return results


def normalized_dataset(df):
    features = df.iloc[:, :-1]
    labels = df.iloc[:, -1]
    data_normal = (features - features.min()) / (features.max() - features.min())
    data_normal['species'] = labels
    return data_normal
