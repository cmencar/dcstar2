import numpy as np
import pandas as pd
from fcmeans import FCM

from data_compression.CompressionStrategy import CompressionStrategy


class Fcm(CompressionStrategy):

    def __init__(self, data, n_p=3, n_epochs=100, m=1.7):

        super().__init__(data)
        self.n_c = int(n_p/self.get_n_class_data())
        self.n_epochs = n_epochs
        self.m = m

    def get_data_features(self):
        df_features = self.data.iloc[:, :-1]
        return df_features

    def get_n_class_data(self):
        n_classes = len(self.data.iloc[:, -1].unique())
        return n_classes

    def algorithm(self):
        start = pd.Timestamp.now()
        unique_y = self.data.iloc[:, -1].unique()
        prototypes = []
        for i in range(len(unique_y)):
            class_data = self.data.loc[self.data.iloc[:, -1] == unique_y[i]]
            df_features = class_data.iloc[:, :-1]
            # fit the fuzzy-c-means
            fcm = FCM(n_clusters=self.n_c, max_iter=self.n_epochs, m=self.m)
            fcm.fit(df_features)
            # outputs
            fcm_centers = fcm.centers
            fcm_centers = fcm_centers.to_numpy().tolist()

            for z in range(len(fcm_centers)):
                fcm_centers[z].append(unique_y[i])
                prototypes.append(fcm_centers[z])
        prototypes = np.array(prototypes)
        print("Tempo esecuzione algoritmo")
        print(pd.Timestamp.now() - start)
        return prototypes
