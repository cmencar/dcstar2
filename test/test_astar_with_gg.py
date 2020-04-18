from heuristic_search.prototypes_creators import PrototypesCreator
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
from cut_sequences.point import Point
from heuristic_search.astar import AStar
import matplotlib.pyplot as plt


# loading of prototypes point list and dimensional boundaries
# loader = PrototypesCreator()
# point_list, m_d, M_d = loader.load("created point lists/point_list_1.json")

point_list = [
    Point(coordinates=[.2354, .34], label="prototype_1", name="point_A"),
    Point(coordinates=[.3345, .3421], label="prototype_1", name="point_B"),
    Point(coordinates=[.351, .3453], label="prototype_2", name="point_C"),
    Point(coordinates=[.45235, .00009], label="prototype_1", name="point_D"),
    Point(coordinates=[.9, .5444], label="prototype_1", name="point_E"),
    Point(coordinates=[.999, .4], label="prototype_2", name="point_F"),
    Point(coordinates=[.799, .24], label="prototype_1", name="point_G")
]

# creation of DCStar object for the clustering operation
dcstar = AStar(point_list, m_d=0, M_d=1)

# acquiring cuts sequences created in DCStar object with passed points list
cuts_sequences = dcstar.get_cuts_sequences()

# execution of clustering with DCStar and acquiring of results
result, branches_taken, time = dcstar.find(verbose=True)
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
