from cut_sequences.cuts_sequence import CutsSequence
from cut_sequences.point import Point
from cut_sequences.selected_cuts_sequence import SelectedCutsSequence
from cut_sequences.dcstar import DCStar
import matplotlib.pyplot as plt
import random as rand

'''
point_list = [
    Point(coordinates = [.18, .09], label="prototype_1", name="point_1"),
    Point(coordinates = [.26, .28], label="prototype_1", name="point_2"),
    Point(coordinates = [.62, .17], label="prototype_1", name="point_3"),
    Point(coordinates = [.71, .74], label="prototype_1", name="point_4"),
    Point(coordinates = [.928, .06], label="prototype_1", name="point_5"),
    Point(coordinates = [.33, .65], label="prototype_1", name="point_6"),
    Point(coordinates = [.326, .78], label="prototype_1", name="point_7"),
    Point(coordinates = [.405, .91], label="prototype_1", name="point_8"),
    Point(coordinates = [.88, .11], label="prototype_1", name="point_9"),
    Point(coordinates = [.14, .16], label="prototype_1", name="point_10"),
    Point(coordinates = [.244, .672], label="prototype_1", name="point_11"),
    Point(coordinates = [.29, .672], label="prototype_1", name="point_12"),
    Point(coordinates = [.08, .45], label="prototype_1", name="point_13"),
    Point(coordinates = [.77, .89], label="prototype_1", name="point_14"),
    Point(coordinates = [.509, .733], label="prototype_1", name="point_15"),
    Point(coordinates = [.33, .802], label="prototype_1", name="point_16"),
]
'''


point_list = [ Point(coordinates=[rand.uniform(0, 1), rand.uniform(0, 1)], label=rand.randrange(1, 6), name=point_id) for point_id in range(12) ]

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


astar = DCStar(point_list)
T_d = astar.get_T_d()

for cut in T_d.get_dimension(0):
    plt.plot([cut, cut], [0, 1], 'k', linestyle='--', color='red')

for cut in T_d.get_dimension(1):
    plt.plot([0, 1], [cut, cut], linestyle='--', color='red')

plt.show()

result, branches_taken = astar.find(in_debug=True)
print("\nFound node in ", branches_taken, " evaluation.")

S_d = SelectedCutsSequence()
S_d.from_binary(T_d, result.get_state())

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
