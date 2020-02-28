import Point as pt
import T_d as cuts
import S_d as selected_cuts
import T_d_bin as binary_cuts
import Mapping as mp

# example definition T_d
T_d = cuts.CutsSequence()
T_d.set_dimension(1, [1.2, 3.5, 4.1])
T_d.set_dimension(2, [3.5, 8.9])
T_d.set_dimension(3, [1.2])
T_d.set_dimension(4, [8.9, 9.0, 9.3, 9.5, 9.8])
T_d.set_dimension(5, [0.1, 6.6])

# example definition S_d_bin
S_d_bin = binary_cuts.BinaryCuts([[True, False, False],
                                  [False, False],
                                  [True],
                                  [False, True, True, False, True],
                                  [False, True]])

# example definition S_d
S_d = selected_cuts.SelectedCuts()
S_d.set_dimension(1, [1.2, 4.1])
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

point_1 = pt.Point(list([1.4, 7.3, 2.1]), "prototype_1")
point_2 = pt.Point(list([5.2, 7.2, 4.4]), "prototype_2")

mp.S_d_to_hyperboxes(T_d)
