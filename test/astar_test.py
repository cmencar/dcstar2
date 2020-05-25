from cut_sequences.point import Point
from heuristic_search.prototypes_creators import PrototypesCreator
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
import doubleclusteringstar as dcstar
import pandas as pd
from data_compression.compression import compression
from data_compression.lvq1 import lvq1

col_iris = ('f1', 'f2', 'species')
original_dataset = pd.read_csv('dataset_ndimensionali/ionosphere.csv', names=col_iris)
n_p = 21

compression = compression(original_dataset)
norm = compression.normalized_dataset()
lvq1 = lvq1(norm, n_p)
compression.set_strategy(lvq1)
prototypes = compression.do_compression()
m_d, M_d = lvq1.get_boundary(prototypes)
filename = "created point lists/iris_100_21.json"
lvq1.create_json(m_d, M_d, prototypes, filename)

# loading of prototypes point list and dimensional boundaries
loader = PrototypesCreator()

point_list, m_d, M_d = loader.load(filename)

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

clustering = dcstar.DoubleClusteringStar(prototypes=point_list, m_d=m_d, M_d=M_d,
                                         genetic_guide_parameters=None, verbose=True)
clustering.predict(save_log=False)
clustering.plot_result()

pass
