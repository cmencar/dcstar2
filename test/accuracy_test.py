from pandas import DataFrame
import doubleclusteringstar as dcstar
from matplotlib import pyplot as plt
import pandas as pd
from data_compression.compression import compression
from data_compression.lvq1 import lvq1
from data_compression.fcm import fcm
import numpy as np

col_bidim = ('f1', 'f2', 'species')
col_iris = ('f1', 'f2', 'f3', 'f4', 'species')
col_appendicitis = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'species')
col_newthyroid = ('f1', 'f2', 'f3', 'f4', 'f5', 'species')
col_bupa = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'species')
col_glass = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'species')
col_wisconsin = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'species')
col_pageblocks = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'species')
col_wine = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13', 'species')
col_ionosphere = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13',
                  'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25',
                  'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'species')
col_sonar = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13',
             'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25',
             'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37',
             'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49',
             'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'species')

dataset = "banana"
n_classes = 3
nps = [n_classes, n_classes * 2, n_classes * 4, n_classes * 8]

original_dataset = pd.read_csv('dataset_bidimensionali/banana.csv', names=col_bidim)

compression = compression(original_dataset)
used_dataset = compression.normalized_dataset()

folds = []
res = []

used_dataset = used_dataset.sample(frac=1).reset_index(drop=True)
X = np.delete(used_dataset.values, np.s_[-1], axis=1)
y = np.delete(used_dataset.values, np.s_[0:-1], axis=1)

for idx in range(10):
    folds.append([X[idx * int(len(X) / 10): (idx + 1) * int(len(X) / 10)],
                  y[idx * int(len(X) / 10): (idx + 1) * int(len(X) / 10)]])

'''
for n_p in nps:

    for index in range(0, 10):

        filename = "accuracy_test/banana/" + str(dataset) + "_100_" + str(n_p) + "_" + str(index + 1) + ".json"

        newX = []
        for i in range(len(folds)):
            if i != index:
                data, labels = folds[i]
                for x, y in zip(data, labels):
                    newX.append(np.append(x, y))
        refactored = DataFrame(newX)

        lvq1_strategy = lvq1(refactored, n_p)
        compression.set_strategy(lvq1_strategy)
        prototypes = compression.do_compression()
        lvq1_strategy.create_json(prototypes, filename)
'''


# Accuracy DC*
for n_p in nps:

    res = []

    print("\n---- Evaluating ", dataset, ".csv in np=", str(n_p) + ": ----")
    for index in range(0, 10):

        filename = "accuracy_test/banana/" + str(dataset) + "_100_" + str(n_p) + "_" + str(index + 1) + ".json"

        print("\n---- Evaluating fold", index + 1, "having", len(folds[index][0]), "elements: ----")

        # loading of prototypes point list and dimensional boundaries
        point_list, m_d, M_d = dcstar.DoubleClusteringStar.load(filename)

        clustering = dcstar.DoubleClusteringStar(prototypes=point_list, m_d=m_d, M_d=M_d, verbose=True)
        clustering.train(save_log=True)
        # clustering.plot_result()

        # Accuracy LVQ1
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

        print("\n\nLVQ1* Classificator accuracy:", counter / len(folds[index][0]) * 100, "% (", counter, ")")

        res.append(100 - clustering.evaluate_classificator(folds[index][0], folds[index][1]))

    print("\n--- DC* Error final percentage:", np.sum(res) / len(res), "---")
    print("--- DC* Standard deviation:", np.std(res), "\n\n\n")

pass
