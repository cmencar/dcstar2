from cut_sequences.hyperbox import Hyperbox

# Class for define set of hyperboxes B
class HyperboxesSet:

    # class constructor
    def __init__(self, points, cuts):

        # inizialization of hyperboxes set
        self.hyperboxes = dict()

        # initialization of list of points
        self.points_list = points

        # initialization of S_d cuts
        # which is based on hyperboxes_set
        self.dimensions_cuts = cuts

        # for each point in passed points list, if that point
        # is part of an existing hyperbox then insert it as
        # one of its belonging points. If that point is not part
        # of an existing hyperbox then create a new hyperbox
        # and insert that point into its belonging points.
        for point in self.points_list:

            if self.hyperboxes.get(self.set_hyperbox_by_point(point)):
                self.hyperboxes.get(self.set_hyperbox_by_point(point)).set_belonging_point(point)

            else:
                hyperbox = Hyperbox(self.set_hyperbox_by_point(point))
                hyperbox.set_belonging_point(point)
                self.hyperboxes.__setitem__(hyperbox.get_boundaries(), hyperbox)


    # Method for defining particular hyperbox starting by point
    # @point: point associated with the hyperbox to find
    def set_hyperbox_by_point(self, point):

        # initializing point coordinate dimension's index
        dimension_index = 1

        # definition of hyperbox's boundaries
        hyperbox_boundaries = list()

        # for each dimension in passed S_d
        for dimension in self.dimensions_cuts:

            # initializing found flag and
            # dimension cut's index
            found = False
            cut_index = 0

            # get the evaluated point coordinate
            coordinate = point.get_coordinate(dimension_index)

            # while the smallest cut with greater value than
            # point coordinate is not found
            while found is False and cut_index <= len(dimension):

                # get the evaluated cut
                cut = dimension[cut_index]

                # if cut value is greater than point coordinate value
                # then insert that cut and previous cut in the
                # dimensional order as one of hyperbox dimensional boundaries
                if coordinate <= cut:
                    hyperbox_boundaries.append((dimension[cut_index-1], cut))
                    found = True

                # increment cut index
                cut_index = cut_index + 1

            # increment point coordinate dimension index
            dimension_index = dimension_index + 1

        return tuple(hyperbox_boundaries)


    # Method for acquiring particular hyperbox starting by point
    # @point: point associated with the hyperbox to find
    def get_hyperbox_by_point(self, point):

        hb_key = self.set_hyperbox_by_point(point)
        return self.hyperboxes.get(hb_key)


    # Method for checking if a given hyperbox is impure
    # @hyperbox: given hyperbox
    def is_impure_hyperbox(self, hyperbox):
        hb = self.hyperboxes.get(hyperbox.value)
        return hb.is_impure()


    # Method for counting impure hyperboxes
    def get_impure_hyperboxes_number(self):

        # initialization of number of impures
        num = 0

        # for each couple (key and corresponding hyperbox)
        for key, hb in self.hyperboxes.items():

            # check if given hyperbox is impure
            if hb.is_impure():
                num = num + 1

        return num


    # Method for acquiring all impure hyperboxes
    def get_impure_hyperboxes(self):

        # initialization impures list
        impure_hbs = list()

        # for each couple (key and corresponding hyperbox)
        for key, hb in self.hyperboxes.items():

            # check if given hyperbox is impure, if so, add it to impure list
            if hb.is_impure() is True:
                impure_hbs.append(hb)

        return impure_hbs
