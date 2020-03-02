import itertools as itool


# Class for defining the node for the hyperboxes' search graph
class HyperboxSearchGraphNode:

    # Class constructor
    # @value: value related to node
    def __init__(self, value):
        self.value = value
        self.adiacents = list()


    # Method for insert a new adiacent node
    # @adiacent: node to be added
    def add_adiacent(self, adiacent):
        self.adiacents.append(adiacent)


    # Method for acquire adiacents nodes
    def get_adiacents(self):
        return self.adiacents


    # Method for set node value
    # @value: value related to node
    def set_value(self, value):
        self.value = value


    # Method for acquire node value
    def get_value(self):
        return self.value



# Class for defining a single hyperbox using
# a particular set of intervals
class Hyperbox:

    # Class constructor. Needs set of intervals
    # made by tuple of tuples
    # @hyperbox_tuple: set of intervals
    def __init__(self, hyperbox_tuple):

        # initializing boundaries and points structure
        self.boundaries = tuple()
        self.points = list()

        # if passed hyperbox is a tuple of tuples then
        # append it into hyperboxes set, else raise an
        # error based on passed wrong type
        if isinstance(hyperbox_tuple, tuple):
            self.boundaries = hyperbox_tuple
        else:
            raise TypeError("Impossible to create hyperbox. Passed a non tuple parameter")


    # Method for acquiring hyperbox boundaries for each dimension
    def get_boundaries(self):
        return self.boundaries


    # Method for setting belonging points of hyperbox
    # @point_list: list of all points into space
    def set_belonging_points(self, point_list):

        # defining dimensions number
        dimensions = len(self.boundaries)

        # for each point into point_list
        for point in point_list:

            dimension_index = 0
            belonging = True

            while dimension_index < dimensions and belonging:
                if self.boundaries[dimension_index][0] <= point.get_coordinate(dimension_index + 1) <= self.boundaries[dimension_index][1]:
                    dimension_index = dimension_index + 1
                else:
                    belonging = False

            if belonging:
                self.points.append(point)


    # Method for acquiring belonging points of hyperbox
    def get_belonging_points(self):
        return self.points


    # Method for checking if a given point is in the hyperbox
    def has_point(self, point):
        return [True if point in self.points else False]


    # Method for checking if the hyperbox is impure
    def is_impure(self):

        # initialization of service variables
        is_impure = False
        point_label = None
        point_index = 0

        # while the hyperbox is not impure and there are points to examinate
        while not is_impure and point_index < len(self.points):

            # if there isn't a fixed label take the one of the examinated point
            # else check if the label of the examinated point is different
            # from the fixed one, if so, set is_impure to True
            if point_label is None:
                point_label = self.points[point_index].get_label()
            elif self.points[point_index].get_label() != point_label:
                is_impure = True

            # increment point index
            point_index = point_index + 1

        return is_impure



# Class for define set of hyperboxes B
class HyperboxesSet:

    # class constructor
    def __init__(self, points, valid_intervals):

        # inizialization of hyperboxes set
        self.B = dict()

        # initialization of list of points
        self.points_list = points

        self.intervals = valid_intervals

        # defining Cartesian product for creating hyperboxes set
        for cartesian_product in itool.product(*self.intervals):
            hyperbox = Hyperbox(cartesian_product)
            hyperbox.set_belonging_points(self.points_list)
            self.B.__setitem__(hyperbox.get_boundaries(), hyperbox)


    def get_hyperbox_by_point(self, point):

        start = HyperboxSearchGraphNode(None)

        hyperboxes_number = len(self.B)
        in_d = len(self.intervals)
        nodes = list()
        nodes.append(list([start]))

        for i in range(0, in_d):

            dim_int = len(self.intervals[i])
            nodes_dim = list()
            for j in range(0, dim_int):
                nodes_dim.append(HyperboxSearchGraphNode(self.intervals[i][j]))
            nodes.append(nodes_dim)

        i = 0
        j = 1
        while i < in_d and j < in_d + 1:
            for node in nodes[i]:
                for child in nodes[j]:
                    node.add_adiacent(child)
            i = i + 1
            j = j + 1

        evaluated_point = nodes[0][0]
        level = 1
        result = list()
        contatore = 0
        while evaluated_point.get_adiacents():
            adiacents = evaluated_point.get_adiacents()
            n_adiacents = len(adiacents)
            idx = 0
            cicla = True
            while cicla and idx < n_adiacents:
                contatore = contatore + 1
                if adiacents[idx].get_value()[0] <= point.get_coordinate(level) <= adiacents[idx].get_value()[1]:
                    evaluated_point = adiacents[idx]
                    level = level + 1
                    result.append(adiacents[idx].get_value())
                    cicla = False
                else:
                    idx = idx + 1

        print("confronti: ", contatore)
        return self.B.get(tuple(result))

    # Method for checking if a given hyperbox is impure
    # @hyperbox: given hyperbox
    def is_impure_hyperbox(self, hyperbox):
        hb = self.B.get(hyperbox.value)
        return hb.is_impure()


    # Method for counting impure hyperboxes
    def get_impure_hyperboxes_number(self):

        # initialization of number of impures
        num = 0

        # for each couple (key and corresponding hyperbox)
        for key, hb in self.B.items():

            # check if given hyperbox is impure
            if hb.is_impure():
                num = num + 1

        return num


    # Method for acquiring all impure hyperboxes
    def get_impure_hyperboxes(self):

        # initialization impures list
        impure_hbs = list()

        # for each couple (key and corresponding hyperbox)
        for key, hb in self.B.items():

            # check if given hyperbox is impure, if so, add it to impure list
            if hb.is_impure() is True:
                impure_hbs.append(hb)

        return impure_hbs
