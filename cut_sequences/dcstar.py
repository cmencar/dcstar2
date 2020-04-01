from cut_sequences.cuts_sequence import CutsSequence
from cut_sequences.selected_cuts_sequence import SelectedCutsSequence
from heuristic_search.pqueue import PriorityQueue
import sys


class DCStarNode:

    def __init__(self, binary_sequence, cost):
        self.state = binary_sequence
        self.cost = cost

    def get_state(self):
        return self.state

    def get_cost(self):
        return self.cost

    def set_cost(self, cost):
        self.cost = cost

    def successors(self):
        return [ DCStarNode(successor, 0) for successor in self.state.get_successors() ]

    def __lt__(self, node):
        return self.cost < node.get_cost()

    def __gt__(self, node):
        return self.cost > node.get_cost()

    def __eq__(self, node):
        return self.cost == node.get_cost()



class DCStar:

    def __init__(self, points_list, m_d = 0, M_d = 1):

        self.points_list = points_list

        self.T_d = self.__create_T_d(self.points_list)

        self.T_d_cuts_number = 0
        for dimension_index in range(self.T_d.get_dimensions_number()):
            self.T_d_cuts_number += self.T_d.get_dimension_size(dimension_index)

        self.closed = PriorityQueue()
        self.open = PriorityQueue()

        self.boundary_points = (m_d, M_d)


    def find(self, in_debug = False):

        #most_promising_node = None

        #start_node = DCStarNode(binary_sequence = self.T_d.generate_starting_binary(), cost = 0)
        most_promising_node = DCStarNode(binary_sequence = self.T_d.generate_starting_binary(), cost = (0, 0, 0))

        #self.open.put(start_node)
        self.open.put(most_promising_node)

        branches_taken = 0

        while self.open.empty() is False:

            most_promising_node = self.open.get()

            self.open.remove(most_promising_node)

            self.closed.put(most_promising_node)

            branches_taken += 1

            if in_debug:

                sys.stdout.write('\r' + "Evaluating node #" + str(branches_taken))

            if self.__goal(most_promising_node):

                return most_promising_node.get_state(), branches_taken

            else:
                successors = self.__successors(most_promising_node)

                for successor in successors:

                    if self.closed.find(successor) is None and self.open.find(successor) is None:

                        first_level_priority = self.__get_first_level_priority(successor)
                        second_level_priority = self.__get_second_level_priority(successor, most_promising_node)
                        third_level_priority = self.__get_third_level_priority(successor)

                        successor.set_cost((first_level_priority, second_level_priority, third_level_priority))

                        self.open.put(successor)


        return most_promising_node.get_state(), branches_taken


    #
    def __g(self, node):
        cuts_number = 0

        for dimension_index in range(node.get_state().get_dimensions_number()):
            for cut in node.get_state().get_dimension(dimension_index):
                if cut:
                    cuts_number += 1

        return cuts_number


    #
    def __h(self, node):

        S_d = SelectedCutsSequence()
        S_d.from_binary(self.T_d, node.get_state())

        hyperboxes_set = S_d.generate_hyperboxes_set(self.points_list, m_d = self.boundary_points[0], M_d = self.boundary_points[1])
        hyperboxes = [hyperbox for hyperbox in hyperboxes_set.get_hyperboxes() if hyperbox.is_impure()]

        heuristic_value = 0

        while len(hyperboxes) > 0:
            worst_hb = hyperboxes[0]

            for hb in hyperboxes:
                if hb.get_different_classes_number() > worst_hb.get_different_classes_number():
                    worst_hb = hb

            heuristic_value = heuristic_value + worst_hb.get_different_classes_number()

            newly_created_hyperboxes = list()

            for hb in hyperboxes:
                if worst_hb.is_connected(hb) is False:
                    newly_created_hyperboxes.append(hb)

            hyperboxes = newly_created_hyperboxes

        return heuristic_value


    #
    def __goal(self, node):

        S_d = SelectedCutsSequence()
        S_d.from_binary(self.T_d, node.get_state())

        hyperboxes_set = S_d.generate_hyperboxes_set(self.points_list)

        return True if hyperboxes_set.get_impure_hyperboxes_number() == 0 else False


    #
    def __successors(self, node):
        return node.successors()


    #
    def __create_T_d(self, points_list):

        n_dimensions = len(points_list[0].get_coordinates())
        res = list()

        for dimension_index in range(n_dimensions):

            projections_on_d = dict()
            projections_in_d_list = list()
            cuts_in_d = list()

            sorted_point_list = sorted(points_list, key= lambda point: point.get_coordinate(dimension_index) )

            for point in sorted_point_list:
                if projections_on_d.get(point.get_coordinate(dimension_index)) is None:
                    projections_on_d.__setitem__(point.get_coordinate(dimension_index), [point.get_label()])
                else:
                    projections_on_d.get(point.get_coordinate(dimension_index)).append(point.get_label())


            for point_coordinate, point_classes in projections_on_d.items():
                projections_in_d_list.append((point_coordinate, set(point_classes)))

            projections_in_d_list = sorted(projections_in_d_list)

            for projection_idx in range(len(projections_in_d_list) - 1):

                if projections_in_d_list[projection_idx][1] != projections_in_d_list[projection_idx + 1][1] or len(projections_in_d_list[projection_idx][1]) > 1:
                    cuts_in_d.append((projections_in_d_list[projection_idx][0] + projections_in_d_list[projection_idx + 1][0])/2)

            res.append(cuts_in_d)

        return CutsSequence(res)


    #
    def get_T_d(self):
        return self.T_d


    def __get_first_level_priority(self, node):
        return self.__g(node) + self.__h(node)


    def __get_second_level_priority(self, successor, node):

        node_state = node.get_state()
        successor_state = successor.get_state()

        cut_indexes = None

        looping = True
        dimension_index = 0

        while looping:

            if dimension_index == node_state.get_dimensions_number():
                looping = False
            else:

                cut_index = 0
                while looping and cut_index < node_state.get_dimension_size(dimension_index):

                    if node_state.get_cut(dimension_index, cut_index) != successor_state.get_cut(dimension_index, cut_index):

                        cut_indexes = (dimension_index, cut_index)
                        looping = False

                    cut_index += 1

            dimension_index += 1

        i = cut_indexes[1]
        t_k_minus_1 = None
        while i > 0 and t_k_minus_1 is None:
            if not successor_state.get_cut(cut_indexes[0], i):
                t_k_minus_1 = self.T_d.get_dimension(cut_indexes[0])[i]
            else:
                i -= 1

        i = cut_indexes[1]
        t_k_plus_1 = None
        while i < self.T_d.get_dimension_size(cut_indexes[0]) and t_k_plus_1 is None:
            if not successor_state.get_cut(cut_indexes[0], i):
                t_k_plus_1 = self.T_d.get_dimension(cut_indexes[0])[i]
            else:
                i += 1

        if t_k_minus_1 is None:
            t_k_minus_1 = self.boundary_points[0]
        if t_k_plus_1 is None:
            t_k_plus_1 = self.boundary_points[1]

        t_k = self.T_d.get_dimension(cut_indexes[0])[cut_indexes[1]]
        return min(t_k - t_k_minus_1, t_k_plus_1 - t_k)


    #
    def __get_third_level_priority(self, node):

        value = 0

        node_state = node.get_state()

        for dimension_index in range(node_state.get_dimensions_number()):
            if node_state.get_dimension_size(dimension_index) > 0:
                value += 1

        return -value
