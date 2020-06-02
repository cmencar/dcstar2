from heuristic_search import astar, dcstar_problem
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
from cut_sequences.point import Point
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import random
import time


class DoubleClusteringStar:

    def __init__(self, prototypes, m_d, M_d, verbose=False, genetic_guide_parameters=None):

        self.problem = dcstar_problem.DCStarProblem(prototypes, m_d=m_d, M_d=M_d, verbose=verbose,
                                                    gg_parameters=genetic_guide_parameters)
        self.prototypes = prototypes
        self.m_d = m_d
        self.M_d = M_d
        self.cuts_sequences = self.problem.get_cuts_sequences()
        self.result = SelectedDimensionalSequenceNumeric()
        self.verbose = verbose
        self.branches_taken = 0
        self.time = 0


    def train(self, save_log=False):

        binary_result, self.branches_taken, self.time, evaluated_nodes = astar.astar(problem=self.problem)
        self.result.from_binary(self.cuts_sequences, binary_result)

        if self.problem.verbose:
            print("\nFound node in", self.branches_taken, "evaluation in", self.time, "sec.")
            nodes = [node[0] for node in evaluated_nodes]
            if len(nodes) - len(set(nodes)) > 0:
                print("Duplicate elements:", set([node for node in evaluated_nodes if evaluated_nodes.count(node) > 1]))

        if save_log:
            self.__save_log(evaluated_nodes)

        return self.result, self.branches_taken, self.time


    def predict(self, element):

        point = Point(element)

        hyperboxes_set = self.result.generate_hyperboxes_set(point_list=self.prototypes, m_d=self.m_d, M_d=self.M_d)

        predicted_class = None
        for hyperbox in hyperboxes_set.get_hyperboxes():
            if hyperbox.is_in_boundaries(point):
                predicted_class = hyperbox.get_belonging_points()[0].get_label()

        return predicted_class


    # @TODO N.B. FATTA AD-HOC PER IRIS, QUINDI MODIFICARE STRUTTURA DI GESTIONE DEL DATASET
    def evaluate_classificator(self, dataset, results):

        hbs = self.result.generate_hyperboxes_set(point_list=self.prototypes, m_d=self.m_d, M_d=self.M_d)
        for hb in hbs.get_hyperboxes():
            if hb.is_impure():
                print("IMPURE HB!\n")

        counter = 0
        nonecounter = 0
        for element, result in zip(dataset, results):
            cl = self.predict(element)
            if result == cl:
                counter += 1
            elif cl is None:
                nonecounter += 1

        print("Classificator accuracy:", counter/len(dataset) * 100, "% (", counter, ")")
        print("Classificator accuracy (None):", nonecounter/len(dataset) * 100, "% (", nonecounter, ")")

        return counter/len(dataset)*100


    def plot_result(self):

        if self.result is not None and self.result.get_dimensions_number() == 2:

            # printing T_d sequences in the plot
            for cut in self.cuts_sequences.get_dimension(0):
                plt.plot([cut, cut], [self.m_d[0], self.M_d[0]], 'k', linestyle=':', color='grey')
            for cut in self.cuts_sequences.get_dimension(1):
                plt.plot([self.m_d[1], self.M_d[1]], [cut, cut], linestyle=':', color='grey')

            # printing S_d sequences in the plot
            for cut in self.result.get_dimension(0):
                plt.plot([cut, cut], [self.m_d[0], self.M_d[0]], 'k', linestyle='--', color='red')
            for cut in self.result.get_dimension(1):
                plt.plot([self.m_d[1], self.M_d[1]], [cut, cut], linestyle='--', color='red')

            classes = set([p.get_label() for p in self.prototypes])
            colors_list = list(colors._colors_full_map.values())
            random.shuffle(colors_list)
            colored_class = {label: color for label, color in zip(classes, colors_list)}

            for point in self.prototypes:
                if point.get_label() == 1.0:
                    color = "red"
                elif point.get_label() == 2.0:
                    color = "green"
                else:
                    color = "blue"
                plt.scatter(point.get_coordinate(0), point.get_coordinate(1), color=color)

            # showing the plot to video
            plt.show()


    def __save_log(self, evaluated_nodes):

        filename = time.asctime(time.localtime(time.time())).replace(" ", "_").replace(":", "_") + ".dcl"
        file = open(filename, "w")

        file.write("# Prototypes\n")
        for prototype in self.prototypes:
            file.write(repr(prototype.get_coordinates()).replace("\n", "") + "; " + repr(prototype.get_label()) + "\n")

        file.write("\n# T_d sequences\n")
        file.write(repr(self.cuts_sequences.elements).replace("\n", "").replace("\t", "") + "\n")

        if self.problem.get_genetic_guide_individual() is not None:
            file.write("\n# Genetic sequences\n")
            file.write(
                repr(self.problem.get_genetic_guide_individual().elements).replace("\n", "").replace("\t", "") + "\n")
            file.write("\n# Genetic purity\n")
            file.write(repr(self.problem.get_genetic_guide_purity()) + "\n")
            file.write("\n# Genetic algoritm's time\n")
            file.write(repr(self.problem.get_genetic_algorithm_time()) + "\n")

        file.write("\n# S_d sequences\n")
        for evaluated_node in evaluated_nodes:
            file.write(evaluated_node[0].replace("\n", "").replace("\t", "") + "; " + evaluated_node[1] + "\n")

        file.write("\n# M_d\n")
        file.write(repr(self.M_d) + "\n")

        file.write("\n# m_d\n")
        file.write(repr(self.m_d) + "\n")

        file.write("\n# Time\n")
        file.write(repr(self.time) + "\n")

        file.write("\n# Number of evaluated nodes\n")
        file.write(repr(self.branches_taken) + "\n")

        hbs = self.result.generate_hyperboxes_set(point_list=self.prototypes, m_d=self.m_d, M_d=self.M_d).get_hyperboxes()
        file.write("\n# Number of hyperboxes created\n")
        file.write(repr(len(hbs)) + "\n")

        file.close()
