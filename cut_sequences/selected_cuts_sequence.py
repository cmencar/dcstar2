from cut_sequences.dimensional_sequence import DimensionalSequence
from cut_sequences.hyperboxes_set import HyperboxesSet
from cut_sequences.dimensional_sequence_binary import DimensionalSequenceBinary
import numpy as np


# Class defining selected cuts sequence S_d
class SelectedCutsSequence(DimensionalSequence):

    # Cuts class constructor method
    # @cuts_list: list of cuts for each dimension
    def __init__(self, cuts_list = []):

        # calling superclass constructor
        super().__init__()

        # control for define if the passed parameter is an iterable object
        # If parameter isn't iterable object then the constructor fail and
        # show an error message
        try:
            _ = (element for element in cuts_list)
        except TypeError:
            print("Error in creating SelectedCutsSequence. Passed non-iterable parameter")
            return

        # for each dimension take its cuts, insert them in a list
        # and convert that list in a NumPy array. Finally, insert
        # the newly created NumPy array in elementlist
        for dimension in cuts_list:
            formatted_cuts_list = list()
            [ formatted_cuts_list.append(cut) for cut in dimension ]
            self.elementlist.append(np.array(formatted_cuts_list))


    # Function for converting a logical cut sequence to
    # a point-based cut sequence
    # @T_d: general cut sequence
    # @S_d_bin: logical cut sequence
    def from_binary(self, T_d, S_d_bin):

        # clear all previous elements into elementlist
        self.elementlist.clear()

        # for each dimension of S_d_bin logical sequence cut
        for dimension_index in range(S_d_bin.get_dimensions_number()):

            # definition of a temporary element's list for the evaluated dimension
            dimension_elements = list()

            # definition of an index for the temporary element's list
            dimension_element_index = 0

            # for each element in dimension referred by dimension_index
            for element_index in range(S_d_bin.get_dimension_size(dimension_index)):

                # if cut logical value set in dimension referred by dimension_index at
                # position referred by element_index is True, then insert into the
                # temporary element's list the corrisponding point-based value of
                # T_d cut sequence
                if S_d_bin.get_cut(dimension_index, element_index):
                    dimension_elements.insert(dimension_element_index, T_d.get_dimension(dimension_index)[element_index])
                    dimension_element_index = dimension_element_index + 1

            # insert a new dimension in S_d structure
            self.elementlist.append(dimension_elements)


    # Function for creating a logical cut sequence from the comparison
    # between a general cut sequence and a selected cut sequence
    # @T_d: general cut sequence
    def get_binary(self, T_d):

        # initializing empty list of generic cuts
        T_d_converted = list()

        # for each dimension in the general cuts sequence,
        # append the whole dimension into the list
        [ T_d_converted.append(T_d.get_dimension(dimension_index)) for dimension_index in range(T_d.get_dimensions_number()) ]

        # return the logical cut sequence using SelectedCutsSequenceBin constructor
        # passing the converted general cuts list and selected cuts sequence's elementlist
        return DimensionalSequenceBinary(self.elementlist, T_d_converted)


    # Function for generate an hyperboxes set starting
    # from any S_d sequence of cuts
    # @point_list: list of prototype points
    # @m_d: smallest boundary cut of dimension d
    # @M_d: greatest boundary cut of dimension d
    def generate_hyperboxes_set(self, point_list, m_d = 0, M_d = 1):

        # initialization of a list of intervals
        intervals = list()

        # for each dimension in S_d sequence
        for dimension in self.elementlist:

            # get the evaluated dimension and the number of cuts in it
            dimension_size = len(dimension)

            # initialization of a list of intervals for
            # the evaluated dimension
            dimension_intervals = list()

            # set the m_d cut, the leftmost cut of dimension
            dimension_intervals.append(m_d)

            # for each cut in evaluate dimension, insert it into
            # the list of intervals for that dimension
            [ dimension_intervals.append(dimension[cut_index]) for cut_index in range(dimension_size) ]

            # set the M_d cut, the rightmost cut of dimension
            dimension_intervals.append(M_d)

            # insert the list of interval for evaluate dimension into
            # the S_d interval list
            intervals.append(dimension_intervals)

        # creation of hyperboxes set
        hyperboxes = HyperboxesSet(point_list, intervals)

        # return the set of hyperboxes
        return hyperboxes

