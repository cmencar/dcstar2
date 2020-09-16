import csv

from pandas import DataFrame
import json
import doubleclusteringstar as dcstar
from matplotlib import pyplot as plt
import pandas as pd
from data_compression.compression import compression
from data_compression.fcm2 import fcm2
from data_compression.lvq1 import lvq1
from data_compression.fcm import fcm
import numpy as np

dataset = "wine"
m = 2
n_e = 1000

original_dataset = pd.read_csv('dataset_ndimensionali/wine.csv', header=None)
n_classes = 3
nps = [n_classes, n_classes * 2, n_classes * 4, n_classes * 8]

compression = compression(original_dataset)
used_dataset = compression.normalized_dataset()

folds = []
res = []
res2 = []

used_dataset = used_dataset.sample(frac=1).reset_index(drop=True)
X = np.delete(used_dataset.values, np.s_[-1], axis=1)
y = np.delete(used_dataset.values, np.s_[0:-1], axis=1)

for idx in range(10):
    folds.append([X[idx * int(len(X) / 10): (idx + 1) * int(len(X) / 10)],
                  y[idx * int(len(X) / 10): (idx + 1) * int(len(X) / 10)]])

start_total = pd.Timestamp.now()

for n_p in nps:

    for index in range(0, 10):

        filename = "accuracy_test/FCM/" + str(dataset) + "/" + str(dataset) + "_" + str(n_e) + "_" + str(
            n_p) + "_" + str(index + 1) + "_" + ".json"

        filename2 = "accuracy_test/FCM2/" + str(dataset) + "_FCM2" + "/" + str(dataset) + "_" + str(n_e) + "_" + str(
            n_p) + "_" + str(index + 1) + "_" + ".json"

        newX = []
        for i in range(len(folds)):
            if i != index:
                data, labels = folds[i]
                for x, y in zip(data, labels):
                    newX.append(np.append(x, y))
        refactored = DataFrame(newX)
        lvq1_strategy = lvq1(refactored, n_prototypes=n_p, n_epochs=n_e)
        fcm_strategy = fcm(refactored, n_p=n_p, n_epochs=n_e, m=m)
        fcm2_strategy = fcm2(refactored, n_p=n_p, n_epochs=n_e, m=m)

        compression.set_strategy(fcm_strategy)
        prototypes = compression.do_compression()
        compression.create_json(prototypes, filename)

        compression.set_strategy(fcm2_strategy)
        prototypes2 = compression.do_compression()
        compression.create_json(prototypes2, filename2)

print(pd.Timestamp.now() - start_total)

# Accuracy DC*
for n_p in nps:

    res = []
    res2 = []

    print("\n---- Evaluating ", dataset, ".csv in np=", str(n_p) + ": ----")
    for index in range(0, 10):

        filename = "accuracy_test/FCM/" + str(dataset) + "/" + str(dataset) + "_" + str(n_e) + "_" + str(
            n_p) + "_" + str(index + 1) + "_" + ".json"

        filename2 = "accuracy_test/FCM2/" + str(dataset) + "_FCM2" + "/" + str(dataset) + "_" + str(n_e) + "_" + str(
            n_p) + "_" + str(index + 1) + "_" + ".json"

        print("\n---- Evaluating fold", index + 1, " with FCM1 ", "having", len(folds[index][0]), "elements: ----")

        # loading of prototypes point list and dimensional boundaries
        point_list, m_d, M_d = dcstar.DoubleClusteringStar.load(filename)
        clustering = dcstar.DoubleClusteringStar(prototypes=point_list, m_d=m_d, M_d=M_d, verbose=True)
        clustering.train(save_log=True)
        # clustering.plot_result()

        print("\n---- Evaluating fold", index + 1, " with FCM2 ", "having", len(folds[index][0]), "elements: ----")
        point_list2, m_d2, M_d2 = dcstar.DoubleClusteringStar.load(filename2)
        clustering2 = dcstar.DoubleClusteringStar(prototypes=point_list2, m_d=m_d2, M_d=M_d2, verbose=True)
        clustering2.train(save_log=True)
        # clustering2.plot_result()

        # Accuracy FCM1
        counter = 0
        for element, result in zip(folds[index][0], folds[index][1]):
            min_dist = np.linalg.norm(point_list[0].get_coordinates() - element)
            cl_ = point_list[0].get_label()
            for point in point_list:
                norma = np.linalg.norm(point.get_coordinates() - element)
                if norma < min_dist:
                    min_dist = norma
                    cl_ = point.get_label()

            if result == cl_:
                counter += 1

        # Accuracy FCM2
        counter2 = 0
        for element2, result2 in zip(folds[index][0], folds[index][1]):
            min_dist2 = np.linalg.norm(point_list2[0].get_coordinates() - element2)
            cl_2 = point_list2[0].get_label()
            for point2 in point_list2:
                norma2 = np.linalg.norm(point2.get_coordinates() - element2)
                if norma2 < min_dist2:
                    min_dist2 = norma2
                    cl_2 = point2.get_label()

            if result2 == cl_2:
                counter2 += 1

        print("\n\nFCM Classificator accuracy:", counter / len(folds[index][0]) * 100, "% (", counter, ")")
        res.append(100 - clustering.evaluate_classificator(folds[index][0], folds[index][1]))

        print("\n\nFCM2 Classificator accuracy:", counter2 / len(folds[index][0]) * 100, "% (", counter2, ")")
        res2.append(100 - clustering2.evaluate_classificator(folds[index][0], folds[index][1]))

    print("\n--- DC* with FCM1 Error final percentage:", np.sum(res) / len(res), "---")
    print("--- DC* with FCM1 Standard deviation:", np.std(res), "\n\n")

    print("--- DC* with FCM2 Error final percentage:", np.sum(res2) / len(res2), "---")
    print("--- DC* with FCM2 Standard deviation:", np.std(res2), "\n\n\n")
pass
