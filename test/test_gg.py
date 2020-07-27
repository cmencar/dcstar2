from cut_sequences.dimensional_sequence_numeric import DimensionalSequenceNumeric
# from genetic_algorithm.deap_genetic_guide_sequence_problem import DeapGeneticGuideSequenceProblem
# from genetic_algorithm.dgp_test import DeapGeneticGuideSequenceProblem
# from genetic_algorithm.gp_test import GeneticGuideSequenceProblem
# from genetic_algorithm.dgp_option2_plus1_null import DeapGeneticGuideSequenceProblem
from genetic_algorithm.dgp_option2_plus1_random import DeapGeneticGuideSequenceProblem
from heuristic_search.prototypes_creator import PrototypesCreator
# import winsound

# TODO - varie dimensioni del torneo, test
gg_args_test = {
    # "selected_for_tournament": 3,
    "selected_for_tournament": 5,
    # "selected_for_tournament": 10,
    "generations": 15000,
    "mating_rate": 0.5
}

filecuts = open("tagli.txt", "w")

test_datasets = [
    ("created point lists/banana_100_30.json", "banana"),
    ("created point lists/bandiera_100_30.json", "bandiera"),
    ("created point lists/glass_100_18.json", "glass"),
    ("created point lists/ionosphere_100_20_norm.json", "iono"),
    ("created point lists/iris_100_42_norm.json", "iris"),
    ("created point lists/shuttle_100_21_norm.json", "shuttle"),
    ("created point lists/wbc_100_60_norm.json", "wbc"),
    ("created point lists/wine_100_42.json", "wine")
]

# '''
for dataset in test_datasets:
    print(dataset[1])
    loader = PrototypesCreator()
    point_list, m_d, M_d = loader.load(dataset[0])

    numerical_cuts_sequence = list()
    for dimension_index in range(len(point_list[0].get_coordinates())):
        sorted_point_list = sorted(point_list, key=lambda point: point.get_coordinate(dimension_index))
        projections_on_d = dict()
        for point in sorted_point_list:
            if projections_on_d.get(point.get_coordinate(dimension_index)) is None:
                projections_on_d.__setitem__(point.get_coordinate(dimension_index), {point.get_label()})
            else:
                projections_on_d.get(point.get_coordinate(dimension_index)).add(point.get_label())
        sorted_projections_on_d = sorted([(point_coordinate, set(point_classes)) for point_coordinate, point_classes in
                                          projections_on_d.items()])
        cuts_in_d = [
            (sorted_projections_on_d[projection_idx][0] + sorted_projections_on_d[projection_idx + 1][0]) / 2
            for projection_idx in range(len(sorted_projections_on_d) - 1)
            if sorted_projections_on_d[projection_idx][1] != sorted_projections_on_d[projection_idx + 1][1]
            or len(sorted_projections_on_d[projection_idx][1]) > 1]
        numerical_cuts_sequence.append(cuts_in_d)
    cuts_sequence = DimensionalSequenceNumeric(numerical_cuts_sequence)

    genes_per_dimension = list()
    for dimension in range(cuts_sequence.get_dimensions_number()):
        genes_per_dimension.append(len(cuts_sequence.get_dimension(dimension)))

    genes_number = 0
    for num in genes_per_dimension:
        genes_number += num

    population_size = 2 * genes_number

    mutation_rate = 1 / genes_number
    # crossover = 1 - mutation_rate

    print("Mutation rate calculated: ", mutation_rate)

    # genetic_guide = GeneticGuideSequenceProblem(genes_number, mutation_rate, gg_args_test["mating_rate"],
    genetic_guide = DeapGeneticGuideSequenceProblem(genes_number, mutation_rate, gg_args_test["mating_rate"],
    # genetic_guide = DeapGeneticGuideSequenceProblem(genes_number, mutation_rate, crossover,
                                                    gg_args_test["selected_for_tournament"], cuts_sequence,
                                                    point_list, genes_per_dimension, m_d, M_d)

    a, b = genetic_guide.evolve(population_size, gg_args_test["generations"], dataset[1])

    content = dataset[1] + " " + str(a) + "/" + str(b) + "\n"
    filecuts.write(content)
# '''
'''
print("banana")
loader = PrototypesCreator()
point_list, m_d, M_d = loader.load("created point lists/banana_100_30.json")

numerical_cuts_sequence = list()
for dimension_index in range(len(point_list[0].get_coordinates())):
    sorted_point_list = sorted(point_list, key=lambda point: point.get_coordinate(dimension_index))
    projections_on_d = dict()
    for point in sorted_point_list:
        if projections_on_d.get(point.get_coordinate(dimension_index)) is None:
            projections_on_d.__setitem__(point.get_coordinate(dimension_index), {point.get_label()})
        else:
            projections_on_d.get(point.get_coordinate(dimension_index)).add(point.get_label())
    sorted_projections_on_d = sorted([(point_coordinate, set(point_classes)) for point_coordinate, point_classes in
                                        projections_on_d.items()])
    cuts_in_d = [
        (sorted_projections_on_d[projection_idx][0] + sorted_projections_on_d[projection_idx + 1][0]) / 2
        for projection_idx in range(len(sorted_projections_on_d) - 1)
        if sorted_projections_on_d[projection_idx][1] != sorted_projections_on_d[projection_idx + 1][1]
        or len(sorted_projections_on_d[projection_idx][1]) > 1]
    numerical_cuts_sequence.append(cuts_in_d)
cuts_sequence = DimensionalSequenceNumeric(numerical_cuts_sequence)

genes_per_dimension = list()
for dimension in range(cuts_sequence.get_dimensions_number()):
    genes_per_dimension.append(len(cuts_sequence.get_dimension(dimension)))

genes_number = 0
for num in genes_per_dimension:
    genes_number += num

population_size = 2 * genes_number

mutation_rate = 1 / genes_number
# crossover = 1 - mutation_rate

print("Mutation rate calculated: ", mutation_rate)

# genetic_guide = GeneticGuideSequenceProblem(genes_number, mutation_rate, gg_args_test["mating_rate"],
genetic_guide = DeapGeneticGuideSequenceProblem(genes_number, mutation_rate, gg_args_test["mating_rate"],
# genetic_guide = DeapGeneticGuideSequenceProblem(genes_number, mutation_rate, crossover,
                                                gg_args_test["selected_for_tournament"], cuts_sequence,
                                                point_list, genes_per_dimension, m_d, M_d)

a, b = genetic_guide.evolve(population_size, gg_args_test["generations"], "banana")

content = str(a) + "/" + str(b) + "\n"
filecuts.write(content)
'''
filecuts.close()
# winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
