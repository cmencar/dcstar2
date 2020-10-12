from cut_sequences.point import Point
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
import doubleclusteringstar as dcstar
import pandas as pd
from data_compression.Compression import Compression
from data_compression.Lvq1 import Lvq1
import numpy as np
from sklearn.model_selection import train_test_split

col_bidim = ('f1', 'f2', 'species')
col_iris = ('f1', 'f2', 'f3', 'f4', 'species')
col_glass = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'species')
col_wine = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13', 'species')
original_dataset = pd.read_csv('dataset_ndimensionali/iris.csv', names=col_iris)
n_p = 4 #24 #48 #42

'''
compression = compression(original_dataset)
norm = compression.normalized_dataset()
lvq1 = lvq1(norm, n_p)
#lvq1 = lvq1(original_dataset, n_p)
compression.set_strategy(lvq1)
prototypes = compression.do_compression()
m_d, M_d = lvq1.get_boundary(prototypes)
filename = "created point lists/iris_100_48______.json"
lvq1.create_json(m_d, M_d, prototypes, filename)

# loading of prototypes point list and dimensional boundaries
loader = PrototypesCreator()

point_list, m_d, M_d = loader.load(filename)
#point_list, m_d, M_d = loader.load("created point lists/glass_100_18.json")

# declaration of DeapGeneticGuideSequenceProblem parameters
gg_args_test_01 = {"selected_for_tournament": 5,
                   "generations": 20,
                   "mating_rate": 0.7,
                   "selected_best": 10}

gg_args_test_02 = {"selected_for_tournament": 2,
                   "generations": 15,
                   "mating_rate": 0.7,
                   "selected_best": 10}

gg_args_test_03 = {"selected_for_tournament": 5,
                   "generations": 30,
                   "mating_rate": 0.5,
                   "selected_best": 10}

gg_args_test_04 = {"selected_for_tournament": 5,
                   "generations": 50,
                   "mating_rate": 0.7,
                   "selected_best": 5}

gg_args_test_05 = {"selected_for_tournament": 5,
                   "generations": 50,
                   "mating_rate": 0.2,
                   "selected_best": 10}
'''

compression = Compression(original_dataset)
norm = compression.normalized_dataset()
used_dataset = norm
'''
lvq1 = lvq1(used_dataset, n_p)
#lvq1 = lvq1(norm, n_p)
#lvq1 = lvq1(original_dataset, n_p)
compression.set_strategy(lvq1)
prototypes = compression.do_compression()
m_d, M_d = lvq1.get_boundary(prototypes)
'''
filename = "created point lists/wine_100_42.json"
#lvq1.create_json(m_d, M_d, prototypes, filename)

# loading of prototypes point list and dimensional boundaries
point_list, m_d, M_d = dcstar.DoubleClusteringStar.load(filename)

for _ in range(10):

    X = np.delete(used_dataset.values, np.s_[-1], axis=1)
    y = np.delete(used_dataset.values, np.s_[0:-1], axis=1)
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.1)

    dat = pd.DataFrame(norm, index=range(0, len(norm.values)))
    to_drop = []
    for index in range(len(used_dataset.values)):
        for element in test_X:
            if np.all(used_dataset.values[index][0:-1] == element):
                to_drop.append(index)

    for idx in to_drop:
        dat = dat.drop(index=idx)

    counter = 0
    for element, result in zip(test_X, test_y):
        #class_ = dataset.species[index]
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

    print("\n\nLVQ1* Classificator accuracy:", counter/len(test_X) * 100, "% (", counter, ")")


    clustering = dcstar.DoubleClusteringStar(prototypes=point_list, m_d=m_d, M_d=M_d,
                                             genetic_guide_parameters=None, verbose=True)
    clustering.train(save_log=True)
    clustering.plot_result()

    clustering.evaluate_classificator(test_X, test_y)
    #clustering.evaluate_classificator(original_dataset)



pass
