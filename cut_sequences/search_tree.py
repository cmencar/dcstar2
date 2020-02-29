
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

    def get_value(self):
        return self.value

    def get_label(self):
        return self.label

    def set_value(self, value):
        self.value = value

    def set_label(self, label):
        self.label = label


def create_search_tree(hyperboxes):

    start = Node((), "Start")

    dimensions_number = S_d.get_dimensions_number()

    for dimension_index in range(1, dimensions_number):

        dimension = S_d.get_dimension(dimension_index)

        for i in range(1, S_d.dimension_size(dimension_index)):

            adiacent_node = Node(dimension[i])
            start.add_child(adiacent_node)





class SearchTree:

    def __init__(self):
        self.root = Node(None)

    def get_root(self):
        return self.root


    def padre(self):
        pass

    def is_foglia(self):
        pass

    def primofiglio(self):
        pass

    def is_ultimofratello(self):
        pass

    def succfratello(self):
        pass

    def cancsottoalbero(self):
        pass

    def inssottoalbero(self):
        pass


