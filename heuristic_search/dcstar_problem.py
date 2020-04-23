from cut_sequences.dimensional_sequence_binary import DimensionalSequenceBinary
from cut_sequences.dimensional_sequence_numeric import DimensionalSequenceNumeric
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
from heuristic_search.Problem import Problem
from genetic_algorithm.deap_genetic_guide import DeapGeneticGuide
import numpy as np


# Class that defines a problem that can be used by the A* algorithm to define a cluster solution.
class DCStarProblem(Problem):

    # Class constructor
    # @points_list: prototype point list to be used to find the cuts sequence for the clustering
    # @m_d: smallest boundary cut of dimension d
    # @M_d: greatest boundary cut of dimension d
    # @verbose: flag for the debug print
    def __init__(self, points_list, m_d, M_d, verbose = False, use_genetic_guide = False):

        # initialization of point list
        self.__points_list = points_list

        # creation of cuts sequences using the points list
        self.__cuts_sequences = self.__create_cuts_sequences()

        # initialization of boundaries of extended cuts sequences
        self.__boundary_points = (m_d, M_d)

        # initialization of starting state
        self.start_state = self.__cuts_sequences.generate_starting_binary()

        # initialization of verbose flag
        self.verbose = verbose

        # initialization of the individual from genetic guide
        self.__genetic_guide_individual = None
        if use_genetic_guide:
            self.__genetic_guide_individual = self.__generate_gg_individual()


    # Method for creating a cuts sequence starting from a list of prototype points
    def __create_cuts_sequences(self):

        # initializes an empty list in order to contain the sequence of T_d cuts that will later be used
        # to create the DimensionalSequenceNumeric object
        numerical_cuts_sequence = list()

        # for each possible dimension, indirectly defined by the number of coordinates of any point
        for dimension_index in range(len(self.__points_list[0].get_coordinates())):

            # sorts the list of points based on the coordinate value on the dimension identified by dimension_index
            sorted_point_list = sorted(self.__points_list, key= lambda point: point.get_coordinate(dimension_index))

            # for each point a projection of the same is determined on the dimension defined by dimension_index.
            # The value of the projection is equivalent to the coordinate of the point on the dimension evaluated.
            # In case two or more points share the same projection there will be two cases: if they are part of
            # the same class, then the class they belong to will be stored only once, if they are part of different
            # classes, then more information about the classes will be stored, so that the information is not lost.
            # projection_on_d will be defined, therefore, as a dictionary where the key is the numerical value
            # of the projection on d while the attribute is the set of classes of the prototypes projected on d
            projections_on_d = dict()
            for point in sorted_point_list:
                if projections_on_d.get(point.get_coordinate(dimension_index)) is None:
                    projections_on_d.__setitem__(point.get_coordinate(dimension_index), {point.get_label()})
                else:
                    projections_on_d.get(point.get_coordinate(dimension_index)).add(point.get_label())

            # dimensional projections must be ordered so that they make sense when defining cuts. In this regard,
            # a list is first defined containing as elements the pair 'projection value'-'set of classes' and,
            # subsequently, it is sorted according to the projection value
            sorted_projections_on_d = sorted([(point_coordinate, set(point_classes))
                                              for point_coordinate, point_classes in projections_on_d.items()])

            # for each pair of projections defined by sorted_projections_on_d a cut must be determined.
            # The cut is only defined if the projections belong to two different classes. In this way, the set
            # of classes of the evaluated projection must either be different from the next projection in the order
            # in sorted_projections_on_d or it must contain more than one class (since it has at least two
            # different classes, at least one of the two is different).
            cuts_in_d = [(sorted_projections_on_d[projection_idx][0] + sorted_projections_on_d[projection_idx + 1][0])/2
                         for projection_idx in range(len(sorted_projections_on_d) - 1)
                         if sorted_projections_on_d[projection_idx][1] != sorted_projections_on_d[projection_idx + 1][1]
                         or len(sorted_projections_on_d[projection_idx][1]) > 1]

            # once a valid cuts sequence for the dimension is defined, it is inserted in the global cuts sequence
            numerical_cuts_sequence.append(cuts_in_d)

        # using the global cuts sequence, a DimensionalSequenceNumeric object is created and passed as return value
        return DimensionalSequenceNumeric(numerical_cuts_sequence)


    # Method for calculating the cost of the node. The cost of the node is calculated evaluating the
    # three-levels priority and define a tuple with the three values
    # @node: Node object of to be evaluated to get the cost value
    def estimate_cost(self, node):
        first_level_priority = self.__get_first_level_priority(node)
        second_level_priority = self.__get_second_level_priority(node)
        third_level_priority = self.__get_third_level_priority(node)
        return tuple((first_level_priority, second_level_priority, third_level_priority))


    # Method for acquiring the g path-cost value. It is based on the counting the cuts present in the
    # logical sequence which value is True
    # @node: Node object of to be evaluated to get the path-cost value
    def g(self, node):
        x = 0
        for dimension_index in range(node.state.get_dimensions_number()):
            for cut in node.state.get_dimension(dimension_index):
                if cut:
                    x += 1
        return x


    # Method for acquiring the heuristic value. It is based on the sum of first-level and second-level heuristic values
    # @node: Node object of to be evaluated to get the second-level heuristic
    def h(self, node):
        return self.__get_first_level_heuristic_value(node) + self.__get_second_level_heuristic_value(node)


    # Method for acquiring if the node is a result of clustering process. Is based on the fact that each hyperbox
    # produced by the passed binary cuts sequence is pure, i.e. it contains a set of prototypes belonging to the same class
    # @state: DimensionalSequenceBinary object of to be evaluated to get the second-level priority
    def goal(self, state):

        # create a selected cuts sequence using the binary sequence of passed node
        selected_cuts_sequences = SelectedDimensionalSequenceNumeric()
        selected_cuts_sequences.from_binary(self.__cuts_sequences, state)

        # generate an HyperboxesSet object from the newly created selected cuts sequence and using the prototype points list
        hyperboxes_set = selected_cuts_sequences.generate_hyperboxes_set(self.__points_list,
                                                                         m_d = self.__boundary_points[0],
                                                                         M_d = self.__boundary_points[1])

        # the return value will be True if the HyperboxesSet object contain only pure hyperboxes, False otherwise
        return True if hyperboxes_set.get_impure_hyperboxes_number() == 0 else False


    # Method for acquiring the list of successors for passed DimensionalSequenceBinary.
    # @state: DimensionalSequenceBinary object to be evaluated to get the successors list.
    def successors(self, state):
        return [successor for successor in state.get_successors()]


    # Method for acquiring the value of first-level priority for the successor node. The first-level priority
    # is a value based on the sum of cost value and heuristic value.
    # @node: Node object of to be evaluated to get the first-level priority
    def __get_first_level_priority(self, node):
        return self.g(node) + self.h(node)


    # Method for acquiring the value of second-level priority for the successor node. The second-level priority is a
    # value based on the thickness of a space that is defined using the newly added cut: greater the value,
    # greater the information granule defined by the distance (so that smaller the distance between left and right
    # cuts of newly inserted cut, smaller is the priority value)
    # @node: Node object of to be evaluated to get the second-level priority
    def __get_second_level_priority(self, node):

        # definition of two binary sequences taken from a node and from its evaluated successor node
        node_state = node.state
        ancestor_state = node.parent.state

        # initialization of indexes for defining the specific cut to be taken to evaluate the section space
        cut_index = 0
        dimension_index = 0

        # initialization of flag for the found cut
        found = False

        # while the cut is not found, search in the logical sequence the newly added cut
        while not found:

            # if there is a pair of cut (one from ancestor_state, one from node_state) that are not equal each other,
            # then the newly added cut into successor node is found. Therefore, set the found flag to true and
            # don't change the indexes value. On the other hand, if the newly added cut is not found in node_state,
            # then increment the cut_index and dimension_index
            if ancestor_state.get_cut(dimension_index, cut_index) != node_state.get_cut(dimension_index, cut_index) or \
                    dimension_index == ancestor_state.get_dimensions_number():
                found = True
            else:
                cut_index = (cut_index + 1) % ancestor_state.get_dimension_size(dimension_index)
                if cut_index == 0:
                    dimension_index += 1

        # initialization of newly added cut (t_k), the previous cut (t_k_previous) and the next cut (t_k_next).
        # The first value set to t_k_previous and t_k_next are, respectively, the values of m_d and M_d
        t_k = self.__cuts_sequences.get_dimension(dimension_index)[cut_index]
        t_k_previous = self.__boundary_points[0][dimension_index]
        t_k_next = self.__boundary_points[1][dimension_index]

        # reset the found flag
        found = False

        # initialize the node_state scanning index to cut_index and search into the binary sequence until
        # the index reaches 0 or an element is found. An element is found (so a valid value for t_k_previous)
        # when a logical cut value is True: using the value defined by index, the numerical value of cut
        # is taken and it is assigned to t_k_previous
        index = cut_index - 1
        while index > 0 and not found:
            if node_state.get_cut(dimension_index, index):
                t_k_previous = self.__cuts_sequences.get_dimension(dimension_index)[index]
                found = True
            index -= 1

        # reset the found flag
        found = False

        # initialize the node_state scanning index to cut_index and search into the binary sequence until
        # the index reaches the last value of dimension (to which dimension_index refers) or an element is found.
        # An element is found (so a valid value for t_k_next) when a logical cut value is True: using the
        # value defined by index, the numerical value of cut is taken and it is assigned to t_k_next
        index = cut_index + 1
        while index < self.__cuts_sequences.get_dimension_size(dimension_index) and not found:
            if node_state.get_cut(dimension_index, index):
                t_k_next = self.__cuts_sequences.get_dimension(dimension_index)[index]
                found = True
            index += 1

        # the returned value is the minimum between two elements: the distance between t_k and t_k_previous
        # and the distance between t_k_next and t_k
        return min(t_k - t_k_previous, t_k_next - t_k)


    # Method for acquiring the value of third-level priority for the successor node. The third-level priority is a
    # value based on the number of different feature used for defining an hyperboxes. It is the number of dimensions
    # (features) in the binary cuts sequence that contain at least one cut. The value is subsequently negated,
    # so that more emphasis is placed on sequences with fewer dimensions used (the more dimensions with at least
    # one cut are presents, the lower the priority).
    # @node: Node object of to be evaluated to get the third-level priority
    def __get_third_level_priority(self, node):

        # for every dimension in the successor node, if it has at least
        # one cut, then the counter is decreased by one unit
        value = 0
        for array in node.state.elements:
            if np.any(array):
                value -= 1
        return value


    # Method for acquiring the first-level heuristic value. It is based on the minimum value of cuts
    # to be defined so that all hyperboxes defined by node are pure. It iterates over the impure hyperboxes,
    # starting from the one with the maximum number of different class labels. Once an hyperbox is selected,
    # the heuristic value is summed to a counter and all connected hyper-boxes are removed (two or more hyperboxes
    # are connected if they have in common at least a couple of cuts, named boundaries). The procedure stops
    # when the collection of hyperboxes to scan is empty and, finally, the value of the counter is returned.
    # @node: Node object of to be evaluated to get the heuristic value
    def __get_first_level_heuristic_value(self, node):

        # create a selected cuts sequence using the binary sequence of passed node
        selected_cuts_sequences = SelectedDimensionalSequenceNumeric()
        selected_cuts_sequences.from_binary(self.__cuts_sequences, node.state)

        # generate an HyperboxesSet object from the newly created selected cuts sequence and using the prototype points list
        hyperboxes_set = selected_cuts_sequences.generate_hyperboxes_set(self.__points_list,
                                                                         m_d = self.__boundary_points[0],
                                                                         M_d = self.__boundary_points[1])

        # all impure hyperboxes are captured by the HyperboxesSet object and placed in a list and is evaluated
        # the minimum number of cuts (for single hyperbox) to be added to transform them in pure hyperboxes.
        # The list is then sorted according to the value of the number of cuts to be added.
        # On the list of impure hyperboxes will be based the evaluation of the value of the first level heuristics.
        hyperboxes = [(hyperbox, self.__get_cuts_number_to_add(hyperbox))
                      for hyperbox in hyperboxes_set.get_hyperboxes() if hyperbox.is_impure()]
        hyperboxes.sort(key = lambda element : element[1])

        # initializing the heuristic value to 0. Later, until the list of impure hyperboxes is not empty,
        # heuristic_value is incremented using the remaining hyperboxes
        # NOTE: the name most_impure_hyperboxes refers to the hyperbox with the largest number of different
        # classes within it, obviously the name given is only used to better render the idea and probably
        # not to be considered a scientifically valid term
        heuristic_value = 0
        while len(hyperboxes) > 0:

            # acquiring the first hyperbox in the impure hyperboxes list (is not necessarily the 'worst').
            most_impure_hyperboxes = hyperboxes[0]

            # for each hyperbox is evaluated if it is 'worse' than most_impure_hyperbox, i.e. if it has
            # more cuts to be added. If so, then the evaluated hyperbox becomes the most_impure_hyperbox
            for hyperbox in hyperboxes:
                if hyperbox[1] > most_impure_hyperboxes[1]:
                    most_impure_hyperboxes = hyperbox

            # heuristic_value is increased by adding the already existing value with the number of cuts to be added
            # in the most_impure_hyperbox. Subsequently, each hyperbox connected to the most_impure_hyperbox (thus also
            # the most_impure_hyperbox itself) is deleted from the list and the evaluation of the remaining hyperboxes continue
            heuristic_value += sum(most_impure_hyperboxes[1])
            hyperboxes = [hyperbox for hyperbox in hyperboxes if most_impure_hyperboxes[0].is_connected(hyperbox[0]) is False]

        # finally, the heuristic_value calculated is passed as return value
        return heuristic_value


    # Method for acquiring the second-level heuristic value. It is based on Jaccard's similarity.
    # When genetic guide is not called acts as a dummy method
    # @node: Node object of to be evaluated to get the second-level heuristic
    def __get_second_level_heuristic_value(self, node):
        if self.__genetic_guide_individual is None:
            return 0
        else:
            # initialize intersection and union cardinality
            intersection_value = 0
            union_value = 0
            # for each dimension into evaluated node
            for dimension in range(node.state.get_dimensions_number()):
                # increment intersection cardinality by the one of the intersection of both
                # evaluated node and genetic guide sequence
                intersection_value += len(
                    set(node.state.get_dimension(dimension)).intersection(
                        set(self.__genetic_guide_individual.get_dimension(dimension))))
                # increment union cardinality by the one of the union of both
                # evaluated node and genetic guide sequence
                union_value += len(
                    set(node.state.get_dimension(dimension)).union(
                        set(self.__genetic_guide_individual.get_dimension(dimension))))
            # return Jaccard similarity
            return 1 - intersection_value / union_value


    # Method for acquiring the value of cuts sequences
    def get_cuts_sequences(self):
        return self.__cuts_sequences


    # Method for acquiring the number of cuts to add for every dimension to transform a passed
    # impure hyperbox into a pure hyperbox
    # @hyperbox: Hyperbox object to be evaluated to get the minimum number of cuts to add
    def __get_cuts_number_to_add(self, hyperbox):

        # definition of the maximum number of cuts per size to be added to the hyperbox. The value is calculated
        # by counting the cuts in T_d that are within the range delimited by the hyperbox boundaries.
        # This count is applied for each d size of the hyperbox.
        max_cuts = [0 for _ in range(self.__cuts_sequences.get_dimensions_number())]
        for dimension_index in range(self.__cuts_sequences.get_dimensions_number()):
            for cut in self.__cuts_sequences.get_dimension(dimension_index):
                if hyperbox.get_boundaries()[dimension_index][0] < cut < hyperbox.get_boundaries()[dimension_index][1]:
                    max_cuts[dimension_index] += 1

        # initialize the necessary_cuts list which contains a set of values equal to 0, one for each hyperbox size
        necessary_cuts = [0 for _ in range(len(max_cuts))]

        # initialize the dimension index to zero
        dimension_index = 0

        # ff the number of cuts to be added is less than the number of different classes in the hyperbox,
        # some cuts must be added. In detail, it evaluate the first dimension and assess if the number of cuts
        # in necessary_cuts is less than max_cuts for that dimension (i.e. if all possible cuts for that dimension
        # in the evaluated hyperbox have already been added in necessary_cuts). If it is smaller, then an additional
        # cut is added, increasing the value of necessary_cuts for the evaluated dimension. Then, at the next iterative
        # step, it evaluate the next dimension, analyzing in the same way the amount of necessary_cuts for that
        # dimension and making, if necessary, the increase. Once the dimensions are finished, it start again from the
        # first dimension (this process is guaranteed by the mod operator) and check again the number of necessary_cuts
        # for this dimension. The cyclic evaluation of the various dimensions ends when the initial condition
        # (i.e. if the number of cuts to be added is less than the number of different classes  in hyperbox) occurs.
        while np.prod([cuts_in_dimension + 1 for cuts_in_dimension in necessary_cuts]) < hyperbox.get_different_classes_number():
            dimension_index = (dimension_index % len(necessary_cuts)) + 1
            if necessary_cuts[dimension_index - 1] < max_cuts[dimension_index - 1]:
                necessary_cuts[dimension_index - 1] += 1

        # the list of the number of cuts for each dimension is returned
        return necessary_cuts


    # Method for generate a genetic DimensionalSequenceBinary individual to be used as guide for A* computation
    def __generate_gg_individual(self):

        # initialize the genetic guide
        genetic_guide, population_size, generations, selected_best = self.__initialize_gg()

        # create an empty binary sequence
        sequence = DimensionalSequenceBinary()

        # generate pure genetic sequence using "evolve" method - possible call of "worst_case_scenario"
        sequence.from_binary(genetic_guide.evolve(population_size, generations, selected_best))

        # generate pure genetic sequence forcing "worst_case_scenario" method
        # sequence.from_binary(DeapGeneticGuide.worst_case_scenario(genetic_guide, genetic_guide.elements_per_dimension))

        # generate genetic sequence with correction of impureness when needed
        # sequence.from_binary(genetic_guide.evolve_without_wsc(population_size, generations, selected_best))

        # Purification of sequence process
        '''
        # create a selected cuts sequence with given genetic guide binary sequence
        s_d = SelectedDimensionalSequenceNumeric()
        s_d.from_binary(self.__cuts_sequences, sequence)
        # generate hyperboxes of created selected cuts sequence
        hbs = s_d.generate_hyperboxes_set(self.__points_list, self.__boundary_points[0], self.__boundary_points[1])
        # if solution sequence is not fully pure
        if hbs.get_impure_hyperboxes_number() != 0:
            print("Impure DGG sequence generated, purification in process")
            # set solution not found
            found = False
            # generate successors of genetic binary sequence with added random cut
            successors = sequence.get_successors()
            # while is not found a pure solution
            while not found:
                # for every generated successor
                for successor in successors:
                    # generate successor's hyperboxes
                    s_d.from_binary(self.__cuts_sequences, successor)
                    hbs = s_d.generate_hyperboxes_set(self.__points_list, self.__boundary_points[0],
                                                      self.__boundary_points[1])
                    # if evaluated successor is fully pure
                    if hbs.get_impure_hyperboxes_number() == 0:
                        # set solution found
                        found = True
                        # change generated sequence with pure successor
                        sequence = successor
                    # generate other successors
                    successors = successor.get_successors()
        '''
        # show genetic guide sequence
        sequence.debug_print()

        return sequence


    # Method for initialize the genetic guide into DCStarProblem if needed
    def __initialize_gg(self):

        # calculate the size of each dimension of cuts sequence
        genes_per_dimension = list()
        for dimension in range(self.__cuts_sequences.get_dimensions_number()):
            genes_per_dimension.append(len(self.__cuts_sequences.get_dimension(dimension)))

        # calculate the total number of genes that the genome will have
        genes_number = 0
        for num in genes_per_dimension:
            genes_number += num

        # set number of individuals for tournament selection
        selected_for_tournament = 5

        # calculate population
        # N.B.: population is given by duplicating the number of genes in the genome
        population_size = 2 * genes_number

        # set number of generations
        generations = 20

        # calculate mutation rate
        # N.B.: mutation rate is calculated by reciprocating the number of genes
        mutation_rate = 1 / genes_number

        # set mating rate
        mating_rate = 0.7

        # set number of best individuals to choose from
        selected_best = 10

        # define DGG object to create the genetic guide with monodimensional lists
        genetic_guide = DeapGeneticGuide(genes_number, mutation_rate, mating_rate, selected_for_tournament,
                                         self.__cuts_sequences, self.__points_list, genes_per_dimension,
                                         self.__boundary_points[0], self.__boundary_points[1])

        return genetic_guide, generations, population_size, selected_best
