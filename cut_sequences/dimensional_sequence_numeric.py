from cut_sequences.dimensional_sequence_binary import DimensionalSequenceBinary
from cut_sequences.dimensional_sequence import DimensionalSequence
import numpy as np


# Class for define cuts sequence T_d
class DimensionalSequenceNumeric(DimensionalSequence):

    # Cuts class constructor method
    # @cuts_list: list of cuts for each dimension
    def __init__(self, cuts_list = None):

        # calling superclass constructor
        super().__init__()

        # control for define if the passed parameter is an iterable object
        # If parameter isn't iterable object then the constructor fail and
        # show an error message
        try:
            _ = (element for element in cuts_list)
        except TypeError:
            print("Error in creating CutsSequence. Passed non-iterable parameter")
            return

        # for each dimension take its cuts, insert them in a list
        # and convert that list in a NumPy array. Finally, insert
        # the newly created NumPy array in elementlist
        self.elements = [np.array([cut for cut in dimension]) for dimension in cuts_list]


    # Function for creating a general cut sequence to
    # a logical cut sequence, where each element (corresponding to
    # an element of T_d) is a False logical value
    def generate_starting_binary(self):

        # initialize an empty list for the creation of a dummy S_d cuts sequence
        # and insert an empty NumPy array for each dimension of T_d
        empty_S_d = [np.ndarray([]) for dimension in self.elements]

        # creating a SelectedCutsSequenceBin using the dummy S_d
        # for defining the absence of cuts
        return DimensionalSequenceBinary(empty_S_d, self.elements)
