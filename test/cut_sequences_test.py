from cut_sequences.point import Point
from cut_sequences.cuts_sequence import CutsSequence
from cut_sequences.selected_cuts_sequence import SelectedCutsSequence
from cut_sequences.selected_cuts_sequence_bin import SelectedCutsSequenceBin
from cut_sequences.hyperboxes_set import HyperboxesSet
from cut_sequences import mapping as mp

# example definition T_d
T_d = CutsSequence()
T_d.set_dimension(1, [-1.5, 3.5, 4.1])
T_d.set_dimension(2, [3.5, 8.9])
T_d.set_dimension(3, [1.2])
T_d.set_dimension(4, [-8.9, 9.0, 9.3, 9.5, 9.8])
T_d.set_dimension(5, [-0.1, 6.6])

# example definition S_d_bin
S_d_bin = SelectedCutsSequenceBin([[True, False, False],
                              [False, False],
                              [True],
                              [False, True, True, False, True],
                              [False, True]])

# example definition S_d
S_d = SelectedCutsSequence()
S_d.set_dimension(1, [-1.5, 4.1])
S_d.set_dimension(2, [])
S_d.set_dimension(3, [1.2])
S_d.set_dimension(4, [9.3, 9.8])
S_d.set_dimension(5, [6.6])

# example calculating different cut structures
print("\n----- from_point_to_logical -----\n")
from_point_to_logical = mp.from_point_to_logical(T_d, S_d)
from_point_to_logical.debug_print()
print("\n----- from_logical_to_point -----\n")
from_logical_to_point = mp.from_logical_to_point(T_d, S_d_bin)
from_logical_to_point.debug_print()
print("\n----- empty_t_d_bin -----\n")
empty_t_d_bin = mp.generate_starting_binary_t_d(T_d)
empty_t_d_bin.debug_print()

# creating simple points
point_1 = Point(list([1.4, 7.3, 2.1, 1.3, 3.2]), "prototype_1")
point_2 = Point(list([5.2, 7.2, 4.4, 1.3, 3.2]), "prototype_2")
point_list = list([point_1, point_2])

# calculating hyperboxes given a selected cuts sequence
S_d_1 = SelectedCutsSequence()
S_d_1.set_dimension(1, list([1, 2, 3]))
S_d_1.set_dimension(2, list([1, 2, 3]))
S_d_1.set_dimension(3, list([1, 2, 3]))
point_A = Point(list([0.2354, 1.34, 1.543]), label="prototype_1", name="point_A")
point_B = Point(list([1.3345, 1.3421, 1.36897]), label="prototype_1", name="point_B")
point_C = Point(list([1.85, 1.53453, 2.6423]), label="prototype_2", name="point_C")
point_D = Point(list([1.45235, 2.00009, 2.141]), label="prototype_1", name="point_D")
point_E = Point(list([2, 3.5444, 0.25434]), label="prototype_1", name="point_E")
point_F = Point(list([3.999, 3.4, 1.7714]), label="prototype_2", name="point_F")
point_list_1 = list([point_A, point_B, point_C, point_D, point_E, point_F])
hyperboxes = mp.generate_hyperboxes_from_s_d(S_d_1, point_list_1, 0, 4)
hb = hyperboxes.get_hyperbox_by_point(point_A)

# calculating impure hyperboxes
S_d_2 = SelectedCutsSequence()
S_d_2.set_dimension(2, list([1, 2]))
S_d_2.set_dimension(1, list([1, 2]))
point_a = Point(list([0.5, 0.5]), label="prototipo_a", name="point_a")
point_b = Point(list([0.6, 0.4]), label="prototipo_b", name="point_b")
point_c = Point(list([1.2, 1.7]), label="prototipo_a", name="point_c")
point_d = Point(list([1.3, 1.1]), label="prototipo_a", name="point_d")
point_e = Point(list([2.05, 2.4]), label="prototipo_b", name="point_e")
point_f = Point(list([2.89, 2.1]), label="prototipo_a", name="point_f")
point_list_2 = list([point_a, point_b, point_c, point_d, point_e, point_f])
hyperboxes_2 = mp.generate_hyperboxes_from_s_d(S_d_2, point_list_2, 0, 4)
impures = hyperboxes_2.get_impure_hyperboxes()
impures_num = hyperboxes_2.get_impure_hyperboxes_number()
hyperbox = hyperboxes_2.get_hyperbox_by_point(point_c)
print("\n--- END OF TEST ---\n")
