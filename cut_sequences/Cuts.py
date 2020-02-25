from abc import ABC, abstractmethod
import numpy as np


# abstract class for cuts sequence
class Cuts(ABC):

    # Class constructor
    def __init__(self):

        # initialization of list of cuts
        self.elementlist = list()


    # Method for setting a single dimension
    # @dimension: index of the dimension to be set
    # @cuts: cut sequence to be defined
    @abstractmethod
    def set_dimension(self, dimension, cuts):
        pass


    # Method for returning the values of a single dimension
    # @dimension: index of the dimension to be get
    # @return the NumPy array for the passed dimension
    @abstractmethod
    def get_dimension(self, dimension):
        pass


    # Method for returning the number of dimensions
    # @dimension: index of the dimension to be get its size
    def get_dimensions_number(self):

        # return the size of list
        return np.size(self.elementlist)


    # Method for returning the value of the size of single dimension
    # @dimension: index of the dimension to be get its size
    def get_dimension_size(self, dimension):

        try:

            # return the size of NumPy array
            return np.size(self.elementlist[dimension - 1])

        except IndexError:

            # print an error message if the index refers to a non-existent dimension
            print("Dimension not found")


    # Method for a debug print of sequence cuts
    def debug_print(self):

        # index initialization
        i = 1

        # for each dimension's array in S_d, print its data
        for dimension_array in self.elementlist:
            print("Dimension ", i, ": ", dimension_array)
            i = i + 1