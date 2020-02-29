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
point_A = Point(list([2.1, 1.4, 1.3]), label="prototype_1", name="point_A")
point_B = Point(list([1.3, 1.3, 1.3]), label="prototype_1", name="point_B")
point_C = Point(list([1.85, 1.5, 2.6]), label="prototype_2", name="point_C")
point_D = Point(list([1.45, 1.9, -2.1]), label="prototype_1", name="point_D")
point_E = Point(list([-2, 3.4, -0.4]), label="prototype_1", name="point_E")
point_F = Point(list([5.2, 4.4, 17.14]), label="prototype_2", name="point_F")
point_list_1 = list([point_A, point_B, point_C, point_D, point_E, point_F])
hyperboxes = mp.generate_hyperboxes_from_s_d(S_d_1, point_list_1)
hb = hyperboxes.get_hyperbox_by_point(point_A)

print("\n--- END OF TEST ---\n")
