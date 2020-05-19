from heuristic_search.prototypes_creators import PrototypesCreator
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
import doubleclusteringstar as dcstar


# loading of prototypes point list and dimensional boundaries
loader = PrototypesCreator()

point_list, m_d, M_d = loader.load("created point lists/chessboard_k5.json")

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
                                         genetic_guide_parameters=gg_args_test_05, verbose=True)
clustering.predict(save_log=True)
clustering.plot_result()

pass
