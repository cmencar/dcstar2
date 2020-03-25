from cut_sequences.point import Point
from cut_sequences.cuts_sequence import CutsSequence
from cut_sequences.selected_cuts_sequence import SelectedCutsSequence

# example definition prototype points
point_A = Point(list([.2354, .34, .543]), label="prototype_1", name="point_A")
point_B = Point(list([.3345, .3421, .36897]), label="prototype_1", name="point_B")
point_C = Point(list([.351, .3453, .6423]), label="prototype_2", name="point_C")
point_D = Point(list([.45235, .00009, .141]), label="prototype_1", name="point_D")
point_E = Point(list([.9, .5444, .25434]), label="prototype_1", name="point_E")
point_F = Point(list([.999, .4, .7714]), label="prototype_2", name="point_F")
point_G = Point(list([.799, .24, .1114]), label="prototype_1", name="point_G")
point_list = list([point_A, point_B, point_C, point_D, point_E, point_F, point_G])

# example definition T_d
print("\n----- T_d -----\n")
T_d = CutsSequence([[.2, .36, .56, .63, .87, .88, .94], [.11, .32, .34, .36, .712, .998], [.02, .47, 0.7111, .89]])
T_d.debug_print()

# example definition S_d_bin as T_d_bin
print("\n----- T_d_bin -----\n")
S_d_bin = T_d.generate_starting_binary()
S_d_bin.debug_print()

# example define 'casually' S_d_bin
print("\n----- S_d_bin -----\n")
print("N.B.: DEFINED HARDCODED \n")
S_d_bin.set_cut(0, 0, True)
S_d_bin.set_cut(0, 1, True)
S_d_bin.set_cut(0, 4, True)
S_d_bin.set_cut(0, 5, True)
S_d_bin.set_cut(0, 6, True)
S_d_bin.set_cut(1, 0, True)
S_d_bin.set_cut(1, 1, True)
S_d_bin.set_cut(1, 2, True)
S_d_bin.set_cut(1, 4, True)
S_d_bin.set_cut(2, 0, True)
S_d_bin.set_cut(2, 3, True)
S_d_bin.debug_print()

# example calculating S_d
print("\n----- S_d -----\n")
S_d = SelectedCutsSequence()
S_d.from_binary(T_d, S_d_bin)
S_d.debug_print()

# calculating hyperboxes given a selected cuts sequence
hyperboxes_set = S_d.generate_hyperboxes_set(point_list, m_d = 0, M_d = 1)
evaluated_point = point_B
hyperboxes = hyperboxes_set.get_hyperbox_by_point(evaluated_point)
print("\n\nHyperbox of point '", evaluated_point.get_name(), "'. Is impure: ", hyperboxes.is_impure())
