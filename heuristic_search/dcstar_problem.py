from cut_sequences.dimensional_sequence_binary import DimensionalSequenceBinary
from cut_sequences.dimensional_sequence_numeric import DimensionalSequenceNumeric
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
from heuristic_search.problem import Problem
from genetic_algorithm.deap_genetic_guide_sequence_problem import DeapGeneticGuideSequenceProblem
import numpy as np
import matplotlib.pyplot as plt


# Class that defines a problem that can be used by the A* algorithm to define a cluster solution.
class DCStarProblem(Problem):

    # Class constructor
    # @points_list: prototype point list to be used to find the cuts sequence for the clustering
    # @m_d: smallest boundary cut of dimension d
    # @M_d: greatest boundary cut of dimension d
    # @verbose: flag for the debug print
    def __init__(self, points_list, m_d, M_d, verbose = False, gg_parameters = None):

        self.unique_successors = True

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
        if gg_parameters is not None:
            self.__genetic_guide_individual = self.__generate_gg_individual(gg_parameters)


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
        second_level_priority = self.__optimized_first_level_heuristic_value(node)
        first_level_priority = self.g(node) + second_level_priority
        third_level_priority = self.__get_second_level_heuristic_value(node)
        fourth_level_priority = self.__get_second_level_priority(node)
        #fifth_level_priority = self.__get_third_level_priority(node)
        return first_level_priority, second_level_priority, third_level_priority, \
               fourth_level_priority#, fifth_level_priority


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

        #first_heuristic = self.__get_first_level_heuristic_value(node)
        #second_heuristic = self.__get_second_level_heuristic_value(node)
        #return first_heuristic, second_heuristic
        first_heuristic = self.__get_first_level_heuristic_value(node)
        return first_heuristic


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
        node = SelectedDimensionalSequenceNumeric()
        node.from_binary(self.__cuts_sequences, state)
        return self.succ_struct(node)
        #return [successor for successor in state.get_successors()]


    def succ_struct(self, node):

        # inizializzazione della struttura completa del nodo e degli elementi del nodo stesso. La struttura completa è
        # associata alle sequenze di tagli T_d, quindi è composta dall'insieme degli elementi numerici dei tagli. Gli
        # elementi del nodo sono, pertanto, un sottinsieme dell'insieme delle sequenze T_d
        complete_structure = self.__cuts_sequences.elements
        evaluated_node = node.elements

        # inizializzazione del numero di dimensioni della struttura del nodo
        dimensions_number = len(complete_structure)

        # inizializzazione della lista delle lunghezze di ogni sequenza dimensionale. La lista contiene, per ogni array
        # di tagli della struttura completa, la dimensione di T_d.
        dimension_lengths = [len(complete_structure[dimension]) for dimension in range(dimensions_number)]

        # inizializzazione del numero totale degli elementi nella struttura
        elements_number = sum(dimension_lengths)

        # inizializzazione della sequenza cumulativa delle lunghezze. Tale sequenza ha il compito di definire gli indici
        # iniziali sulle varie dimensioni in modo tale da poter essere valutate velocemente
        dimension_offsets = [sum(dimension_lengths[:dimension]) for dimension in range(dimensions_number + 1)]

        # mappatura dei tagli presenti nel nodo passato. La mappatura avviene trasformando le sequenze dei tagli in
        # numeri naturali. Ciò avviene in questo modo: ad ogni taglio presente nella struttura completa è associato
        # un numero naturale, partendo da 0 ed arrivando al valore elements_number - 1. Se un determinato taglio
        # è presente tra gli elementi delle sequenze di tagli del nodo passato, allora si acquisisce il valore
        # dell'indice e lo si inserisce nella struttura della mappatura
        mapped_elements = [np.where(complete_structure[dimension] == evaluated_node[dimension][element])[0][0] + dimension_offsets[dimension]
                           for dimension in range(dimensions_number)
                           for element in range(len(evaluated_node[dimension]))]

        # genera i successori di node mappati come lista di interi
        # generazione dei successori come una lista di tagli mappati. La lista dei successori conterrà un insieme di
        # elementi che saranno differenti tra loro unicamente per un taglio (l'ultimo, per esattezza).
        mapped_successors = [mapped_elements + [new_cut]
                             for new_cut in range(max(mapped_elements, default = -1) + 1, elements_number)]

        # definizione della dimensione associata a ciascun taglio. Per ogni taglio (definito da un elemento naturale)
        # si determina a quale dimensione appartiene: in particolare, se il valore del taglio supera un certo
        # numero di offset (intesi come numeri interi che indicano il taglio, o meglio il suo indice, di partenza per
        # una data dimensione), si determina la dimensione ad esso associato prendendo l'offset minore (ovvero
        # l'indice della dimensione a cui appartiene)
        dimensions = [[min([enum_index - 1 for enum_index, dim_offset in enumerate(dimension_offsets) if dim_offset > cut_index])
                 for cut_index in mapped_successor]
                for mapped_successor in mapped_successors]

        # definizione degli indici dei tagli all'interno delle dimensioni di appartenenza. Essi, pertanto, indicano
        # le posizioni nelle quali i tagli andranno ad essere inseriti. Dato che i tagli all'interno di
        # mapped_successors sono definiti come indici "globali" (ovvero intesi come elementi di una successione
        # a cui fanno capo tutti i tagli di una combinazione, a prescindere dalla dimensione in cui sono posti)
        # bisogna che ci si riconduca agli indici "locali" nelle dimensioni sottraendo a global_cut_index il valore
        # del dimension_offset della dimensione a cui appartiene
        local_cut_indexes = [[global_cut_index - dimension_offsets[dimensions[enum_successor_index][enum_cut_index]]
                        for enum_cut_index, global_cut_index in enumerate(successor)]
                       for enum_successor_index, successor in enumerate(mapped_successors)]

        # definizione della mappatura inversa per la creazione dei successori. La mappatura inversa avviene
        # in questo modo: si acquisiscono i valori dei tagli effettivi (non i valori degli indici) dalla struttura
        # completa sulla base degli elementi presenti in local_cut_indexes e dimensions. Per ognuno degli elementi
        # di local_cut_indexes, infatti, si acquisisce il taglio numerico che si trova alla posizione definita
        # all'interno di un "successore", si utilizza l'indice della dimensione del taglio correlato (presente
        # alla stessa dimensione nella struttura "dimensions") e si acquisisce il taglio effettivo da complete_structure
        # sulla base degli indici trovati. Infine, tutti i successori numerici vengono convertiti in oggetti di tipo
        # DimensionalSequenceBinary e restituiti come output del metodo
        numeric_successors = [[[complete_structure[struct_dim][local_cut_indexes[local_cut_dim][cut_index]]
                                for cut_index in filter(lambda i: dimensions[local_cut_dim][i] == struct_dim, range(len(dimensions[local_cut_dim])))]
                               for struct_dim in range(dimensions_number)]
                              for local_cut_dim in range(len(dimensions))]
        return [DimensionalSequenceBinary(element, self.__cuts_sequences.elements) for element in numeric_successors]



    # Method for acquiring the value of first-level priority for the successor node. The first-level priority
    # is a value based on the sum of cost value and heuristic value.
    # @node: Node object of to be evaluated to get the first-level priority
    def __get_first_level_priority(self, node):

        #g = self.g(node)
        #h = self.h(node)
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
        while index >= 0 and not found:
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

        uno = t_k - t_k_previous
        due = t_k_next - t_k
        return min(uno, due)


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
        hyperboxes = [(hyperbox, self.__get_cuts_number_to_add(hyperbox) )
                      for hyperbox in hyperboxes_set.get_hyperboxes() if hyperbox.is_impure()]
        #hyperboxes.sort(key = lambda element : element[1])

        # initializing the heuristic value to 0. Later, until the list of impure hyperboxes is not empty,
        # heuristic_value is incremented using the remaining hyperboxes
        # NOTE: the name most_impure_hyperboxes refers to the hyperbox with the largest number of different
        # classes within it, obviously the name given is only used to better render the idea and probably
        # not to be considered a scientifically valid term
        heuristic_value = 0
        counter = 0
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
            heuristic_value += most_impure_hyperboxes[1]
            hyperboxes = [hyperbox for hyperbox in hyperboxes if most_impure_hyperboxes[0].is_connected(hyperbox[0]) is False]
            counter += 1

        assert counter == heuristic_value, print("Error in calculating heuristic_value")

        # finally, the heuristic_value calculated is passed as return value
        return heuristic_value


    # TODO DA TRADURRE I COMMENTI IN INGLESE
    def __optimized_first_level_heuristic_value(self, node):

        # create a selected cuts sequence using the binary sequence of passed node
        selected_cuts_sequences = SelectedDimensionalSequenceNumeric()
        selected_cuts_sequences.from_binary(self.__cuts_sequences, node.state)

        # generate an HyperboxesSet object from the newly created selected cuts sequence and using the prototype points list
        hyperboxes_set = selected_cuts_sequences.generate_hyperboxes_set(self.__points_list,
                                                                         m_d = self.__boundary_points[0],
                                                                         M_d = self.__boundary_points[1])

        # acquisizione degli hyperboxes impuri per l'oggetto SelectedDimensionalSequenceNumeric e calcolo del
        # valore del numero minimo di tagli da aggiungere per rendere puri tali hyperboxes. Tutti gli hyperboxes impuri
        # sono salvati all'interno di un dizionario per velocizzare l'accesso ad essi. Il dizionario segue la struttura
        # (hyperbox, n_B_C) : lista di hyperboxes collegati.
        connected_hyperboxes = {(hyperbox, self.__get_cuts_number_to_add(hyperbox)) : []
                                for hyperbox in hyperboxes_set.get_hyperboxes() if hyperbox.is_impure()}

        # definizione della lista degli hyperboxes connessi per ognuno degli hyperboxes del dizionario
        # connected_hyperboxes. Per ogni hyperbox del dizionario si riempie la lista degli hyperboxes in base
        # alla dimensione valutata: infatti, ogni hyperbox possiede un certo gruppo di altri hyperboxes collegati su
        # una particolare dimensione che è differente dal gruppo di hyperboxes associati ad esso su un'altra dimensione.
        for hyperbox, connected_hyperboxes_list in connected_hyperboxes.items():
            for dimension in range(selected_cuts_sequences.get_dimensions_number()):
                connected_hyperboxes_list.append({other_hb for other_hb in connected_hyperboxes.keys()
                                                  if other_hb[0] != hyperbox[0]
                                                  and hyperbox[0].is_connected(other_hb[0], dimension)})

        # inizializzazione del valore dell'euristica a zero. Il valore finale è dato da un incremento unitario che
        # perdura finché il dizionario connected_hyperboxes conterrà hyperboxes impuri da valutare
        heuristic_value = 1
        while len(connected_hyperboxes) > 0:

            # acquisizione del valore massimo di n_B_C associato a tutti gli hyperboxes. Tale valore è associato
            # al valore degli hyperboxes che in questa iterazione verranno valutati, ovvero gli hyperboxes a cui si
            # associa il valore massimo di tagli da aggiungere per poter diventare puri
            max_n_B_C_value = max(connected_hyperboxes.keys(), key = lambda key:key[1])[1]

            # definizione della lista degli hyperboxes che dovranno essere valutati in tale iterazione. Il processo
            # di acquisizione degli hyperbox è semplice: si acquisiscono unicamente gli hyperboxes che possiedono
            # il valore di n_B_C uguale a quello massimo. Di tali hyperboxes, successivamente, si acquisiscono le
            # informazioni riguardo il numero di elementi connessi per ogni dimensione: per esempio, se nella
            # dimensione 0 ci sono tre hyperboxes connessi e nella dimensione 1 ci sono cinque hyperboxes connessi,
            # allora si aggiungono i valori 3 e 5, quindi la struttura inserita nella lista best_hyperboxes sarà:
            # (HYPERBOX, n_B_C), 3, 5
            best_hyperboxes = []
            for hyperbox, connected_hyperboxes_list in connected_hyperboxes.items():
                if hyperbox[1] == max_n_B_C_value:
                    hyperbox_associated_info = [hyperbox]
                    for dimension in connected_hyperboxes_list:
                        hyperbox_associated_info.append(len(dimension))
                    best_hyperboxes.append(hyperbox_associated_info)

            # inizializzazione dell'insieme degli hyperboxes da eliminare dal dizionario
            hyperboxes_to_be_removed = set()

            # se esiste più di un iperbox con un certo valore massimo di n_B_C, allora bisogna scegliere l'hyperbox
            # con il numero maggiore di elementi connessi in una certa dimensione. Per esempio, se un hyperbox h1
            # possiede 3 e 5 elementi connessi nelle due dimensioni, mentre h2 possiede 4 e 2 elementi connessi nelle
            # due dimensioni, allora l'hyperbox che verrà valutato equivale a h1, dato che possiede 5 elementi connessi
            # nella dimensione due, il massimo in assoluto
            if len(best_hyperboxes) > 1:

                # inizializzazione delle variabili dell'hyperbox da acquisire
                best_hyperbox = best_hyperboxes[0][0]
                most_connected_hyperbox_number = best_hyperboxes[0][1]
                dimension_with_most_connected = 0

                # acquisizione dell'hyperbox che possiede il maggior numero di hyperboxes connessi in assoluto
                # su una qualsiasi dimensione, secondo il criterio prima descritto.
                for evaluated_hyperbox in best_hyperboxes:
                    for dimension in range(len(evaluated_hyperbox[1:])):
                        if evaluated_hyperbox[dimension + 1] > most_connected_hyperbox_number:
                            best_hyperbox = evaluated_hyperbox[0]
                            most_connected_hyperbox_number = evaluated_hyperbox[dimension + 1]
                            dimension_with_most_connected = dimension

                # acquisizione degli hyperboxes da rimuovere dal dizionario. Gli hyperboxes da rimuovere sono
                # quello definito da best_hyperbox (presente come chiave nel dizionario) e quelli presenti nella
                # lista degli hyperboxes collegati per il detto best_hyperbox (salvato come attributo del dizionario)
                hyperboxes_to_be_removed = set(hyperbox_to_remove for hyperbox_to_remove
                                               in connected_hyperboxes.get(best_hyperbox)[dimension_with_most_connected])
                hyperboxes_to_be_removed.add(best_hyperbox)

            # se esiste un solo iperbox con un certo valore massimo di n_B_C, allora lo si aggiunge all'insieme degli
            # hyperboxes da rimuovere dal dizionario
            else:
                hyperboxes_to_be_removed.add(best_hyperboxes[0][0])

            # rimozione degli hyperboxes dal dizionario, rimuovendo dapprima gli elementi come key del dizionario.
            # Successivamente, per ogni elemento rimanente, si eliminano i riferimenti degli hyperboxes nelle liste
            # degli elementi connessi, facendo in modo che essi non verranno più valutati.
            for ipercubo_da_cancellare in hyperboxes_to_be_removed:
                connected_hyperboxes.pop(ipercubo_da_cancellare)
            for ipercubo_valutato, ipercubi_connessi_per_dimensione in connected_hyperboxes.items():
                for lista_ipercubi_nella_dimensione in ipercubi_connessi_per_dimensione:
                    lista_ipercubi_nella_dimensione.difference_update(hyperboxes_to_be_removed)

            # il valore di euristica viene incrementato di una unità e si passa alla iterazione successiva
            heuristic_value += 1

        # ritorno del valore di euristica calcolato
        return heuristic_value


    # Method for acquiring the second-level heuristic value. It is based on Jaccard's dissimilarity.
    # When genetic guide is not called acts as a dummy method
    # @node: Node object of to be evaluated to get the second-level heuristic
    def __get_second_level_heuristic_value(self, node):
        if self.__genetic_guide_individual is None:
            return 0
        else:
            # initialize intersection and union cardinality
            intersection_value = 0
            union_value = 0

            genetic_individual = SelectedDimensionalSequenceNumeric()
            genetic_individual.from_binary(self.__cuts_sequences, self.__genetic_guide_individual)

            numerical_node = SelectedDimensionalSequenceNumeric()
            numerical_node.from_binary(self.__cuts_sequences, node.state)

            '''
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
            '''
            for dimension in range(genetic_individual.get_dimensions_number()):
                intersection_value += len(set(numerical_node.get_dimension(dimension)).
                                          intersection(set(genetic_individual.get_dimension(dimension))))
                union_value += len(set(numerical_node.get_dimension(dimension)).
                                       union(set(genetic_individual.get_dimension(dimension))))

            # return Jaccard dissimilarity
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
        return sum(necessary_cuts)


    # Method for generate a genetic DimensionalSequenceBinary individual to be used as guide for A* computation
    # @gg_parameters: dictionary of parameters to initialize genetic guide
    def __generate_gg_individual(self, gg_parameters):

        # initialize the genetic guide
        genetic_guide, population_size, generations, selected_best = self.__initialize_gg(gg_parameters)

        # create an empty binary sequence
        sequence = DimensionalSequenceBinary()

        # generate pure genetic sequence using "evolve" method - possible call of "worst_case_scenario"
        # sequence.from_binary(genetic_guide.evolve(population_size, generations, selected_best))

        # generate pure genetic sequence forcing "worst_case_scenario" method
        # sequence.from_binary(DeapGeneticGuide.worst_case_scenario(genetic_guide, genetic_guide.elements_per_dimension))

        # generate genetic sequence with impure possibility
        sequence.from_binary(genetic_guide.evolve_without_wsc(population_size, generations, selected_best))

        s_d = SelectedDimensionalSequenceNumeric()
        s_d.from_binary(self.__cuts_sequences, sequence)
        hbs = s_d.generate_hyperboxes_set(self.__points_list, self.__boundary_points[0], self.__boundary_points[1])
        if hbs.get_impure_hyperboxes_number() != 0:
            print("evaluated genetic individual is an impure one\n")

        '''
        # Process of sequence purification
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
            #successors = self.successors(sequence)
            # while is not found a pure solution
            while not found and successors != []:
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
        if self.verbose:
            print("Genetic individual:")
            sequence.debug_print()

        return sequence


    # Method for initialize the genetic guide into DCStarProblem if needed
    # @gg_parameters: dictionary of parameters to initialize genetic guide
    def __initialize_gg(self, gg_parameters):

        # calculate the size of each dimension of cuts sequence
        genes_per_dimension = list()
        for dimension in range(self.__cuts_sequences.get_dimensions_number()):
            genes_per_dimension.append(len(self.__cuts_sequences.get_dimension(dimension)))

        # calculate the total number of genes that the genome will have
        genes_number = 0
        for num in genes_per_dimension:
            genes_number += num

        # calculate population
        # N.B.: population is given by duplicating the number of genes in the genome
        population_size = 2 * genes_number

        # calculate mutation rate
        # N.B.: mutation rate is calculated by reciprocating the number of genes
        mutation_rate = 1 / genes_number

        # define DGG object to create the genetic guide with monodimensional lists
        genetic_guide = DeapGeneticGuideSequenceProblem(genes_number, mutation_rate, gg_parameters["mating_rate"],
                                                        gg_parameters["selected_for_tournament"], self.__cuts_sequences,
                                                        self.__points_list, genes_per_dimension,
                                                        self.__boundary_points[0], self.__boundary_points[1])

        return genetic_guide, gg_parameters["generations"], population_size, gg_parameters["selected_best"]


    def get_genetic_guide_individual(self):
        return self.__genetic_guide_individual
