from cut_sequences.dimensional_sequence import DimensionalSequence
import numpy as np


# Class for define selected cuts S_d in a logical way
class DimensionalSequenceBinary(DimensionalSequence):

    # SelectedCuts class constructor method
    # @S_d: selected cuts to be converted in logical sequence
    # @T_d: general cuts sequence
    def __init__(self, S_d, T_d):

        # calling superclass constructor
        super().__init__()

        # control for define if the passed parameters are iterable objects
        # If parameters aren't iterable objects then the constructor fail and
        # show an error message
        try:
            _ = (element for element in S_d)
            _ = (element for element in T_d)
        except TypeError:
            print("Error in creating DimensionalSequenceBinary. Passed non-iterable parameter")
            return

        # evaluate T_d and S_d dimension in parallel
        for T_d_dimension, S_d_dimension in zip(T_d, S_d):

            # defining an empty list which represents the presence of cuts
            # in the evaluated S_d dimension (in a logical way)
            binary_array = list()

            # for every cut in evaluated T_d dimension, if that cut is in S_d dimension then
            # set the corresponding value to true into the binary array, elsewhere set it to False
            [ binary_array.append(True) if cut in S_d_dimension else binary_array.append(False) for cut in T_d_dimension ]

            # inserting the binary array (casted into a NumPy array) in the elementlist
            self.elementlist.append(np.array(binary_array))


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

