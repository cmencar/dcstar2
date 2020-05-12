from heuristic_search.prototypes_creators import PrototypesCreator
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
import doubleclusteringstar as dcstar


# loading of prototypes point list and dimensional boundaries
loader = PrototypesCreator()

point_list, m_d, M_d = loader.load("created point lists/bandiera_1000_30.json")

# declaration of DeapGeneticGuideSequenceProblem parameters
gg_args = {"selected_for_tournament": 5,
           "generations": 20,
           "mating_rate": 0.7,
           "selected_best": 10}

clustering = dcstar.DoubleClusteringStar(prototypes=point_list, m_d=m_d, M_d=M_d,
                                         genetic_guide_parameters=gg_args, verbose=True)
clustering.predict_verbose(save_log=True)
clustering.plot_result()
'''
clustering.problem.genetic_guide_individual.debug_print()
selected_cuts_sequences = SelectedDimensionalSequenceNumeric()
selected_cuts_sequences.from_binary(clustering.problem.cuts_sequences, clustering.problem.genetic_guide_individual)
hyperboxes_set = selected_cuts_sequences.generate_hyperboxes_set(clustering.problem.points_list, m_d = clustering.problem.boundary_points[0],
                                                                 M_d=clustering.problem.boundary_points[1])
print("puro") if hyperboxes_set.get_impure_hyperboxes_number() == 0 else print("impuro")
'''
pass
