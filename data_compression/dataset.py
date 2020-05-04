from sklearn import preprocessing
import pandas as pd
from data_compression.compression_algorithm import Compression


class dataset:

    def __init__(self, data, strategy: Compression = None):
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
        return self.data["classes"].unique()

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


# Normalization method taken from the sklearn library
def normalized_dataset(df):
    normalized_features = preprocessing.scale(df.iloc[:, :-1])
    labels = df.iloc[:, -1]
    # Union of normalized features with corresponding labels
    list_of_tuples = list(zip(normalized_features[:, 0], normalized_features[:, -1], labels))
    df = pd.DataFrame(list_of_tuples, columns=['feature1', 'feature2', 'classes'])
    return df
