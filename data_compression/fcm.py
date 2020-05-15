import json
import random
import operator
import numpy as np
import pandas as pd
import math

from data_compression.compression_strategy import compression_strategy


class fcm(compression_strategy):

    def __init__(self, data, n_clusters=3, n_epochs=100, m=1.7):

        self.data = data
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
            start = pd.Timestamp.now()
            cluster_centers = self.calculateCenterCluster(m_matrix, n, df_features)
            m_matrix = self.updateMembershipValue(m_matrix, cluster_centers, n, df_features)
            cluster_labels = self.getClusters(m_matrix, n)

            if epoch == 0:
                print("Cluster Centers:")
                print(np.array(cluster_centers))
            # print("Timer epoca n." + str(epoch + 1))
            # print(pd.Timestamp.now() - start)
            epoch += 1
        # print(np.array(m_matrix))
        # print("Final Cluster center:")  # final cluster centers
        cluster_centers = np.array(cluster_centers)
        cluster_labels = np.array(cluster_labels)
        return cluster_labels, cluster_centers
