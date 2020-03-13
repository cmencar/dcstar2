from cut_sequences.point import Point
from cut_sequences.cuts_sequence import CutsSequence
from cut_sequences.selected_cuts_sequence import SelectedCutsSequence
from cut_sequences.selected_cuts_sequence_bin import SelectedCutsSequenceBin
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

# initializing S_d and subset of prototypes into S_d
S_d_for_hb_eval = SelectedCutsSequence()
S_d_for_hb_eval.set_dimension(1, list([.2, .36, .87, .88, .94]))
S_d_for_hb_eval.set_dimension(2, list([.11, .32, .34, .712]))
S_d_for_hb_eval.set_dimension(3, list([.02, .89]))
point_A = Point(list([.2354, .34, .543]), label="prototype_1", name="point_A")
point_B = Point(list([.3345, .3421, .36897]), label="prototype_1", name="point_B")
point_C = Point(list([.351, .3453, .6423]), label="prototype_2", name="point_C")
point_D = Point(list([.45235, .00009, .141]), label="prototype_1", name="point_D")
point_E = Point(list([.9, .5444, .25434]), label="prototype_1", name="point_E")
point_F = Point(list([.999, .4, .7714]), label="prototype_2", name="point_F")
point_G = Point(list([.799, .24, .1114]), label="prototype_1", name="point_G")
points_set = list([point_A, point_B, point_C, point_D, point_E, point_F, point_G])

# calculating hyperboxes given a selected cuts sequence
eval_point = point_B
hyperboxes = mp.generate_hyperboxes_set_from_s_d(S_d_for_hb_eval, points_set, m_d=0, M_d=1)
hb = hyperboxes.get_hyperbox_by_point(eval_point)
print("\n\nHyperbox of point '", eval_point.get_name(), "'. impure: ", hb.is_impure())




