from heuristic_search.prototypes_creators import PrototypesCreator
import doubleclusteringstar as dcstar


# loading of prototypes point list and dimensional boundaries
loader = PrototypesCreator()

point_list, m_d, M_d = loader.load("created point lists/banana_100_20.json")

# declaration of DeapGeneticGuideSequenceProblem parameters
gg_args = {"selected_for_tournament": 5,
           "generations": 20,
           "mating_rate": 0.7,
           "selected_best": 10}

clustering = dcstar.DoubleClusteringStar(prototypes=point_list, m_d=m_d, M_d=M_d,
                                         genetic_guide_parameters=gg_args, verbose=True)
clustering.predict_verbose(save_log=True)
clustering.plot_result()

pass