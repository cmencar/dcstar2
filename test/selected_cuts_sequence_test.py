from cut_sequences.dimensional_sequence_numeric import DimensionalSequenceNumeric
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric

# definition of al list of list containing numerical cuts values
cuts_list = [[.12, .33, .56, .711, .83], [.41, .46, .65], [.18, .52, .88]]

# creation of a DimensionalSequenceNumeric containing T_ds cuts sequences
cuts_sequence = DimensionalSequenceNumeric(cuts_list)

# creation of an initial selected cuts sequence binary
initial_binary_cuts_sequence = cuts_sequence.generate_starting_binary()

# creation of the successors of initial_binary_cuts_sequence
binary_successors = initial_binary_cuts_sequence.get_successors()

# definition of a SelectedDimensionalSequenceNumeric containing S_ds
# selected cuts sequences using first element of binary_successors list
successor = SelectedDimensionalSequenceNumeric()
successor.from_binary(cuts_sequence, binary_successors[0])
