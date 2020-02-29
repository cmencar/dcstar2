
import itertools as itool

class Node:

    def __init__(self, value, label = None, ):
        self.value = value
        self.label = label
        self.children = list()

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def get_child(self, order):
        if order < len(self.children):
            return self.children[order]

    def get_childer(self):
        return self.children

    def get_value(self):
        return self.value

    def get_label(self):
        return self.label

    def set_value(self, value):
        self.value = value

    def set_label(self, label):
        self.label = label


class Hyperbox:

    def __init__(self, hyperbox_tuple):

        self.value = tuple()

        self.points = list()

        # if passed hyperbox is a tuple of tuples then
        # append it into hyperboxes set, else raise an
        # error based on passed wrong type
        if isinstance(hyperbox_tuple, tuple):
            self.value = hyperbox_tuple
        else:
            raise TypeError("Impossible to create hyperbox. Passed a non tuple parameter")


    def set_belonging_points(self, point_list):

        dimensions = len(self.value)

        for point in point_list:

            dimension_index = 0
            belonging = True

            while dimension_index < dimensions and belonging:
                if self.value[dimension_index][0] <= point.get_coordinate(dimension_index + 1) <= self.value[dimension_index][1]:
                    dimension_index = dimension_index + 1
                else:
                    belonging = False

            if belonging:
                self.points.append(point)


    def get_belonging_points(self):
        return self.points


    def has_point(self, point):
        return [True if point in self.points else False]


    def is_impure(self):

        is_pure = True
        point_label = None
        point_index = 0

        while is_pure and point_index < len(self.points):
            if point_label is None:
                point_label = self.points[point_index].get_label()
            elif self.points[point_index].get_label() != point_label:
                is_pure = False

        return is_pure



# Class for define set of hyperboxes B
class HyperboxesSet:

    # class constructor
    def __init__(self, points, valid_intervals):

        # inizialization of hyperboxes set
        #self.B = list()
        self.B = dict()

        # initialization of list of points
        self.points_list = points

        self.intervals = valid_intervals

        # defining Cartesian product for creating hyperboxes set
        for cartesian_product in itool.product(*self.intervals):
            hyperbox = Hyperbox(cartesian_product)
            hyperbox.set_belonging_points(self.points_list)
            #self.B.append(hyperbox)
            self.B.__setitem__(hyperbox.value, hyperbox)


    def get_hyperbox_by_point(self, point):

        start = Node((), "Start")

        hyperboxes_number = len(self.B)
        in_d = len(self.intervals)
        nodes = list()
        nodes.append(list([start]))

        for i in range(0, in_d):

            dim_int = len(self.intervals[i])
            nodes_dim = list()
            for j in range(0, dim_int):
                nodes_dim.append(Node(self.intervals[i][j]))
            nodes.append(nodes_dim)

        i = 0
        j = 1
        while i < in_d and j < in_d + 1:
            for node in nodes[i]:
                for child in nodes[j]:
                    node.add_child(child)
            i = i + 1
            j = j + 1

        evaluated_point = nodes[0][0]
        level = 1
        result = list()
        contatore = 0
        while evaluated_point.get_childer():
            adiacents = evaluated_point.get_childer()
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



    def is_impure_hyperbox(self, hyperbox):
        # TODO si potrebbe usare get_hyperbox_by_point per ogni punto in self.points_list e
        #  vedere se ci sono altri punti per tale HB: se ce n'è almeno uno allora è impuro
        #  e la funzione termina (in alternativa se si salva il calcolo della purezza
        #  in insert_hyperboxes allora si può ricorrere semplicemente ad accedere al valore
        #  di purezza dell'HB salvato)
        pass

    def get_impure_hyperboxes_number(self):
        # TODO si passa il numero di HB impuri
        pass

    def get_impure_hyperboxes(self):
        pass
