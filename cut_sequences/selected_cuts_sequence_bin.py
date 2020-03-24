from cut_sequences.cuts import Cuts
import numpy as np


# Class for define selected cuts S_d in a logical way
class SelectedCutsSequenceBin(Cuts):

    # SelectedCuts class constructor method
    # @
    # @
    def __init__(self, S_d, T_d):

        # calling superclass constructor
        super().__init__()

        try:
            _ = (element for element in S_d)
            _ = (element for element in T_d)
        except TypeError:
            print("Error in creating SelectedCutsSequenceBin. Passed non-iterable parameter")
            return

        for dimension_td, dimension_sd in zip(T_d, S_d):
            binary_array = list()
            [ binary_array.append(True) if cut in dimension_sd else binary_array.append(False)
              for cut in dimension_td ]
            self.elementlist.append(np.array(binary_array))

    '''
        for dimension_index in range(T_d.get_dimensions_number()):
            binary_array = list()
            [ binary_array.append(True) if T_d.get_dimension(dimension_index)[cut_index] in S_d.get_dimension(dimension_index) else binary_array.append(False)
              for cut_index in range(T_d.get_dimension_size(dimension_index)) ]
            self.elementlist.append(np.array(binary_array))
    '''


    # Method for setting a single dimension
    # @dimension: index of the dimension to be set
    # @cut_index: cut sequence's index to be set
    # @value: cut value to be set
    def set_cut(self, dimension, cut_index, value):

        try:

            # Set the single cut of dimension with a boolean element
            self.elementlist[dimension][cut_index] = value

        except IndexError:

            # print an error message if the index refers to a non-existent dimension
            print("Dimension not found, impossible to initialize")


    # Method for returning the value of a single cut of single dimension
    # @dimension: index of the dimension to be get
    # @cut_index: index of the cut to be get
    # @return the boolean for the passed cut of passed dimension
    def get_cut(self, dimension, cut_index):

        try:

            # return the boolean element for the cut
            return self.elementlist[dimension][cut_index]

        except IndexError:

            # print an error message if the index refers to a non-existent dimension
            print("Dimension not found, impossible to initialize")

