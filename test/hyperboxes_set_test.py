from cut_sequences.point import Point
from cut_sequences.dimensional_sequence_numeric import DimensionalSequenceNumeric
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric

# definition prototype points
point_list = [
    Point(coordinates = [.14, .34, .343], label="prototype_1", name="point_A"),
    Point(coordinates = [.24, .3421, .36897], label="prototype_1", name="point_B"),
    Point(coordinates = [.351, .3453, .6423], label="prototype_2", name="point_C"),
    Point(coordinates = [.59, .00009, .141], label="prototype_1", name="point_D"),
    Point(coordinates = [.9, .5444, .25434], label="prototype_1", name="point_E"),
    Point(coordinates = [.17, .4, .42], label="prototype_2", name="point_F"),
    Point(coordinates = [.799, .24, .1114], label="prototype_1", name="point_G")
]

# definition of al list of list containing numerical cuts values
cuts_list = [[.12, .33, .56, .711, .83], [.41, .46, .65], [.18, .52, .88]]
m_d = [0, 0, 0]
M_d = [1, 1, 1]

# creation of a DimensionalSequenceNumeric containing T_ds cuts sequences
cuts_sequence = DimensionalSequenceNumeric(cuts_list)

# creation of a successor, simulating the iterated creation of successor list
# defining only the final successor with service operator set_cut()
simulated_successor_binary = cuts_sequence.generate_starting_binary()
simulated_successor_binary.set_cut(0, 1, True)
simulated_successor_binary.set_cut(0, 3, True)
simulated_successor_binary.set_cut(1, 0, True)
simulated_successor_binary.set_cut(2, 0, True)
simulated_successor_binary.set_cut(2, 1, True)
simulated_successor_binary.set_cut(2, 2, True)
simulated_successor = SelectedDimensionalSequenceNumeric()
simulated_successor.from_binary(cuts_sequence, simulated_successor_binary)

# definition of the HyperboxesSet object
hyperboxes_set = simulated_successor.generate_hyperboxes_set(point_list, m_d, M_d)

pass