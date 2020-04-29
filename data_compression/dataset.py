from sklearn import preprocessing
import pandas as pd


class dataset:

    def __init__(self, data):
        self.data = data
        self.features = data.iloc[:, :-1]
        self.labels = data.iloc[:, -1]

    # It only takes the features from the dataset
    def get_features(self):
        return self.features

    # It only takes the labels from the dataset
    def get_labels(self):
        return self.labels

    # Delete duplicates from dataset labels to get unique labels
    def get_unique_labels(self):
        return self.data["classes"].unique()

    # Normalization method taken from the sklearn library
    def normalized_dataset(self):
        normalized_features = preprocessing.scale(self.features)
        # Union of normalized features with corresponding labels
        list_of_tuples = list(zip(normalized_features[:, 0], normalized_features[:, -1], self.labels))
        df = pd.DataFrame(list_of_tuples, columns=['feature1', 'feature2', 'classes'])
        return df
