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
        normalized_X = preprocessing.scale(X)
        # Union of normalized features with corresponding labels
        list_of_tuples = list(zip(normalized_X[:, 0], normalized_X[:, -1], y))
        df = pd.DataFrame(list_of_tuples, columns=['feature1', 'feature2', 'classes'])
        print(df)
        return df, unique_y

    # Method for initialization of prototypes
    # input: normalized_dataSet, n_prototypes, unique_labels
    # output: prototypes_init
    def init_prot(self, data, n_prototypes, unique_y):
        # calculation number of features
        n_dimension = data.shape[1]
        # I initialize the empty array where I will put the chosen prototypes
        p_init = np.empty((0, n_dimension))
        # Initialize prototypes using random choice.
        for i in range(len(unique_y)):
            # Division of the dataset according to the label examined
            class_data = data.loc[data.classes == unique_y[i]]
            # Calculation of the number of prototypes for the label examined
            np_class = round(len(class_data) / len(data) * n_prototypes)
            # Causal choice of label prototypes examined
            for j in range(np_class):
                x = class_data.sample().to_numpy()
                # Adding the initial prototype chosen in the array
                p_init = np.append(p_init, x, axis=0)
        return p_init

    # Training phase of the lvq1 algorithm
    # Input: normalized_dataset, tolerance, p_init, n_epochs, learning_rate
    # Output: collection of prototypes
    def vector_quantization(self, data, tolerance, p_init, n_epochs, learning_rate):
        # Initializing the flag to determine the end of the cycle do-while
        flag = True
        # Initialization of epochs
        i = 1
        # Copy of the initial prototype array, so you can update them
        prototypes = np.copy(p_init)
        while flag:
            # error initialization
            e = 0
            for index, x in data.iterrows():
                # initialization of the list of distances
                dist = list()
                for j in range(len(prototypes)):
                    # Euclidean distance between the initial prototype and the element of the examined
                    # normalized_dataset
                    distance = np.linalg.norm(prototypes[j][0:-1] - x[0:-1])
                    # Adding the calculated distance to the distance list
                    dist.append((j, distance))
                # Descending order of the distance list
                dist.sort(key=lambda z: z[1])
                # Assignment to variable p of the first element of the ordered distance list (shorter distance)
                p = prototypes[dist[0][0]]
                # Copy of the prototype with shorter distance
                p_old = np.copy(p)
                if x.iloc[-1] == p[-1]:
                    p[0:-1] = np.add(p[0:-1], np.multiply(learning_rate, np.subtract(x[0:-1], p[0:-1]))).to_numpy()
                else:
                    p[0:-1] = np.subtract(p[0:-1], np.multiply(learning_rate, np.subtract(x[0:-1], p[0:-1]))).to_numpy()
                prototypes[dist[0][0]] = p
                # Error Update
                e = e + np.linalg.norm(p - p_old)
            # Increase of the epoch
            i = i + 1
            # Update learning_rate
            learning_rate = learning_rate - (learning_rate / n_epochs)
            # Checking the cycle exit conditions
            if i > n_epochs and e < tolerance:
                flag = False
        return prototypes

