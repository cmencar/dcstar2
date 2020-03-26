
# Class for defining a single hyperbox using
# a particular set of intervals
class Hyperbox:

    # Class constructor. Needs set of intervals
    # made by tuple of tuples
    # @hyperbox_tuple: set of intervals
    def __init__(self, hyperbox_boundaries):

        # initializing boundaries and points structure
        self.points = list()

        # acquire every dimensional boundaries, insert them in a list
        # (as a list of tuples) and convert the list into a tuple
        self.boundaries = tuple([ tuple(dimensional_boundaries) for dimensional_boundaries in hyperbox_boundaries ])


    # Method for acquiring hyperbox boundaries for each dimension
    def get_boundaries(self):
        return self.boundaries


    # Method for setting belonging point of hyperbox
    # @point_list: single points, part of hyperbox
    def set_belonging_point(self, point):
        self.points.append(point)


    # Method for acquiring belonging points of hyperbox
    def get_belonging_points(self):
        return self.points


    # Method for checking if a given point is in the hyperbox
    def has_point(self, point):
        return [ True if point in self.points else False ]


    # Method for checking if the hyperbox is impure
    def is_impure(self):

        # initialization of service variables
        is_impure = False
        point_label = self.points[0].get_label()
        point_index = 1

        # while the hyperbox is not impure and there are points to examinate
        while not is_impure and point_index < len(self.points):

            # check if the label of the examinated point is different
            # from the fixed one, if so, set is_impure to True
            if self.points[point_index].get_label() != point_label:
                is_impure = True

            # increment point index
            point_index = point_index + 1

        return is_impure
