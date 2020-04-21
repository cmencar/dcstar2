
# Class for defining a single hyperbox using
# a particular set of intervals
class Hyperbox:

    # Class constructor. Needs set of intervals
    # made by tuple of tuples
    # @hyperbox_tuple: set of intervals
    def __init__(self, hyperbox_boundaries):

        # initializing boundaries and points structure
        self.__points = list()

        # acquire every dimensional boundaries, insert them in a list
        # (as a list of tuples) and convert the list into a tuple
        self.__boundaries = tuple([tuple(S_d_boundaries) for S_d_boundaries in hyperbox_boundaries])


    # Method for acquiring hyperbox boundaries for each dimension
    def get_boundaries(self):
        return self.__boundaries


    # Method for setting belonging point of hyperbox
    # @point_list: single points, part of hyperbox
    def set_belonging_point(self, point):
        self.__points.append(point)


    # Method for acquiring belonging points of hyperbox
    def get_belonging_points(self):
        return self.__points


    # Method for checking if the hyperbox is impure
    def is_impure(self):

        # initialization of service variables
        point_label = self.__points[0].get_label()
        point_index = 1

        # while the hyperbox is not impure and there are points to examinate
        while point_index < len(self.__points):

            # check if the label of the examinated point is different
            # from the fixed one, if so, set is_impure to True
            if self.__points[point_index].get_label() != point_label:
                return True

            # increment point index
            point_index = point_index + 1

        return False


    # Method for acquiring the number of different prototypes
    # classes present in the hyperbox
    def get_different_classes_number(self):
        return len({point.get_label() for point in self.__points})


    # Method for acquiring if the passed hyperbox and this hyperbox
    # are 'connected'. The term 'connected' refers to the fact that
    # the two hb have at least one pair of boundaries in common
    # @hyperbox: element that is needed to evaluate for the connection
    def is_connected(self, hyperbox):

        # if at least one pair of boundary (defined as a tuple of two elements,
        # left boundary and right boundary) is the same for both this hyperbox and
        # passed hyperbox boundaries, it means that they are 'connected', so the
        # method returns True. If no pair of boundaries are found in common,
        # then they are not 'connected' and the method returns False
        for dimension, passed_hyperbox_dimension in zip(self.__boundaries, hyperbox.get_boundaries()):
            if dimension == passed_hyperbox_dimension:
                return True

        return False
