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
        self.elementlist = [ np.array([ True if cut in S_d_dimension else False for cut in T_d_dimension ])
                             for T_d_dimension, S_d_dimension in zip(T_d, S_d) ]


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
        self.elementlist.clear()

        # converting each dimension
        [ self.elementlist.append(np.array(dimension)) for dimension in S_d_bin ]


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


    # Method for creating successors of S_d_bin (in binary form)
    def get_successors(self):

        successors = list()

        dimension_index = 0

        for dimension in self.elementlist:

            cut_index = 0

            for cut in dimension:

                if not cut:

                    new_elementlist = [ np.array([ cut for cut in array ]) for array in self.elementlist ]

                    new_elementlist[dimension_index][cut_index] = True

                    successor = DimensionalSequenceBinary()

                    successor.from_binary(new_elementlist)

                    successors.append(successor)

                cut_index = cut_index + 1

            dimension_index = dimension_index + 1

        return successors