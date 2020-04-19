from cut_sequences.dimensional_sequence_numeric import DimensionalSequenceNumeric
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
from heuristic_search.pqueue import PriorityQueue
from heuristic_search.astar_node import AStarNode
from genetic_algorithm.deap_genetic_guide import DeapGeneticGuide
import numpy as np
import sys
import time


# Class defining the DC* clustering method
class AStar:

    # Class constructor
    # @points_list: prototype point list to be used to find the
    #  cuts sequence for the clustering
    # @m_d: smallest boundary cut of dimension d
    # @M_d: greatest boundary cut of dimension d
    def __init__(self, points_list, m_d=0, M_d=1):

        # initialization of point list
        self.__points_list = points_list

        # creation of cuts sequences using the points list
        self.__cuts_sequences = self.__create_cuts_sequences()

        # initialization of boundaries of extended cuts sequences
        self.__boundary_points = (m_d, M_d)

        # initialization of priority queues: the closed queue,
        # dedicated to nodes already evaluated, and the x, dedicated
        # to all nodes to be evaluated
        self.__closed_queue = PriorityQueue()
        self.__open_queue = PriorityQueue()

        # calculate the size of each dimension of cuts sequence
        self.genes_per_dimension = list()
        for dimension in range(self.__cuts_sequences.get_dimensions_number()):
            self.genes_per_dimension.append(len(self.__cuts_sequences.get_dimension(dimension)))

        # calculate the total number of genes that the genome will have
        self.genes_number = 0
        for num in self.genes_per_dimension:
            self.genes_number += num

        # set number of individuals for tournament selection
        self.selected_for_tournament = 5

        # calculate population
        # N.B.: population is given by duplicating the number of genes in the genome
        self.population_size = 2 * self.genes_number

        # set number of generations
        self.generations = 20

        # calculate mutation rate
        # N.B.: mutation rate is calculated by reciprocating the number of genes
        self.mutation_rate = 1 / self.genes_number

        # set mating rate
        self.mating_rate = 0.7

        # set number of best individuals to choose from
        self.selected_best = 10

        # define DGG object to create the genetic guide with monodimensional lists
        self.genetic_guide = DeapGeneticGuide(self.genes_number, self.mutation_rate, self.mating_rate,
                                              self.selected_for_tournament, self.__cuts_sequences, self.__points_list,
                                              self.genes_per_dimension, self.__boundary_points[0],
                                              self.__boundary_points[1])

        # evolution and acquisition of the best individual from genetic guide with monodimensional lists (wsc)
        self.best_pure_individual, self.worst = self.genetic_guide.evolve(self.population_size, self.generations,
                                                                          self.selected_best)

        # evolution and acquisition of the best individual from genetic guide with monodimensional lists (without wsc)
        self.best_individual = self.genetic_guide.evolve_without_wsc(self.population_size, self.generations,
                                                                     self.selected_best)

    # Method for acquiring the partition of Universe of Discours
    # given a list of prototype points into an n-dimensional space
    # @verbose: flag for the setting of a verbose computation
    def find(self, verbose=False):

        # initialization of timer (used to measure the time
        # taken in the computation)
        start_time = time.time()

        # defining a initial most_promising_node. Initially, this
        # node will be equal to a binary cuts sequence where all cuts
        # are defined as False and the cost is equal to a tuple
        # containing three values equal to 0
        most_promising_node = AStarNode(state=self.__cuts_sequences.generate_starting_binary(), cost=(0, 0, 0))

        # inserting the initial most_promising_node into the open_queue
        self.__open_queue.put(most_promising_node)

        # initialize the counter for the evaluated nodes
        nodes_evaluated = 0

        # while in the open_queue there will still be nodes
        # to evaluate, you acquire the most promising node from
        # the open_queue itself and calculate the various cost levels
        while self.__open_queue.empty() is False:

            # acquiring the most promising node from the open_queue,
            # removing it from the same queue and inserting it in
            # the closed_queue
            most_promising_node = self.__open_queue.get()
            self.__open_queue.remove(most_promising_node)
            self.__closed_queue.put(most_promising_node)

            # incrementing the counter of nodes evaluated
            nodes_evaluated += 1

            # depending if the verbose mode is chosen, the correct
            # on-screen printing is shown
            if verbose:
                sys.stdout.write('\r' + "Evaluating node #" + str(nodes_evaluated))
            else:
                sys.stdout.write('\r' + "Evaluating" + str('.' * (nodes_evaluated % 5)))

            # if the most_promising_node is one of possible solution (the calculation
            # is defined through the goal function where is evaluated if the
            # node's cuts sequence returns only impure hyperboxes) then it returns
            # that node as the result of clustering. In addition to the cuts sequence,
            # defined through a SelectedDimensionalSequenceNumeric object, other values
            # are returned such as the number of nodes evaluated and the time
            # taken for the computation
            if self.__goal(most_promising_node):
                return most_promising_node.get_state(), nodes_evaluated, time.time() - start_time

            else:

                # if the most_promising_node is not a possible solution (so the
                # goal function returned False) then a list of successors is created
                # (through the successors operator). A successor to the
                # most_promising_node is a node that has all logical cuts sequence values
                # equal to those of the most_promising_node except one. The element that
                # differs between the successor and the most_promising_node is a cut, whose
                # value is converted from False to True.
                for successor in self.__successors(most_promising_node):

                    # a particular cost is assigned to the successor. The cost is
                    # composed of three different values:
                    #  - the first value (first-level priority) is based on the sum of
                    #    path-cost value and heuristics (first and second level)
                    #  - the second value (second-level priority) is based on the minimum
                    #    number of cuts to add so that the solution returns only pure hyperboxes
                    # - the third value (thrid-level priority) is based on the number
                    #    of features (dimensions) that are used to define the
                    #    cuts sequence of the successor
                    # NOTE: the first two levels are more valuable within research because
                    # they are more discriminatory. The third level is only used when
                    # the first two levels are equal.
                    first_level_priority = self.__get_first_level_priority(successor)
                    second_level_priority = self.__get_second_level_priority(successor, most_promising_node)
                    third_level_priority = self.__get_third_level_priority(successor)
                    successor.set_cost((first_level_priority, second_level_priority, third_level_priority))

                    # the created successor is inserted into the open_queue
                    # and will be evaluated later on the basis of its cost (obviously based
                    # on the three levels of priority)
                    self.__open_queue.put(successor)

        # if there is no intermediate solution, i.e. a solution that
        # does not imply the use of all the cuts defined by cuts sequences
        # (and, therefore, form a set of minimal hypercubes) then the solution
        # will be the last most_promising_node, i.e. the one whose cuts
        # sequence is associated with the binary cuts sequence with
        # all the values set to True.
        return most_promising_node.get_state(), nodes_evaluated, time.time() - start_time

    # Method for acquiring if the node is a result of
    # clustering process. Is based on the fact that each hyperbox
    # produced by the passed binary cuts sequence is pure,
    # i.e. it contains a set of prototypes belonging to the same class
    # @node: node of to be evaluated to get the second-level priority
    def __goal(self, node):

        # create a selected cuts sequence using the binary sequence of passed node
        selected_cuts_sequences = SelectedDimensionalSequenceNumeric()
        selected_cuts_sequences.from_binary(self.__cuts_sequences, node.get_state())

        # generate an HyperboxesSet object from the newly created selected
        # cuts sequence and using the prototype points list
        hyperboxes_set = selected_cuts_sequences.generate_hyperboxes_set(self.__points_list,
                                                                         m_d=self.__boundary_points[0],
                                                                         M_d=self.__boundary_points[1])

        # the return value will be True if the HyperboxesSet object
        # contain only pure hyperboxes, False otherwise
        return True if hyperboxes_set.get_impure_hyperboxes_number() == 0 else False

    # Method for acquiring the successors of node
    # @node: node from which to extrapolate successors
    def __successors(self, node):
        return node.successors()

    # Method for creating a cuts sequence starting from
    # a list of prototype points.
    # @points_list: list of prototype points
    def __create_cuts_sequences(self):

        # initializes an empty list in order to contain the
        # sequence of T_d cuts that will later be used
        # to create the DimensionalSequenceNumeric object
        numerical_cuts_sequence = list()

        # for each possible dimension, indirectly defined
        # by the number of coordinates of any point
        for dimension_index in range(len(self.__points_list[0].get_coordinates())):

            # sorts the list of points based on the coordinate
            # value on the dimension identified by dimension_index
            sorted_point_list = sorted(self.__points_list, key=lambda point: point.get_coordinate(dimension_index))

            # for each point a projection of the same is determined on the
            # dimension defined by dimension_index. The value of the projection
            # is equivalent to the coordinate of the point on the dimension
            # evaluated. in case two or more points share the same projection
            # there will be two cases: if they are part of the same class, then
            # the class they belong to will be stored only once, if they are part
            # of different classes, then more information about the classes
            # will be stored, so that the information is not lost.
            # projection_on_d will be defined, therefore, as a dictionary where
            # the key is the numerical value of the projection on d while
            # the attribute is the set of classes of the prototypes projected on d
            projections_on_d = dict()
            for point in sorted_point_list:
                if projections_on_d.get(point.get_coordinate(dimension_index)) is None:
                    projections_on_d.__setitem__(point.get_coordinate(dimension_index), {point.get_label()})
                else:
                    projections_on_d.get(point.get_coordinate(dimension_index)).add(point.get_label())

            # dimensional projections must be ordered so that they make sense
            # when defining cuts. In this regard, a list is first defined
            # containing as elements the pair 'projection value'-'set of classes'
            # and, subsequently, it is sorted according to the projection value
            sorted_projections_on_d = sorted([(point_coordinate, set(point_classes))
                                              for point_coordinate, point_classes in projections_on_d.items()])

            # for each pair of projections defined by sorted_projections_on_d
            # a cut must be determined. The cut is only defined if the projections
            # belong to two different classes. In this way, the set of classes of
            # the evaluated projection must either be different from the next projection
            # in the order in sorted_projections_on_d or it must contain more than
            # one class (since it has at least two different classes, at least one
            # of the two is different).
            cuts_in_d = [(sorted_projections_on_d[projection_idx][0] + sorted_projections_on_d[projection_idx + 1][0])/2
                         for projection_idx in range(len(sorted_projections_on_d) - 1)
                         if sorted_projections_on_d[projection_idx][1] != sorted_projections_on_d[projection_idx + 1][1]
                         or len(sorted_projections_on_d[projection_idx][1]) > 1]

            # once a valid cuts sequence for the dimension is defined, it is
            # inserted in the global cuts sequence
            numerical_cuts_sequence.append(cuts_in_d)

        # using the global cuts sequence, a DimensionalSequenceNumeric object
        # is created and passed as return value
        return DimensionalSequenceNumeric(numerical_cuts_sequence)

    # Method for acquiring the value of cuts sequences
    def get_cuts_sequences(self):
        return self.__cuts_sequences

    # Method for acquiring the value of first-level priority
    # for the successor node. The first-level priority is a value
    # based on the sum of cost value and heuristic value.
    # @node: node of to be evaluated to get the first-level priority
    def __get_first_level_priority(self, node):
        return self.__get_path_cost_value(node) + self.__get_heuristic_value(node)

    # Method for acquiring the value of second-level priority
    # for the successor node. The second-level priority is a
    # value based on the thickness of a space that is defined using
    # the newly added cut: greater the value, greater the information granule
    # defined by the distance (so that smaller the distance between left and right
    # cuts of newly inserted cut, smaller is the priority value)
    # @successor: node of to be evaluated to get the second-level priority
    # @node: node of which 'successor' is the successor
    def __get_second_level_priority(self, successor, node):

        # definition of two binary sequences taken from a node
        # and from its evaluated successor node
        successor_state = successor.get_state()
        node_state = node.get_state()

        # initialization of indexes for defining the specific cut
        # to be taken to evaluate the section space
        cut_index = 0
        dimension_index = 0

        # initialization of flag for the found cut
        found = False

        # while the cut is not found, search in the logical sequence
        # the newly added cut
        while not found:

            # if there is a pair of cut (one from node_state, one from successor_state)
            # that are not equal each other, then the newly added cut into successor node
            # is found. Therefore, set the found flag to true and don't change the indexes
            # value. On the other hand, if the newly added cut is not found in successor_state,
            # then increment the cut_index and dimension_index
            if node_state.get_cut(dimension_index, cut_index) != successor_state.get_cut(dimension_index, cut_index) or \
                    dimension_index == node_state.get_dimensions_number():
                found = True
            else:
                cut_index = (cut_index + 1) % node_state.get_dimension_size(dimension_index)
                if cut_index == 0:
                    dimension_index += 1

        # initialization of newly added cut (t_k), the previous cut
        # (t_k_previous) and the next cut (t_k_next). The first value
        # set to t_k_previous and t_k_next are, respectively, the values
        # of m_d and M_d
        t_k = self.__cuts_sequences.get_dimension(dimension_index)[cut_index]
        t_k_previous = self.__boundary_points[0]
        t_k_next = self.__boundary_points[1]

        # reset the found flag
        found = False

        # initialize the successor_state scanning index to cut_index
        # and search into the binary sequence until the index reaches 0
        # or an element is found. An element is found (so a valid value
        # for t_k_previous) when a logical cut value is True: using the
        # value defined by index, the numerical value of cut is taken and
        # it is assigned to t_k_previous
        index = cut_index - 1
        while index > 0 and not found:
            if successor_state.get_cut(dimension_index, index):
                t_k_previous = self.__cuts_sequences.get_dimension(dimension_index)[index]
                found = True
            index -= 1

        # reset the found flag
        found = False

        # initialize the successor_state scanning index to cut_index
        # and search into the binary sequence until the index reaches the
        # last value of dimension (to which dimension_index refers)
        # or an element is found. An element is found (so a valid value
        # for t_k_next) when a logical cut value is True: using the
        # value defined by index, the numerical value of cut is taken and
        # it is assigned to t_k_next
        index = cut_index + 1
        while index < self.__cuts_sequences.get_dimension_size(dimension_index) and not found:
            if successor_state.get_cut(dimension_index, index):
                t_k_next = self.__cuts_sequences.get_dimension(dimension_index)[index]
                found = True
            index += 1

        # the returned value is the minimum between two elements: the distance
        # between t_k and t_k_previous and the distance between t_k_next and t_k
        return min(t_k - t_k_previous, t_k_next - t_k)

    # Method for acquiring the value of third-level priority
    # for the successor node. The third-level priority is a
    # value based on the number of different feature used
    # for defining an hyperboxes. It is the number of dimensions
    # (features) in the binary cuts sequence that contain at least one cut.
    # The value is subsequently negated, so that more emphasis is placed on
    # sequences with fewer dimensions used (the more dimensions with at least
    # one cut are presents, the lower the priority).
    # @node: node of to be evaluated to get the third-level priority
    def __get_third_level_priority(self, node):

        # for every dimension in the successor node, if it has at least
        # one cut, then the counter is decreased by one unit
        value = 0
        for dimension_index in range(node.get_state().get_dimensions_number()):
            if node.get_state().get_dimension_size(dimension_index) > 0:
                value -= 1
        return value

    # Method for acquiring the g path-cost value. It is based on the counting
    # the cuts present in the logical sequence which value is True
    # @node: node of to be evaluated to get the path-cost value
    def __get_path_cost_value(self, node):
        return sum([np.sum(node.get_state().get_dimension(dimension_index) == True)
                    for dimension_index in range(node.get_state().get_dimensions_number())])

    # Method for acquiring the heuristic value. It is based on the
    # sum of first-level and second-level heuristic values
    # @node: node of to be evaluated to get the second-level heuristic
    def __get_heuristic_value(self, node):
        return self.__get_first_level_heuristic_value(node) + self.__get_second_level_heuristic_value(node)

    # Method for acquiring the first-level heuristic value. It is based
    # on the minimum value of cuts to be defined so that all hyperboxes
    # defined by node are pure. It iterates over the impure hyperboxes,
    # starting from the one with the maximum number of different class labels.
    # Once an hyperbox is selected, the heuristic value is summed to a
    # counter and all connected hyper-boxes are removed (two or more hyperboxes
    # are connected if they have in common at least a couple of cuts, named boundaries).
    # The procedure stops when the collection of hyperboxes to scan is empty
    # and, finally, the value of the counter is returned.
    # @node: node of to be evaluated to get the heuristic value
    def __get_first_level_heuristic_value(self, node):

        # create a selected cuts sequence using the binary sequence of passed node
        selected_cuts_sequences = SelectedDimensionalSequenceNumeric()
        selected_cuts_sequences.from_binary(self.__cuts_sequences, node.get_state())

        # generate an HyperboxesSet object from the newly created selected
        # cuts sequence and using the prototype points list
        hyperboxes_set = selected_cuts_sequences.generate_hyperboxes_set(self.__points_list,
                                                                         m_d=self.__boundary_points[0],
                                                                         M_d=self.__boundary_points[1])

        # all impure hyperboxes are captured by the HyperboxesSet object
        # and placed in a list. On them will be based the evaluation
        # of the value of the first level heuristics
        hyperboxes = [hyperbox for hyperbox in hyperboxes_set.get_hyperboxes() if hyperbox.is_impure()]

        # initializing the heuristic value to 0. Later, until the list
        # of impure hyperboxes is not empty, heuristic_Value is incremented
        # using the remaining hyperboxes
        # NOTE: the name most_impure_hyperboxes refers to the hyperbox
        # with the largest number of different classes within it, obviously
        # the name given is only used to better render the idea and probably
        # not to be considered a scientifically valid term
        heuristic_value = 0
        while len(hyperboxes) > 0:

            # acquiring the first hyperbox in the impure hyperboxes list
            # (is not necessarily the 'worst').
            most_impure_hyperboxes = hyperboxes[0]

            # for each hyperbox is evaluated if it is 'worse' than
            # most_impure_hyperbox, i.e. if it has more prototypes of
            # different classes. If so, then the evaluated hyperbox
            # becomes the most_impure_hyperbox
            for hyperbox in hyperboxes:
                if hyperbox.get_different_classes_number() > most_impure_hyperboxes.get_different_classes_number():
                    most_impure_hyperboxes = hyperbox

            # heuristic_value is increased by adding the already
            # existing value with the number of prototypes with
            # different classes in the most_impure_hyperbox. Subsequently,
            # each hyperbox connected to the most_impure_hyperbox
            # (thus also the most_impure_hyperbox itself) is deleted from
            # the list and the evaluation of the remaining hyperboxes continue
            heuristic_value = heuristic_value + most_impure_hyperboxes.get_different_classes_number()
            hyperboxes = [hyperbox for hyperbox in hyperboxes if most_impure_hyperboxes.is_connected(hyperbox) is False]

        # finally, the heuristic_value calculated is passed as return value
        return heuristic_value

    # Method for acquiring the second-level heuristic value
    # It is based on
    # TODO(TO BE CONTINUED)
    # @node: node of to be evaluated to get the second-level heuristic
    def __get_second_level_heuristic_value(self, node):
        return 1
