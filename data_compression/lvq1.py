import numpy as np
import pandas as pd
from sklearn import preprocessing


class lvq1:

    def __init__(self, data, n_prototypes, n_epochs, learning_rate, tolerance):

        self.data = data
        self.n_prototypes = n_prototypes
        self.n_epochs = n_epochs
        self.learning_rate = learning_rate
        self.tolerance = tolerance

    # Method for the normalization of the initial dataset
    # input: dataSet
    # output: normalized_dataset, unique_labels
    def normalized_dataset(self, data):
        # It only takes the features from the dataset
        X = data.iloc[:, :-1]
        # It only takes the labels from the dataset
        y = data.iloc[:, -1]
        # Delete duplicates from dataset labels to get unique labels
        unique_y = data["classes"].unique()
        # Normalization method taken from the sklearn library
        normalized_X = preprocessing.normalize(X)
        # Union of normalized features with corresponding labels
        list_of_tuples = list(zip(normalized_X[:, 0], normalized_X[:, -1], y))
        df = pd.DataFrame(list_of_tuples, columns=['feature1', 'feature2', 'classes'])
        return df, unique_y

    def init_prot(self, data, n_prototypes, unique_y):
        n_dimension = data.shape[1]
        p_init = np.empty((0, n_dimension))
        # Initialize prototypes using random choice.
        for i in range(len(unique_y)):
            class_data = data.loc[data.classes == unique_y[i]]
            np_class = round(len(class_data) / len(data) * n_prototypes)
            for j in range(np_class):
                x = class_data.sample().to_numpy()
                p_init = np.append(p_init, x, axis=0)
        return p_init

    def vector_quantization(self, data, tolerance, p_init, n_epochs, learning_rate):
        flag = True
        i = 1
        prototypes = np.copy(p_init)
        while flag:
            e = 0
            for index, x in data.iterrows():
                dist = list()
                for j in range(len(prototypes)):
                    distance = np.linalg.norm(prototypes[j][0:-1] - x[0:-1])
                    dist.append((j, distance))
                dist.sort(key=lambda z: z[1])
                p = prototypes[dist[0][0]]
                p_old = np.copy(p)
                if x.iloc[-1] == p[-1]:
                    p[0:-1] = np.add(p[0:-1], np.multiply(learning_rate, np.subtract(x[0:-1], p[0:-1]))).to_numpy()
                else:
                    p[0:-1] = np.subtract(p[0:-1], np.multiply(learning_rate, np.subtract(x[0:-1], p[0:-1]))).to_numpy()
                prototypes[dist[0][0]] = p
                e = e + np.linalg.norm(p - p_old)
            i = i + 1
            learning_rate = learning_rate - (learning_rate / n_epochs)
            if i > n_epochs and e < tolerance:
                flag = False
        return prototypes

