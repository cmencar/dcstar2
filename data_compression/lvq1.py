import numpy as np
import pandas as pd
from data_compression.compression_strategy import compression_strategy
import matplotlib.pyplot as plt
import json


class lvq1(compression_strategy):

    def __init__(self, data, n_prototypes, n_epochs=1000, learning_rate=0.0001, tolerance=8):

        super().__init__(data)
        self.n_prototypes = n_prototypes
        self.n_epochs = n_epochs
        self.learning_rate = learning_rate
        self.tolerance = tolerance

    # Method for creation of prototypes
    # input: normalized_dataSet, n_prototypes, unique_labels
    # output: prototypes
    def algorithm(self):
        # calculation number of features
        n_dimension = self.data.shape[1]
        unique_y = self.get_unique_labels()
        # I initialize the empty array where I will put the chosen prototypes
        p_init = np.empty((0, n_dimension))
        # Initialize prototypes using random choice.
        for i in range(len(unique_y)):
            # Division of the dataset according to the label examined
            class_data = self.data.loc[self.data.iloc[:, -1] == unique_y[i]]
            # Calculation of the number of prototypes for the label examined
            np_class = int(np.ceil(len(class_data) / len(self.data) * self.n_prototypes))
            # Causal choice of label prototypes examined
            for j in range(np_class):
                x = class_data.sample().to_numpy()
                # Adding the initial prototype chosen in the array
                p_init = np.append(p_init, x, axis=0)

        # Initialization of epochs and error
        i = 0
        e = 0
        # Copy of the initial prototype array, so you can update them
        prototypes = np.copy(p_init)
        while i < self.n_epochs and e < self.tolerance:
            start = pd.Timestamp.now()
            for row in self.data.itertuples():
                # initialization of the list of distances
                dist = list()
                for j in range(len(prototypes)):
                    # Euclidean distance between the initial prototype and the element of the examined
                    # normalized_dataset
                    distance = np.linalg.norm(prototypes[j][0:-1] - row[1:-1])
                    # Adding the calculated distance to the distance list
                    dist.append((j, distance))
                # Descending order of the distance list
                dist.sort(key=lambda z: z[1])
                # Assignment to variable p of the first element of the ordered distance list (shorter distance)
                p = prototypes[dist[0][0]]
                # Copy of the prototype with shorter distance
                p_old = np.copy(p)
                if row[-1] == p[-1]:
                    p[0:-1] = np.add(p[0:-1], np.multiply(self.learning_rate, np.subtract(row[1:-1], p[0:-1])))
                else:
                    p[0:-1] = np.subtract(p[0:-1], np.multiply(self.learning_rate, np.subtract(row[1:-1], p[0:-1])))
                prototypes[dist[0][0]] = p
                # Error Update
                e = e + np.linalg.norm(p[0:-1] - p_old[0:-1])
            print("Timer epoca n." + str(i + 1))
            print(pd.Timestamp.now() - start)
            # Increase of the epoch
            i = i + 1
            # Update learning_rate
            self.learning_rate = self.learning_rate - (self.learning_rate / self.n_epochs)
        return prototypes

    def get_unique_labels(self):
        return self.data.iloc[:, -1].unique()

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

    def create_json(self, prototypes, filename):
        point_coordinates = prototypes[:, :-1].tolist()
        point_labels = prototypes[:, -1].tolist()
        m_d = self.get_min_boundary(prototypes).tolist()
        M_d = self.get_max_boundary(prototypes).tolist()
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

    def get_min_boundary(self, prototypes):
        extendend_data = np.vstack((prototypes, self.data))
        minValues = np.amin(extendend_data[:, 0:-1], axis=0)
        return minValues

    def get_max_boundary(self, prototypes):
        extendend_data = np.vstack((prototypes, self.data))
        maxValues = np.amax(extendend_data[:, 0:-1], axis=0)
        return maxValues
