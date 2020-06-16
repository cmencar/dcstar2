from cut_sequences.point import Point
from heuristic_search.prototypes_creators import PrototypesCreator
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
import doubleclusteringstar as dcstar
import pandas as pd
from data_compression.compression import compression
from data_compression.lvq1 import lvq1
import numpy as np
from sklearn.model_selection import train_test_split

col_bidim = ('f1', 'f2', 'species')
col_iris = ('f1', 'f2', 'f3', 'f4', 'species')
col_glass = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'species')
col_wisconsin = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'species')
col_wine = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13', 'species')
original_dataset = pd.read_csv('dataset_ndimensionali/cancer.csv', names=col_wisconsin)
n_p = 32

compression = compression(original_dataset)
norm = compression.normalized_dataset()
used_dataset = norm
'''
lvq1 = lvq1(used_dataset, n_p)
compression.set_strategy(lvq1)
prototypes = compression.do_compression()
m_d, M_d = lvq1.get_boundary(prototypes)
'''

filename = "RISULTATI TEST ACCURACY/wisconsin_100_32.json"
#filename = "created point lists/wisconsin_100_4.json"
#lvq1.create_json(m_d, M_d, prototypes, filename)

# loading of prototypes point list and dimensional boundaries
loader = PrototypesCreator()

point_list, m_d, M_d = loader.load(filename)

gg_args_test = {"selected_for_tournament": 5,
                "generations": 20,
                "mating_rate": 0.7}

clustering = dcstar.DoubleClusteringStar(prototypes=point_list, m_d=m_d, M_d=M_d, genetic_guide_parameters=gg_args_test,
                                         verbose=True)
clustering.train(save_log=False)
clustering.plot_result()

used_dataset = used_dataset.sample(frac=1).reset_index(drop=True)
X = np.delete(used_dataset.values, np.s_[-1], axis=1)
y = np.delete(used_dataset.values, np.s_[0:-1], axis=1)

# Accuracy LVQ1
counter = 0
for element, result in zip(X, y):
    min_dist = np.linalg.norm(point_list[0].get_coordinates() - element)
    cl_ = point_list[0].get_label()
    for point in point_list:
        norma = np.linalg.norm(point.get_coordinates() - element)
        if norma < min_dist:
            min_dist = norma
            cl_ = point.get_label()

    #    cl = self.predict(element)
    if result == cl_:
        counter += 1

print("\n\nLVQ1* Classificator accuracy:", counter/len(X) * 100, "% (", counter, ")")


# Accuracy DC*
folds = []
res = []

for index in range(10):
    folds.append([X[index * int(len(X)/10): (index+1) * int(len(X)/10)], y[index * int(len(X)/10): (index+1) * int(len(X)/10)]])

for index in range(len(folds)):
    print("\nEvaluating fold", index+1, "having", len(folds[index][0]), "elements:")
    res.append(100 - clustering.evaluate_classificator(folds[index][0], folds[index][1]))

print("\n--- Error final percentage:", np.sum(res)/len(res), "---")

pass
