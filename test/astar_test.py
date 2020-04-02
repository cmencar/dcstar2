from cut_sequences.dimensional_sequence_numeric import DimensionalSequenceNumeric
from cut_sequences.point import Point
from cut_sequences.prototypes_creator import PrototypesCreator, PrototypesLoader
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
from cut_sequences.dcstar import DCStar
import matplotlib.pyplot as plt


#creator = PrototypesCreator()
#creator.create("created point lists/point_list_1.json", n_points=20, n_classes=3, n_dimensions=3, m_d=0, M_d=1)
loader = PrototypesLoader()
point_list, m_d, M_d = loader.load("created point lists/point_list_1.json")

astar = DCStar(point_list, m_d = m_d, M_d = M_d)
T_d = astar.get_T_d()

result, branches_taken = astar.find(in_debug=True)
print("\nFound node in ", branches_taken, " evaluation.")

S_d = SelectedDimensionalSequenceNumeric()
S_d.from_binary(T_d, result)
hyperboxes_set = S_d.generate_hyperboxes_set(point_list, m_d=m_d, M_d=M_d)
hyperboxes = hyperboxes_set.get_hyperboxes()

for cut in T_d.get_dimension(0):
    plt.plot([cut, cut], [0, 1], 'k', linestyle=':', color='grey')

for cut in T_d.get_dimension(1):
    plt.plot([0, 1], [cut, cut], linestyle=':', color='grey')

for cut in S_d.get_dimension(0):
    plt.plot([cut, cut], [0, 1], 'k', linestyle='--', color='black')

for cut in S_d.get_dimension(1):
    plt.plot([0, 1], [cut, cut], linestyle='--', color='black')

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

plt.show()

pass
