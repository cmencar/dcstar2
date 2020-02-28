import numpy as np
from Cuts import Cuts


# Class for define cuts T_d
class CutsSequence(Cuts):

    # Cuts class constructor method
    # @dimensions: number of dimensions of the T_d sequence to initialize as empty lists
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
                        np.sort(npdim)
                        self.elementlist.append(npdim)
            else:
                for dim in cuts_list:
                    npdim = np.array(dim)
                    np.sort(npdim, kind='mergesort')
                    self.elementlist.append(npdim)


    # Method for setting a single dimension
    # @dimension: index of the dimension to be set
    # @cuts: cut sequence to be defined
    def set_dimension(self, dimension, cuts):

        try:

            # if inserted dimension refer to a not-existent dimension
            # then insert a new NumPy array
            if len(self.elementlist) < dimension:
                self.elementlist.insert(dimension, np.array([]))

            # if passed cuts is configured as a NumPy array,
            # set the single dimension with that array. Otherwise,
            # convert the passed list in a NumPy array.
            if isinstance(cuts, np.ndarray):
                np.sort(cuts, kind='mergesort')
                self.elementlist[dimension - 1] = cuts
            else:
                npcuts = np.array(cuts)
                np.sort(npcuts, kind='mergesort')
                self.elementlist[dimension - 1] = npcuts

        except IndexError:

            # print an error message if the index refers to a non-existent dimension
            print("Dimension not found, impossible to initialize")


    # Method for returning the values of a single dimension
    # @dimension: index of the dimension to be get
    # @return the NumPy array for the passed dimension
    def get_dimension(self, dimension):

        try:

            # return the NumPy array of the dimension
            return self.elementlist[dimension - 1]

        except IndexError:

            # print an error message if the index refers to a non-existent dimension
            print("Dimension not found, returned None")

            # return a None value
            return None
