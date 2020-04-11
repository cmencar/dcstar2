from heuristic_search.prototypes_creators import PrototypesCreator
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
from heuristic_search.dcstar import DCStar
import matplotlib.pyplot as plt


# loading of prototypes point list and dimensional boundaries
loader = PrototypesCreator()
point_list, m_d, M_d = loader.load("created point lists/point_list_1.json")

# creation of DCStar object for the clustering operation
dcstar = DCStar(point_list, m_d = m_d, M_d = M_d)

# acquiring cuts sequences created in DCStar object with passed points list
cuts_sequences = dcstar.get_cuts_sequences()

# execution of clustering with DCStar and acquiring of results
result, branches_taken, time = dcstar.find(verbose = True)
print("\nFound node in", branches_taken, "evaluation in", time, "sec.")

# creation of an selected cuts sequence with found cuts sequence
selected_cuts_sequences = SelectedDimensionalSequenceNumeric()
selected_cuts_sequences.from_binary(cuts_sequences, result)

# if created cuts sequences is in a bidimensional space then show
# a plot with grafical view of found selected cuts sequence
if cuts_sequences.get_dimensions_number() == 2:

    # printing S_d with d=1 in the plot
    for cut in cuts_sequences.get_dimension(0):
        plt.plot([cut, cut], [0, 1], 'k', linestyle=':', color='grey')
    for cut in cuts_sequences.get_dimension(1):
        plt.plot([0, 1], [cut, cut], linestyle=':', color='grey')

    # printing S_d with d=2 in the plot
    for cut in selected_cuts_sequences.get_dimension(0):
        plt.plot([cut, cut], [0, 1], 'k', linestyle='--', color='black')
    for cut in selected_cuts_sequences.get_dimension(1):
        plt.plot([0, 1], [cut, cut], linestyle='--', color='black')

    # printing points in the plot
    for point in point_list:
        color = 'ko'
        if point.get_label() == 1:
            color = 'ro'
        elif point.get_label() == 2:
            color = 'bo'
        elif point.get_label() == 3:
            color = 'ko'
        elif point.get_label() == 4:
            color = 'yo'
        elif point.get_label() == 5:
            color = 'mo'
        plt.plot(point.get_coordinate(0), point.get_coordinate(1), color)

    # showing the plot to video
    plt.show()

pass
