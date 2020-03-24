from cut_sequences.cuts import Cuts
from cut_sequences.hyperboxes_set import HyperboxesSet
from cut_sequences.selected_cuts_sequence_bin import SelectedCutsSequenceBin
import numpy as np


# Class defining selected cuts sequence S_d
class SelectedCutsSequence(Cuts):

    # Cuts class constructor method
    # @dimensions: number of dimensions of the S_d sequence to initialize as empty lists
    # @cuts_list: list of cuts for each dimension
    def __init__(self, cuts_list=None):

        # calling superclass constructor
        super().__init__()

        # if passed cuts' list is empty
        if cuts_list is None:
            self.elementlist.append(np.array([]))
        else:

            # if passed cuts' list is configured as a list of NumPy array,
            # set the single dimension with that array. Otherwise,
            # convert the passed list of list in a list of NumPy array.
            # before the initialization, every dimension is sorted
            if isinstance(cuts_list, np.ndarray):
                for dim in cuts_list:
                    np.sort(dim, kind='mergesort')
                    self.elementlist.append(dim)
            else:
                for dim in cuts_list:
                    npdim = np.array(dim)
                    np.sort(npdim, kind='mergesort')
                    self.elementlist.append(npdim)


    # Function for converting a logical cut sequence to
    # a point-based cut sequence
    # @T_d: general cut sequence
    # @S_d_bin: logical cut sequence
    def from_binary(self, T_d, S_d_bin):

        # definition of a new S_d sequence of selected cuts
        #S_d = SelectedCutsSequence()

        # if logical cut sequence is empty then return an empty S_d
        #if S_d_bin.get_dimensions_number() < 1:
        #    return
        #else:
        self.elementlist.clear()

        # for each dimension of S_d_bin logical sequence cut
        for dimension_index in range(S_d_bin.get_dimensions_number()):

            # if dimension referred by dimension_index is empty then
            # set an empty NumPy array
            if S_d_bin.get_dimension_size(dimension_index) < 1:
                #S_d.set_dimension(dimension_index, np.array([]))
                self.elementlist.append(np.array([]))
            else:

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
                        dimension_elements.insert(dimension_element_index,
                                                  T_d.get_dimension(dimension_index)[element_index])
                        dimension_element_index = dimension_element_index + 1

                # insert a new dimension in S_d structure
                #S_d.set_dimension(dimension_index, dimension_elements)
                self.elementlist.append(dimension_elements)

    # Function for creating a logical cut sequence from the comparison
    # between a general cut sequence and a selected cut sequence
    def get_binary(self, T_d):

        # initializing empty list of generic cuts
        T_d_converted = list()

        # for each dimension in the general cuts sequence,
        # append the whole dimension into the list
        for dimension_index in range(T_d.get_dimensions_number()):
            T_d_converted.append(T_d.get_dimension(dimension_index))

        # return the logical cut sequence using SelectedCutsSequenceBin constructor
        # passing the converted general cuts list and selected cuts sequence's elementlist
        return SelectedCutsSequenceBin(self.elementlist, T_d_converted)


    # Function for generate an hyperboxes set starting
    # from any S_d sequence of cuts
    # @point_list: list of prototype points
    # @m_d: smallest boundary cut of dimension d
    # @M_d: greatest boundary cut of dimension d
    def generate_hyperboxes_set(self, point_list, m_d=0, M_d=1):

        # initialization of a list of intervals
        intervals = list()

        # for each dimension in S_d sequence
        for dimension in self.elementlist:

            # get the evaluated dimension and the number of cuts in it
            dimension_size = len(dimension)

            # initialization of a list of intervals for
            # the evaluated dimension
            dimension_intervals = list()

            # if the evaluated dimension has at least one cut
            if dimension_size > 0:

                # set the m_d cut, the leftmost cut of dimension
                dimension_intervals.append(m_d)

                # for each cut in evaluate dimension, insert it into
                # the list of intervals for that dimension
                for cut_index in range(0, dimension_size):
                    dimension_intervals.append(dimension[cut_index])

                # set the M_d cut, the rightmost cut of dimension
                dimension_intervals.append(M_d)

            # if the evaluate dimension doesn't have a cut, then set
            # only m_d and M_d cuts
            else:
                dimension_intervals.append(m_d)
                dimension_intervals.append(M_d)

            # insert the list of interval for evaluate dimension into
            # the S_d interval list
            intervals.append(dimension_intervals)

        # initialization of a list of valid intervals, used for
        # saving not-empty lists
        valid_intervals = list()

        # inserting into valid_intervals list only the not-empty sublists
        [valid_intervals.append(interval) for interval in intervals if interval]

        # creation of hyperboxes set
        hyperboxes = HyperboxesSet(point_list, valid_intervals)

        # return the set of hyperboxes
        return hyperboxes

