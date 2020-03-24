from cut_sequences.point import Point
from cut_sequences.cuts_sequence import CutsSequence
from cut_sequences.selected_cuts_sequence import SelectedCutsSequence
from cut_sequences.selected_cuts_sequence_bin import SelectedCutsSequenceBin
from cut_sequences import mapping as mp

# example definition T_d
T_d = CutsSequence([[-1.5, 3.5, 4.1], [3.5, 8.9], [1.2], [-8.9, 9.0, 9.3, 9.5, 9.8], [-0.1, 6.6]])

# example definition S_d
S_d = SelectedCutsSequence([[-1.5, 4.1], [], [1.2], [9.3, 9.8], [6.6]])

# example definition S_d_bin
S_d_bin = S_d.get_binary(T_d)

# example calculating different cut structures
print("\n----- from_point_to_logical -----\n")
#from_point_to_logical = mp.from_point_to_logical(T_d, S_d)
#from_point_to_logical.debug_print()
print("\n----- from_logical_to_point -----\n")
S_d_from_binary = SelectedCutsSequence()
S_d_from_binary.from_binary(T_d, S_d_bin)
S_d_from_binary.debug_print()
print("\n----- empty_t_d_bin -----\n")
empty_t_d_bin = T_d.generate_starting_binary()
empty_t_d_bin.debug_print()

# initializing S_d and subset of prototypes into S_d
S_d_for_hb_eval = SelectedCutsSequence([[.2, .36, .87, .88, .94], [.11, .32, .34, .712], [.02, .89]])
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
hyperboxes = S_d_for_hb_eval.generate_hyperboxes_set(points_set, m_d=0, M_d=1)
hb = hyperboxes.get_hyperbox_by_point(eval_point)
print("\n\nHyperbox of point '", eval_point.get_name(), "'. impure: ", hb.is_impure())




