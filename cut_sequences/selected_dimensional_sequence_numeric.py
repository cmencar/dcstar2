from cut_sequences.dimensional_sequence import DimensionalSequence
from cut_sequences.hyperboxes_set import HyperboxesSet
from cut_sequences.dimensional_sequence_binary import DimensionalSequenceBinary
import numpy as np


# Class defining selected cuts sequences
class SelectedDimensionalSequenceNumeric(DimensionalSequence):

    # Cuts class constructor method
    # @selected_cuts_list: list of selected cuts sequence for each dimension
    def __init__(self, selected_cuts_list = []):

        # calling superclass constructor
        super().__init__()

        # control for define if the passed parameter is an iterable object
        # If parameter isn't iterable object then the constructor fail and
        # show an error message
        try:
            _ = (element for element in selected_cuts_list)
        except TypeError:
            print("Error in creating SelectedCutsSequence. Passed non-iterable parameter")
            return

        # define a list of element composed by NumPy array (one of each dimension of S_d)
        # where its elements are the same cuts passed in cuts_list structure
        self.elements = [np.array([cut for cut in S_d]) for S_d in selected_cuts_list]


    # Function for converting a logical cut sequence to a point-based cut sequence
    # @cuts_sequences: general cut sequence
    # @selected_binary_cuts_sequences: logical cut sequence
    def from_binary(self, cuts_sequences, selected_binary_cuts_sequences):

        # clear all previous elements into elements
        self.elements.clear()

        # for each S_d_bin logical sequence cut
        for dimension_index in range(selected_binary_cuts_sequences.get_dimensions_number()):

            # definition of a temporary cuts' list for the evaluated dimension. The list contain numerical values
            # of cuts for the evaluated dimension, presents in T_d, where the corresponding value in S_d_bin is True
            dimension_cuts = [cuts_sequences.get_dimension(dimension_index)[cut_index]
                              for cut_index in range(selected_binary_cuts_sequences.get_dimension_size(dimension_index))
                              if selected_binary_cuts_sequences.get_cut(dimension_index, cut_index)]

            # insert a new dimension in selected cuts sequences structure
            self.elements.append(np.array(dimension_cuts))


    # Function for creating a logical cut sequence from the comparison between a general cut sequence
    # and a selected cut sequence
    # @cuts_sequences: general cuts sequence objects
    def get_binary(self, cuts_sequences):

        # definition of T_d cuts sequence taken from cuts_sequences. The list is made evaluating
        # each dimension of DimensionalSequence object and putting them into the 'cuts_list_converted' list
        # (the T_d dimensions are NumPy arrays)
        cuts_list_converted = [cuts_sequences.get_dimension(dimension_index)
                               for dimension_index in range(cuts_sequences.get_dimensions_number())]

        # return the logical cut sequence using SelectedCutsSequenceBin constructor passing the converted
        # general cuts list and selected cuts sequence's elements
        return DimensionalSequenceBinary(self.elements, cuts_list_converted)


    # Function for generate an hyperboxes set starting from any selected cuts sequences
    # @point_list: list of prototype points
    # @m_d: smallest boundary cut of dimension d
    # @M_d: greatest boundary cut of dimension d
    def generate_hyperboxes_set(self, point_list, m_d, M_d):

        # initialization of a list of intervals
        expanded_intervals = list()

        # initialization of index for dimensional m_d and M_d
        dimension_index = 0

        # for each S_d sequence
        for S_d in self.elements:

            # initialization of a list of intervals for the evaluated dimension
            expanded_S_d = list()

            # set the m_d cut, the leftmost cut of dimension
            expanded_S_d.append(m_d[dimension_index])

            # for each cut in evaluate dimension, insert it into the list of intervals for that dimension
            for cut_index in range(len(S_d)):
                expanded_S_d.append(S_d[cut_index])

            # set the M_d cut, the rightmost cut of dimension
            expanded_S_d.append(M_d[dimension_index])

            # insert the list of interval for evaluate dimension into the expanded S_d interval list
            expanded_intervals.append(expanded_S_d)

            # increment the index for m_d and M_d
            dimension_index += 1

        # return the created hyperboxes set
        return HyperboxesSet(point_list, expanded_intervals)

