from heuristic_search.pqueue import PriorityQueue
from heuristic_search.node import Node
import sys
import time



# Class including A* algorithm
class AStar:

    # Method for the execution of A* algorithm for the clustering problem
    @staticmethod
    def astar(problem):

        # initialization of the evaluated nodes' cuts sequence list
        evaluated_nodes = []

        # initialization of timer (used to measure the time taken in the computation) and number of branches taken
        start_time = time.time()
        branches_taken = 0

        # initialization of priority queues
        closed = PriorityQueue()
        front = PriorityQueue()

        # definition of the starting node for the evaluation and its starting cost. The starting node is now defined
        # as the first estimated node to be evaluated in problem computation
        start_node = Node(problem.start_state)
        estimated_node = ((0, 0, 0), start_node)
        front.put(estimated_node)

        # if the front priority queue is not empty means that are more nodes to be evaluated
        while not front.empty():

            # incrementing the branches taken counter
            branches_taken = branches_taken + 1

            # depending if the verbose mode is chosen, the correct on-screen printing is shown
            if problem.verbose:
                sys.stdout.write('\r' + "Evaluating node #" + str(branches_taken))
            else:
                sys.stdout.write('\r' + "Evaluating" + str('.' * (branches_taken % 5)))

            # acquiring the most promising node from front priority queue, i.e. the node with the best estimated_cost,
            # and initialize the current_state variable with the most promising node state (a DimensionalSequenceBinary object)
            (estimated_cost, current_node) = front.get()
            current_state = current_node.state

            # adding the current evaluated node into the evaluated_node list
            evaluated_nodes.append([repr(current_state.elements), repr(estimated_cost)])

            # if it is not a unique successor then insert the current_node in closed queue. unique_successor means that
            # is impossible to find cycles in the evaluated path: consequently, the paths taken by the A* algorithm
            # are simple paths and, therefore, the macrostructure can be related back to a tree
            if not problem.unique_successors:
                closed.put((estimated_cost, current_node))

            # if the evaluated current_state is a possible result then return it and finish the execution early.
            # The information on current_State as a possible result is given by the goal function, which returns True
            # if the cut sequence defined by the state generates a set of hyperboxes all pure
            if problem.goal(current_state):
                return current_node.state, branches_taken, time.time() - start_time, evaluated_nodes

            # if the evaluated current_State is not a possible result then define the list of successors of the
            # evaluated current_state. Those successors will be evaluated in the next steps.
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
    def __get_second_level_heuristic_value_dummy(self, node):
        return 1

    # Method for acquiring the second-level heuristic value. It is based on Jaccard similarity between the individual
    # generated by AStar and the one generated by DGG.
    # @node: node of to be evaluated to get the second-level heuristic
    def __get_second_level_heuristic_value(self, node):
        intersection_value = 0
        union_value = 0
        for dimension in range(node.get_state().get_dimensions_number()):
            intersection_value += len(
                set(node.get_state().get_dimension(dimension)).intersection(
                    set(self.genetic_guide_individual.get_dimension(dimension))))
            union_value += len(
                set(node.get_state().get_dimension(dimension)).union(
                    set(self.genetic_guide_individual.get_dimension(dimension))))
        return 1 - intersection_value / union_value

    def __generate_gg_individual(self):

        # generate pure genetic sequence using "evolve" method - possible call of "worst_case_scenario"
        # elements = self.genetic_guide.evolve(self.population_size, self.generations, self.selected_best)

        # generate pure genetic sequence using "worst_case_scenario" method directly
        # elements = DeapGeneticGuide.worst_case_scenario(self.genetic_guide, self.genes_per_dimension)

        # generate genetic sequence with correction of impureness when needed
        # '''
        elements = self.genetic_guide.evolve_without_wsc(self.population_size, self.generations, self.selected_best)
        sequence = DimensionalSequenceBinary()
        sequence.from_binary(elements)
        s_d = SelectedDimensionalSequenceNumeric()
        s_d.from_binary(self.__cuts_sequences, sequence)
        hbs = s_d.generate_hyperboxes_set(self.__points_list, self.__boundary_points[0], self.__boundary_points[1])
        if hbs.get_impure_hyperboxes_number() != 0:
            print("Impure DGG sequence generated, purification in process")
            found = False
            successors = sequence.get_successors()
            while not found:
                for successor in successors:
                    s_d.from_binary(self.__cuts_sequences, successor)
                    hbs = s_d.generate_hyperboxes_set(self.__points_list, self.__boundary_points[0],
                                                      self.__boundary_points[1])
                    if hbs.get_impure_hyperboxes_number() == 0:
                        found = True
                        sequence = successor
                    successors = successor.get_successors()
        # '''
        sequence.debug_print()
