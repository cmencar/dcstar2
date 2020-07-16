import json
import random
import operator
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from seaborn import scatterplot as scatter

from data_compression.compression_strategy import compression_strategy


class fcm(compression_strategy):

    def __init__(self, data, n_clusters=3, n_epochs=100, m=1.7):

        super().__init__(data)
        self.n_c = n_clusters
        self.n_epochs = n_epochs
        self.m = m

    def get_data_features(self):
        df_features = self.data.iloc[:, :-1]
        return df_features

    # inizializing the membership matrix
    def initializedMembership(self, n):
        m_matrix = []
        for i in range(n):
            random_num_list = [random.random() for i in range(self.n_c)]
            summation = sum(random_num_list)
            temp_list = [x / summation for x in random_num_list]

            flag = temp_list.index(max(temp_list))
            for j in range(0, len(temp_list)):
                if j == flag:
                    temp_list[j] = 1
                else:
                    temp_list[j] = 0

            m_matrix.append(temp_list)
        return m_matrix

    def calculateCenterCluster(self, m_matrix, n, df_features):
        cluster_mem_val = list(zip(*m_matrix))
        cluster_centers = []
        for j in range(self.n_c):
            x = list(cluster_mem_val[j])
            xraised = [p ** self.m for p in x]
            denominator = sum(xraised)
            temp_num = []
            for i in range(n):
                data_point = list(df_features.iloc[i])
                prod = [xraised[i] * val for val in data_point]
                temp_num.append(prod)
            numerator = map(sum, list(zip(*temp_num)))
            center = [z / denominator for z in numerator]
            cluster_centers.append(center)
        return cluster_centers

    def updateMembershipValue(self, m_matrix, c_centers, n, df_features):
        p = float(2 / (self.m-1))
        for i in range(n):
            x = list(df_features.iloc[i])
            distances = [np.linalg.norm(np.array(list(map(operator.sub, x, c_centers[j])))) for j in range(self.n_c)]
            for j in range(self.n_c):
                den = sum([math.pow(float(distances[j] / distances[c]), p) for c in range(self.n_c)])
                m_matrix[i][j] = float(1 / den)
        return m_matrix

    def getClusters(self, m_matrix, n):
        cluster_labels = list()
        for i in range(n):
            max_val, idx = max((val, idx) for (idx, val) in enumerate(m_matrix[i]))
            cluster_labels.append(idx)
        return cluster_labels

    def algorithm(self):
        df_features = self.get_data_features()
        n = len(df_features)
        m_matrix = self.initializedMembership(n)
        cluster_centers = []
        cluster_labels = []
        epoch = 0
        while epoch < self.n_epochs:
            cluster_centers = self.calculateCenterCluster(m_matrix, n, df_features)
            m_matrix = self.updateMembershipValue(m_matrix, cluster_centers, n, df_features)
            cluster_labels = self.getClusters(m_matrix, n)

            if epoch == 0:
                print("Cluster Centers:")
                print(np.array(cluster_centers))
            epoch += 1

        # print(np.array(m_matrix))
        # print("Final Cluster center:")  # final cluster centers
        cluster_centers = np.array(cluster_centers)
        cluster_labels = np.array(cluster_labels)
        return cluster_labels, cluster_centers

    def draw_clusters(self, cluster_label, cluster_center):
        X = self.data.iloc[:, :-1].to_numpy()
        f, axs = plt.subplots(1, 2, figsize=(11, 5))
        scatter(X[:, 0], X[:, 1], ax=axs[0])
        scatter(X[:, 0], X[:, 1], ax=axs[1], hue=cluster_label)
        scatter(cluster_center[:, 0], cluster_center[:, 1], ax=axs[1], marker=">", s=200)
        plt.show()

    def create_json(self, cluster_center, cluster_labels, filename):
        point_coordinates = cluster_center.tolist()
        point_labels = list(set(cluster_labels))
        m_d = self.get_min_boundary(cluster_center).tolist()
        M_d = self.get_max_boundary(cluster_center).tolist()
        point_id = list()
        for i in point_coordinates:
            point_id.append(point_coordinates.index(i))

        data = {'points': [], 'm_d': m_d, 'M_d': M_d}
        for i in range(len(point_coordinates)):
            coordinates = point_coordinates[i]
            data['points'].append({
                'coordinates': coordinates,
                'class': int(point_labels[i]),
                'name': "cluster_center" + " " + str(point_id[i] + 1)
            })

        with open(filename, 'w') as output:
            json.dump(data, output, indent=1)

    def get_min_boundary(self, prototypes):
        minValues = np.amin(prototypes, axis=0)
        return minValues

    def get_max_boundary(self, prototypes):
        maxValues = np.amax(prototypes, axis=0)
        return maxValues