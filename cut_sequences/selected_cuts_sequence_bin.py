from cut_sequences.cuts import Cuts
import numpy as np


# Class for define selected cuts S_d in a logical way
class SelectedCutsSequenceBin(Cuts):

    # SelectedCuts class constructor method
    # @cuts_list: list of cuts (defined in a logical way) for each dimension
    def __init__(self, cuts_list=None):

        # calling superclass constructor
        super().__init__()

        # initialize the error flag
        error = False

        try:

            # if cuts' list has a content then
            # check if every cut is a binary element
            if cuts_list is not None:
                for cuts_dimension in cuts_list:
                    for cut in cuts_dimension:
                        assert cut is True or cut is False

        except AssertionError:

            # print an error message if the assertion fails and
            # initialize the size to a default value and set the error flag
            print("Error in constructing a new BinaryCuts object (passed a non-binary element).")
            error = True

        finally:

            # set cuts_list correct structure
            if cuts_list is None:
                cuts_list = list()

            # if there isn't an error in asserting list content
            if error is not True:

                # if passed logic cuts' list is configured as a list of NumPy array,
                # set the single dimension with that array. Otherwise,
                # convert the passed list of list in a list of NumPy array.
                if isinstance(cuts_list, np.ndarray):
                    for dimension in cuts_list:
                        self.elementlist.append(dimension)
                else:
                    for dimension in cuts_list:
                        self.elementlist.append(np.array(dimension))


    # Method for setting a single dimension
    # @dimension: index of the dimension to be set
    # @cuts: cut sequence to be defined
    def set_dimension(self, dimension, cuts):

        try:

            # if inserted dimension refer to a not-existent dimension
            # then insert a new NumPy array
            if len(self.elementlist) < dimension:
                self.elementlist.insert(dimension - 1, np.array([]))

            # if passed cuts is configured as a NumPy array,
            # set the single dimension with that array. Otherwise,
            # convert the passed list in a NumPy array.
            if isinstance(cuts, np.ndarray):
                self.elementlist[dimension - 1] = cuts
            else:
                self.elementlist[dimension - 1] = np.array(cuts)

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
            self.elementlist[dimension - 1][cut_index - 1] = value

        except IndexError:

            # print an error message if the index refers to a non-existent dimension
            print("Dimension not found, impossible to initialize")


    # Method for returning the values of a single dimension
    # @dimension: index of the dimension to be get
    # @return the NumPy array for the passed dimension
    def get_dimension(self, dimension):

        try:

            return self.elementlist[dimension - 1]

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
            return self.elementlist[dimension - 1][cut_index - 1]

        except IndexError:

            # print an error message if the index refers to a non-existent dimension
            print("Dimension not found, impossible to initialize")

