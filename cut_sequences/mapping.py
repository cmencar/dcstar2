from cut_sequences.selected_cuts_sequence_bin import SelectedCutsSequenceBin
from cut_sequences.selected_cuts_sequence import SelectedCutsSequence
from cut_sequences.hyperboxes_set import HyperboxesSet
import numpy as np



'''
# Function for converting a point-based cut sequence to
# a logical cut sequence to
# @T_d: general cut sequence
# @S_d: point-based cut sequence
def from_point_to_logical(T_d, S_d):

    # definition of a new S_d sequence of selected cuts
    S_d_bin = SelectedCutsSequenceBin()

    # if cut sequence is empty then return an S_d_bin
    # with every logical value set to False
    if S_d.get_dimensions_number() < 1:
        return generate_starting_binary_t_d(T_d)
    else:

        # for each dimension of T_d cut sequence
        for dimension_index in range(1, T_d.get_dimensions_number() + 1):

            # definition of a temporary element's list for the evaluated dimension
            dimension_elements = list()

            # definition of indexes for scanning the NumPy arrays
            T_d_index = 0
            S_d_index = 0

            # until the scan of all elements in the T_d array is completed
            while T_d_index < T_d.get_dimension_size(dimension_index):

                # if S_d's dimension referred is an empty NumPy array then
                # insert a False logical value for each T_d corrisponding element
                # and increment T_d_index
                if S_d.get_dimension_size(dimension_index) == 0 or S_d.get_dimension_size(dimension_index) <= S_d_index:
                    dimension_elements.append(False)
                    T_d_index = T_d_index + 1

                # if T_d's dimension value referred is lower than S_d's dimension
                # value referred then insert a False logical value for that
                # element and increment T_d_index
                elif T_d.get_dimension(dimension_index)[T_d_index] < S_d.get_dimension(dimension_index)[S_d_index]:
                    dimension_elements.append(False)
                    T_d_index = T_d_index + 1

                # if T_d's dimension value referred is equal to S_d's dimension
                # value referred then insert a True logical value for that
                # element and increment both T_d_index and S_d_index
                elif T_d.get_dimension(dimension_index)[T_d_index] == S_d.get_dimension(dimension_index)[S_d_index]:
                    dimension_elements.append(True)
                    T_d_index = T_d_index + 1
                    S_d_index = S_d_index + 1

            # inserting the list of logical elements, made by T_d element's presence
            # into S_d structure, into S_d_bin structure (converting automatically
            # the list into a NumPy array)
            S_d_bin.set_dimension(dimension_index, dimension_elements)

    # return complete S_d_bin structure
    return S_d_bin
'''




