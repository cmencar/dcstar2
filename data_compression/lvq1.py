import numpy as np
import pandas as pd
from data_compression.compression_algorithm import compression_algorithm
import json


class lvq1(compression_algorithm):

    def __init__(self, data, n_prototypes, n_epochs=10, learning_rate=0.1, tolerance=5):

        self.data = data
        self.n_prototypes = n_prototypes
        self.n_epochs = n_epochs
        self.learning_rate = learning_rate
        self.tolerance = tolerance

    # Method for initialization of prototypes
    # input: normalized_dataSet, n_prototypes, unique_labels
    # output: prototypes
    def algorithm(self, unique_y):
        # calculation number of features
        n_dimension = self.data.shape[1]
        # I initialize the empty array where I will put the chosen prototypes
        p_init = np.empty((0, n_dimension))
        # Initialize prototypes using random choice.
        for i in range(len(unique_y)):
            # Division of the dataset according to the label examined
            class_data = self.data.loc[self.data.classes == unique_y[i]]
            # Calculation of the number of prototypes for the label examined
            np_class = round(len(class_data) / len(self.data) * self.n_prototypes)
            # Causal choice of label prototypes examined
            for j in range(np_class):
                x = class_data.sample().to_numpy()
                # Adding the initial prototype chosen in the array
                p_init = np.append(p_init, x, axis=0)
        # Initializing the flag to determine the end of the cycle do-while
        flag = True
        # Initialization of epochs
        i = 1
        # Copy of the initial prototype array, so you can update them
        prototypes = np.copy(p_init)
        while flag:
            # error initialization
            e = 0
            for index, x in self.data.iterrows():
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
                    p[0:-1] = np.add(p[0:-1], np.multiply(self.learning_rate, np.subtract(x[0:-1], p[0:-1])))
                else:
                    p[0:-1] = np.subtract(p[0:-1], np.multiply(self.learning_rate, np.subtract(x[0:-1], p[0:-1])))
                    prototypes[dist[0][0]] = p
                    # Error Update
                    e = e + np.linalg.norm(p - p_old)
            # Increase of the epoch
            i = i + 1
            # Update learning_rate
            self.learning_rate = self.learning_rate - (self.learning_rate / self.n_epochs)
            # Checking the cycle exit conditions
            if i > self.n_epochs and e < self.tolerance:
                flag = False
            results = pd.DataFrame(prototypes, columns=['feature1', 'feature2', 'classes'])
        return results

    def create_json(self, prototypes, m_d, M_d):
        point_coordinates = prototypes.iloc[:, :-1].values.tolist()
        # print(point_coordinates)
        point_labels = prototypes.iloc[:, -1].values.tolist()
        # print(point_labels)
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

        with open("file_name.json", 'w') as output:
            json.dump(data, output, indent=1)


