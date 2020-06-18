from cut_sequences.dimensional_sequence_numeric import DimensionalSequenceNumeric
from genetic_algorithm.deap_genetic_guide_sequence_problem import DeapGeneticGuideSequenceProblem
from heuristic_search.prototypes_creators import PrototypesCreator

filename = "created point lists/shuttle_100_21_norm.json"
loader = PrototypesCreator()
point_list, m_d, M_d = loader.load(filename)

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

gg_args_test = {
    "selected_for_tournament": 5,
    "generations": 100,
    "mating_rate": 0.7
}

genes_per_dimension = list()
for dimension in range(cuts_sequence.get_dimensions_number()):
    genes_per_dimension.append(len(cuts_sequence.get_dimension(dimension)))

genes_number = 0
for num in genes_per_dimension:
    genes_number += num

population_size = 2 * genes_number

mutation_rate = 1 / genes_number
# TODO mutation_rate prefissati, test da togliere
# mutation_rate = 0.3
# mutation_rate = 0.2
# mutation_rate = 0.15
# mutation_rate = 0.1
# mutation_rate = 0.9

print("Mutation rate calculated: ", mutation_rate)

genetic_guide = DeapGeneticGuideSequenceProblem(genes_number, mutation_rate, gg_args_test["mating_rate"],
                                                gg_args_test["selected_for_tournament"], cuts_sequence,
                                                point_list, genes_per_dimension, m_d, M_d)

genetic_guide.evolve(population_size, gg_args_test["generations"])
