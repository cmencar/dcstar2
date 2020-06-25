from cut_sequences.hyperbox import Hyperbox

# Class for define set of hyperboxes
class HyperboxesSet:

    # class constructor
    # @points: prototypes point list
    # @cuts: selected cuts sequences used to calculate HyperboxesSet
    def __init__(self, points, cuts):

        # initialization of dictionary of points
        self.__points = dict()

        # initialization of selected cuts sequences on which hyperboxes_set is based
        self.__selected_cuts_sequences = cuts

        # initialization of hyperboxes
        self.__set_hyperboxes(points)


    # Method for defining all hyperboxes in hyperboxes set
    # @points: points list passed to constructor
    def __set_hyperboxes(self, points):

        # for each point in passed points list, create its hyperbox.
        # If there is already a point that use an hyperbox defined with
        # the created hyperbox boundaries then use that hyperbox for the point
        for point in points:

            hyperbox_boundaries = self.__set_hyperbox_by_point(point)
            hyperbox = Hyperbox(hyperbox_boundaries)

            for point_key, hb in self.__points.items():
                if hb.get_boundaries() == hyperbox_boundaries:
                    hyperbox = hb

            hyperbox.set_belonging_point(point)
            self.__points.__setitem__(point, hyperbox)


    # Method for defining particular hyperbox starting by point
    # @point: point associated with the hyperbox to find
    def __set_hyperbox_by_point(self, point):

        # initializing point coordinate dimension's index
        dimension_index = 0

        # definition of hyperbox's boundaries
        hyperbox_boundaries = list()

        # for each S_d in selected cuts sequences
        for S_d in self.__selected_cuts_sequences:

            # initializing found flag and
            # dimension cut's index
            found = False
            cut_index = 0

            # get the evaluated point coordinate
            coordinate = point.get_coordinate(dimension_index)

            # while the smallest cut with greater value than
            # point coordinate is not found
            while found is False and cut_index <= len(S_d):

                # get the evaluated cut
                cut = S_d[cut_index]


                # if cut value is greater than point coordinate value then insert that cut and previous cut in the
                # dimensional order as one of hyperbox dimensional boundaries. Instead, if cut value is equal to the
                # point coordinate value then insert that cut and following cut in the dimensional order as one of
                # hyperbox dimensional boundaries
                if coordinate <= cut:
                    if cut_index == 0:
                        hyperbox_boundaries.append((cut, S_d[cut_index + 1]))
                    else:
                        hyperbox_boundaries.append((S_d[cut_index - 1], cut))

                    found = True

                # increment cut index
                cut_index = cut_index + 1

            # increment point coordinate dimension index
            dimension_index = dimension_index + 1

        return tuple(hyperbox_boundaries)


    # Method for counting hyperboxes
    def get_hyperboxes_number(self):
        return len({hyperbox for point, hyperbox in self.__points.items()})


    # Method for counting pure hyperboxes
    def get_pure_hyperboxes_number(self):
        return len({hyperbox for point, hyperbox in self.__points.items() if not hyperbox.is_impure()})


    # Method for counting impure hyperboxes
    def get_impure_hyperboxes_number(self):
        return len({hyperbox for point, hyperbox in self.__points.items() if hyperbox.is_impure()})


    # Method for acquiring all hyperboxes as a list.
    # The hyperboxes are taken once and only once, regardless of
    # occurences as attributes in the dictionary of points
    def get_hyperboxes(self):
        return list({hyperbox for point, hyperbox in self.__points.items()})


