from heuristic_search.prototypes_creators import PrototypesCreator
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
import matplotlib.pyplot as plt
from heuristic_search.astar import astar
from heuristic_search.dcstar_problem import DCStarProblem


# loading of prototypes point list and dimensional boundaries
loader = PrototypesCreator()
point_list, m_d, M_d = loader.load("created point lists/chessboard_k5.json")


# creation of DCStarProblem object for the clustering operation
problem = DCStarProblem(point_list, m_d = m_d, M_d = M_d, verbose = True, use_genetic_guide = False)

# acquiring cuts sequences created in DCStar object with passed points list
cuts_sequences = problem.get_cuts_sequences()

# execution of clustering with DCStar and acquiring of results
result, branches_taken, time = astar(problem)
print("\nFound node in", branches_taken, "evaluation in", time, "sec.")

# creation of an selected cuts sequence with found cuts sequence
selected_cuts_sequences = SelectedDimensionalSequenceNumeric()
selected_cuts_sequences.from_binary(cuts_sequences, result)

# if created cuts sequences is in a bidimensional space then show a plot with grafical view of found selected cuts
# sequence
if cuts_sequences.get_dimensions_number() == 2:

    # printing S_d with d=1 in the plot
    for cut in cuts_sequences.get_dimension(0):
        plt.plot([cut, cut], [m_d, M_d], 'k', linestyle=':', color='grey')
    for cut in cuts_sequences.get_dimension(1):
        plt.plot([m_d, M_d], [cut, cut], linestyle=':', color='grey')

    # printing S_d with d=2 in the plot
    for cut in selected_cuts_sequences.get_dimension(0):
        plt.plot([cut, cut], [m_d, M_d], 'k', linestyle='--', color='black')
    for cut in selected_cuts_sequences.get_dimension(1):
        plt.plot([m_d, M_d], [cut, cut], linestyle='--', color='black')

    # printing points in the plot
    for point in point_list:
        color = 'ko'
        if point.get_label() == 1:
            color = 'rs'
        elif point.get_label() == 2:
            color = 'b*'
        elif point.get_label() == 3:
            color = 'ko'
        elif point.get_label() == 4:
            color = 'y.'
        elif point.get_label() == 5:
            color = 'mo'
        plt.plot(point.get_coordinate(0), point.get_coordinate(1), color)

    # showing the plot to video
    plt.show()

pass
