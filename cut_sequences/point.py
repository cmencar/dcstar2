import numpy as np


# Class for the definition of a given point
# into the features space
class Point:

    # Class constructor
    # @coordinates_array: points' coordinates for every dimension
    # label: point label
    # name: point name
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
        coordinate_list = list()
        [ coordinate_list.append(coordinate) for coordinate in coordinates ]
        self.coordinates = np.array(coordinate_list)

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
            return self.coordinates[dimension]

        except IndexError:

            # print an error message if the index refers to a non-existent dimension
            print("Dimension not found")


    # Method for acquiring point label
    def get_label(self):
        return self.label


    # Method for acquiring point associated name
    def get_name(self):
        return self.name

