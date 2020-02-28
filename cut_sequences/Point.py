import numpy as np


# Class for the definition of a given point
# into the features space
class Point:

    # Class constructor
    def __init__(self, coordinates_array = None, label = None, name = None):

        # if coordinates' array is not empty
        if coordinates_array is not None:

            # if coordinates' array is an NumPy array, set
            # the coordinates' class array with passed array
            if isinstance(coordinates_array, np.ndarray):
                self.coordinates = coordinates_array

            # if coordinates' array is not a NumPy array
            else:

                # initialize the coordinates' array with a NumPy array
                self.coordinates = np.ndarray(shape=(len(coordinates_array),))

                # initialize the array index
                array_index = 0

                # for each coordinate into the coordinates' array,
                # insert it as new element of coordinates' class array
                for coordinate in coordinates_array:
                    self.coordinates.put(array_index, coordinate)
                    array_index = array_index + 1

        # if coordinates' array is empty, set an empty NumPy array
        # as coordinates' class array
        else:
            self.coordinates = np.array([])

        # initialize label information
        self.label = label

        # initialize name information
        self.name = name


    # Method for acquiring all dimensions' coordinates
    def get_coordinates(self):
        return self.coordinates


    # Method for acquiring coordinate for specific dimension
    def get_coordinate(self, dimension):

        try:

            # return the coordinates for specific dimension
            return self.coordinates[dimension - 1]

        except IndexError:

            # print an error message if the index refers to a non-existent dimension
            print("Dimension not found")


    # Method for setting coordinate for specific dimension
    def set_coordinate(self, dimension, coordinate):

        try:

            # set the coordinates for specific dimension
            self.coordinates[dimension - 1] = coordinate

        except IndexError:

            # print an error message if the index refers to a non-existent dimension
            print("Dimension not found")


    # Method for setting coordinate for specific dimension
    def add_coordinate(self, dimension, coordinate):

        try:

            # add the coordinate for specific dimension
            self.coordinates.insert(dimension - 1, coordinate)

        except IndexError:

            # print an error message if the index refers to a non-existent dimension
            print("Dimension not found")


    # Method for acquiring point label
    def get_label(self):
        return self.label


    # Method for setting point label
    def set_label(self, label):
        self.label = label


    # Method for acquiring point associated name
    def get_name(self):
        return self.name


    # Method for setting point associated name
    def set_name(self, name):
        self.name = name

