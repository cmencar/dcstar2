from cut_sequences.selected_cuts_sequence_bin import SelectedCutsSequenceBin
from cut_sequences.cuts import Cuts
import numpy as np


# Class for define cuts sequence T_d
class CutsSequence(Cuts):

    # Cuts class constructor method
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
            if isinstance(cuts_list, np.ndarray):
                for dim in cuts_list:
                    if isinstance(dim, np.ndarray):
                        np.sort(dim, kind='mergesort')
                        self.elementlist.append(dim)
                    else:
                        npdim = np.array(dim)
                        np.sort(npdim, kind='mergesort')
                        self.elementlist.append(npdim)
            else:
                for dim in cuts_list:
                    npdim = np.array(dim)
                    np.sort(npdim, kind='mergesort')
                    self.elementlist.append(npdim)


    # Function for converting a general cut sequence to
    # a logical cut sequence, where each element (corresponding
    # an element of T_d) is a False logical value
    # @T_d: general cut sequence
    def generate_starting_binary(self):

        empty_S_d = list()

        for dimension in self.elementlist:
            empty_S_d.append(np.ndarray([]))

        return SelectedCutsSequenceBin(empty_S_d, self.elementlist)

        '''
        # definition of a new list of logical value
        T_d_bin = list()

        # for each dimension of T_d sequence cut
        for dimension_index in range(T_d.get_dimensions_number()):

            # definition of a list of logical value for referred dimension
            dimension = list()

            # for each element in dimension referred by dimension_index
            # insert a False logical value
            for element in T_d.get_dimension(dimension_index):
                dimension.append(False)

            # insert the logical value cut dimension's list
            # into T_d_bin
            T_d_bin.insert(dimension_index, dimension)

        # return a BinaryCuts object using T_d_bin elements
        # return SelectedCutsSequenceBin(T_d_bin)
        return SelectedCutsSequenceBin(None, T_d)
        '''
