from heuristic_search.prototypes_creators import PrototypesLoader
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
from heuristic_search.dcstar import DCStar
import matplotlib.pyplot as plt


# loading of prototypes point list and dimensional boundaries
loader = PrototypesLoader()
point_list, m_d, M_d = loader.load("created point lists/point_list_1.json")

# creation of DCStar object for the clustering operation
dcstar = DCStar(point_list, m_d = m_d, M_d = M_d)

# acquiring T_d created in DCStar object with passed points list
T_d = dcstar.get_T_d()

# execution of clustering with DCStar and acquiring of results
result, branches_taken, time = dcstar.find(verbose = True)
print("\nFound node in", branches_taken, "evaluation in", time, "sec.")

# creation of an S_d cuts sequence with found cuts sequence
S_d = SelectedDimensionalSequenceNumeric()
S_d.from_binary(T_d, result)

# if created T_d in in a bidimensional space then show
# a plot with grafical view of found S_d cuts sequence
if T_d.get_dimensions_number() == 2:

    # printing T_d cuts in the plot
    for cut in T_d.get_dimension(0):
        plt.plot([cut, cut], [0, 1], 'k', linestyle=':', color='grey')
    for cut in T_d.get_dimension(1):
        plt.plot([0, 1], [cut, cut], linestyle=':', color='grey')

    # printing S_d cuts in the plot
    for cut in S_d.get_dimension(0):
        plt.plot([cut, cut], [0, 1], 'k', linestyle='--', color='black')
    for cut in S_d.get_dimension(1):
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
