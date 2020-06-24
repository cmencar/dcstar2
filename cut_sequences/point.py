import numpy as np

# Class for the definition of a given point (prototype)
# into the features space
class Point:

    # Class constructor
    # @coordinates_array: points' coordinates for every dimension
    # @label: point label
    # @name: point name
    def __init__(self, coordinates, label = None, name = None):

        # control for define if the passed parameter is an iterable object
        # If parameter isn't iterable object then the constructor fail and
        # show an error message
        try:
            _ = (element for element in coordinates)
        except TypeError:
            print("Error in creating Point. Passed non-iterable parameter")
            return

        # acquire every coordinate, insert them in a list
        # and convert the list into a NumPy array

        self.__coordinates = np.array([coordinate for coordinate in coordinates])

        # initialize label information
        self.__label = label

        # initialize name information
        self.__name = name


    # Method for acquiring all dimensions' coordinates
    def get_coordinates(self):
        return self.__coordinates


    # Method for acquiring coordinate for specific dimension
    # @dimension: dimension correlated to coordinate to be get
    def get_coordinate(self, dimension):

        # if the indexes refers to a non-existent coordinate then print
        # an error message, elsewhere return the correct value
        try:
            return self.__coordinates[dimension]
        except IndexError:
            print("Coordinate not found, impossible to get")


    # Method for acquiring point label
    def get_label(self):
        return self.__label


    # Method for acquiring point associated name
    def get_name(self):
        return self.__name


