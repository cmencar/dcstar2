from cut_sequences.dimensional_sequence import DimensionalSequence
import numpy as np


# Class for define selected cuts S_d in a logical way
class DimensionalSequenceBinary(DimensionalSequence):

    # DimensionalSequenceBinary class constructor method
    # @S_d: iterable structure for selected cuts to be converted in logical sequence
    # @T_d: iterable structure for general cuts sequence
    def __init__(self, S_d = [], T_d = []):

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

        # defining a list that represents the presence of cuts in the evaluated S_d in a logical way.
        # First of all, for doing this, it must evaluate T_d and S_d dimension in parallel.
        # Later, for every cut in evaluated T_d dimension, if that cut is in S_d dimension then
        # set the corresponding value into the binary array to True, elsewhere set it to False
        self.elements = [np.array([True if cut in S_d_dimension else False for cut in T_d_dimension])
                         for T_d_dimension, S_d_dimension in zip(T_d, S_d)]


    # Method for creating binary sequence cut from a
    # structure that contains logical values
    # @S_d_bin: iterable structure for logical selected cuts sequence
    def from_binary(self, S_d_bin):

        # control for define if the passed parameters are iterable objects
        # If parameters aren't iterable objects then the constructor fail and
        # show an error message
        try:
            _ = (element for element in S_d_bin)
        except TypeError:
            print("Error in creating DimensionalSequenceBinary. Passed non-iterable parameter")
            return

        # clear the previous written data
        self.elements.clear()

        # converting each dimension from a list form
        # to a NumPy array form
        self.elements = [np.array(dimension) for dimension in S_d_bin]


    # Method for returning the value of a single cut of single dimension
    # @dimension: index of the dimension to be get
    # @cut_index: index of the cut to be get
    # @return the boolean for the passed cut of passed dimension
    def get_cut(self, dimension, cut_index):

        # if the indexes refers to a non-existent element then print an error message,
        # elsewhere return the correct value
        try:
            return self.elements[dimension][cut_index]
        except IndexError:
            print("Cut not found, impossible to get")


    # Method for setting a single dimension
    # @dimension: index of the dimension to be set
    # @cut_index: cut sequence's index to be set
    # @value: cut value to be set
    def set_cut(self, dimension, cut_index, value):

        # if the indexes refers to a non-existent element then print an error message,
        # elsewhere set the passed value
        try:
            self.elements[dimension][cut_index] = value
        except IndexError:
            print("Dimension not found, impossible to initialize")


    # Method for creating successors of S_d_bin in binary form
    def get_successors(self):

        # initialize a successors empty list
        successors = list()

        # initialize the index used to identify the specific dimension
        # of the cut to be set to True (i.e. the cut that differentiates an
        # S_d_bin element from his successor)
        dimension_index = 0

        # each dimension is evaluated in order to analyze each possible editable cut
        for dimension in self.elements:

            # the index used to identify the specific cut to be set to True
            cut_index = 0

            # for each cut in the evaluated dimension, if it is equal to False
            # then it can be modified in order to create a successor.
            for cut in dimension:

                # if the evaluated cut binary value is False
                if not cut:

                    # copy every logical cut value from S_d_bin and create
                    # the successor binary structure. Then, set the specific
                    # evaluated cut from False to True
                    binary_successor = [np.array([cut for cut in dimension_array]) for dimension_array in self.elements]
                    binary_successor[dimension_index][cut_index] = True

                    # the logical raw sequence is used to create a
                    # DimensionalSequenceBinary object. The object is
                    # then added to successors' list
                    successor = DimensionalSequenceBinary()
                    successor.from_binary(binary_successor)
                    successors.append(successor)

                # increment the cut_index value
                cut_index += 1

            # increment the dimension_index value
            dimension_index += 1

        return successors
