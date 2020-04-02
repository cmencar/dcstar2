from abc import ABC, abstractmethod


# abstract class for defining a cuts sequence wrapper
class DimensionalSequence(ABC):

    # Class constructor
    def __init__(self):

        # initialization of list of cuts
        self.__elements = list()


    # Method for returning the values of a single dimension
    # @dimension: index of the dimension to be get
    def get_dimension(self, dimension):

        # if the index refers to a non-existent dimension then print an error message,
        # elsewhere return the correct value
        try:
            return self.__elements[dimension]
        except IndexError:
            print("Dimension not found, impossible to initialize")


    # Method for returning the number of dimensions
    def get_dimensions_number(self):
        return len(self.__elements)


    # Method for returning the value of the size of single dimension
    # @dimension: index of the dimension to be get its size
    def get_dimension_size(self, dimension):

        # if the index refers to a non-existent dimension then print an error message,
        # elsewhere return the correct value
        try:
            return len(self.__elements[dimension])
        except IndexError:
            print("Dimension not found, impossible to get")


    # Method for a debug print of sequence cuts
    def debug_print(self):

        # index initialization
        i = 1

        # for each dimension's array in S_d, print its data
        for dimension_array in self.__elements:
            print("Dimension ", i, ": ", dimension_array)
            i = i + 1
