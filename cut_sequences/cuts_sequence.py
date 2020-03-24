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


    # Function for creating a general cut sequence to
    # a logical cut sequence, where each element (corresponding to
    # an element of T_d) is a False logical value
    def generate_starting_binary(self):

        # initialize an empty list for the creation
        # of a dummy S_d cuts sequence
        empty_S_d = list()

        # insert an empty NumPy array for each dimension of T_d
        [ empty_S_d.append(np.ndarray([])) for dimension in self.elementlist ]

        # creating a SelectedCutsSequenceBin using the dummy S_d
        # for defining the absence of cuts
        return SelectedCutsSequenceBin(empty_S_d, self.elementlist)
