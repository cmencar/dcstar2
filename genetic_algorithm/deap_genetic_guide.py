# -*- coding: utf-8 -*-

from deap import creator, base, tools, algorithms

from genetic_algorithm.genetic_evolution import GeneticEvolution
from cut_sequences.cuts_sequence import CutsSequence
from cut_sequences.selected_cuts_sequence import SelectedCutsSequence
from cut_sequences.dimensional_sequence_binary import DimensionalSequenceBinary


# Classe per l'uso della soluzione genetica inerente
# all'algoritmo A* usufruendo della libreria DEAP
class DeapGeneticGuide(GeneticEvolution):

    # definizione del costruttore della classe
    # Al costruttore vanno passati parametri come le funzioni di
    # valutazione e generazione degli indicìvidui (caratteristiche
    # intrinseche del Problem), la dimensione dell'individuo
    # (il numero di attributi per ogni individuo), la probabilità
    # di mutazione inerente il singolo attributo dell'individuo e
    # il numero di individui selezionati nella fase di selezione
    # degli individui migliori (selezione per torneo)
    def __init__(self, evaluate_fun, generate_fun, individual_size,
                 mutation_rate, mating_rate, selected_individuals, cuts_sequence, points_list, elements_per_dimension):

        # definizione della probabitlià di mutazione dell'individuo
        self.mutation_rate = mutation_rate

        # definizione della probabitlià di accoppiamento dell'individuo
        self.mating_rate = mating_rate

        # creazione dell'oggetto per la definizione del massmo valore del fitness
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))

        # creazione dell'oggetto per la definizione dell'individuo
        creator.create("Individual", list, fitness=creator.FitnessMax)

        # definizione del toolbox per i metodi necessari
        self.toolbox = base.Toolbox()

        # definizione dell'individuo, il quale viene generato direttamente
        # dalla funzione definita da un particolare tipo di Problem
        self.toolbox.register("individual", generate_fun, creator.Individual, individual_size)

        # definizioen della struttura che permette il salvataggio dell'insieme
        # di individui come popolazione (vengono valutati come una lista
        # di individui)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        # definizione del metodo di accoppiamento tra individui definendo
        # un uniform partially matched crossover sugli individui.
        self.toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=0)

        # definizione del metodo di mutazione dell'individuo figlio
        # tramite un rimescolamento degli attributi atomici, con una
        # percentuale di mutazione pari a mutation_rate
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=mutation_rate)

        # definizione del metodo di selezione degli individui tramite
        # una competizione formata tra un numero di individui pari a
        # tournament_selected
        self.toolbox.register("select", tools.selTournament, tournsize=selected_individuals)

        # definizione del metodo di valutazione degli individui.
        # Viene passata la funzione di valutazione implementata
        # specificatamente da un tipo di problem
        self.toolbox.register("evaluate", evaluate_fun)

        self.T_d = cuts_sequence
        self.points_list = points_list
        self.individual_size = individual_size
        self.elements_per_dimension = elements_per_dimension

    # Metodo per la valutazione dell'individuo
    def evaluate(self, individual):
        pass

    # Metodo per la generazione dell'individuo
    def generate(self):
        pass

    # Metodo per la generazione e la restituzione dei migliori individui
    # secondo l'algoritmo genetico
    def evolve(self, population_size, generations, selected_best, T_d, individual_size):

        # definisce l'insieme degli indivdui invocando il metodo population.
        # Tale metodo crea un insieme di individui la cui quantità è pari
        # a population_size e vengono definiti secondo la generate_fun passata
        # in fase di creazione della classe
        population = self.toolbox.population(n=population_size)
        '''
        # conversione da sequenze dimensionali a liste monolitiche
        converted_genome = list()
        converted_population = list()
        for genome_number in range(len(population)):
            converted_genome.clear()
            for dimension in population[genome_number]:
                for gene in dimension:
                    converted_genome.append(gene)
            converted_population.append(converted_genome.copy())
        '''

        # per ogni generazione
        for epoch in range(generations):

            # la generazione della progenie viene definita tramite l'algoritmo
            # di varAnd, in cui vengono passati la popolazione degli individui,
            # la probabilità di accoppiamento e dimutazione dell'individuo.
            # Inoltre, utilizza l'insieme delle funzioni di servizio, definite
            # in precedenza nel toolbox per effettuare il crossover e
            # la mutazione (la valutazione e la selezione vengono effettuate
            # con le funzioni passate al costruttore)
            offspring = algorithms.varAnd(population,
                                          self.toolbox,
                                          self.mating_rate,
                                          self.mutation_rate)

            # definizione di una mappa che conterrà i valori delle
            # valutazioni degli individui della progenie
            son_fitness = list()
            for son in offspring:
                son_fitness.append(self.fitness(son, self.T_d, self.points_list))
            # fitness = self.toolbox.map(son_fitness, offspring)

            # definizione di una mappatura tra ogni individuo della
            # progenie e la sua valutazione
            for fit, ind in zip(son_fitness, offspring):
                ind.fitness.value = fit

            # infine, si scelgono un'insieme di individui dalla
            # progenie di grandezza pari alla dimensione della popolazione
            # La selezione viene definita dall'algoritmo di selezione per torneo
            # suun numero pari a selected_individual individui
            population = self.toolbox.select(offspring, k=len(population))

        # Dopo il completamento di tutte le generazioni vengono selezionati
        # un insieme di individui, il cui numero è pari a selected_best,
        # la cui fitness è in assoluto la migliore della popolazione
        return tools.selBest(population, selected_best, fit_attr="fitness.value")

    def fitness(self, individual, T_d, points_list):
        return (1 - self.toolbox.evaluate(individual)) * pow(self.pureness(individual, T_d, points_list,
                                                                           self.elements_per_dimension), 5)

    # Funzione che deifince la purezza di un dato genoma
    def pureness(self, individual, T_d, points_list, elements_per_dimension, m_d=0, M_d=1):
        # inizializzazione sequenze
        S_d = SelectedCutsSequence()
        S_d_b = DimensionalSequenceBinary()

        # conversione da lista monolitica a sequenza
        converted_individual = self.from_monolithic_pop_to_multidim_pop(individual, elements_per_dimension)

        # creazione della sequenza dimensionale binaria e relativa selezione di tagli dal genoma
        S_d_b.from_binary(converted_individual)
        S_d.from_binary(T_d, S_d_b)

        # creazione del set di hyperboxes
        hyperboxes = S_d.generate_hyperboxes_set(points_list, m_d, M_d)

        # calcolo del rapporto tra li numero di hyperbox puri e il numero complessivo di hyperbox
        return hyperboxes.get_pure_hyperboxes_number() / hyperboxes.get_hyperboxes_number()

    def from_multidim_pop_to_monolithic_pop(self, population):
        converted_genome = list()
        converted_population = list()
        for genome_number in range(len(population)):
            converted_genome.clear()
            for dimension in population[genome_number]:
                for gene in dimension:
                    converted_genome.append(gene)
            converted_population.append(converted_genome.copy())
        return converted_population

    def from_monolithic_pop_to_multidim_pop(self, individual, individual_size):
        # riconversione da lista monolitica a "sequenza di tagli dimensionali"
        # list_of_sequences = list()
        sequence = list()
        dimension = list()
        '''
        for individual in population: -- LISTE MULTIDIMENSIONALI
            sequence.clear()
            offset = 0
            i = 0
            for num_elem in individual_size:
                dimension.clear()
                offset = offset + num_elem
                while i < offset:
                    dimension.append(individual[i])
                    i += 1
                sequence.append(dimension.copy())
            list_of_sequences.append(sequence.copy())
        return list_of_sequences
        '''
        offset = 0
        i = 0
        for num_elem in individual_size:
            dimension.clear()
            offset = offset + num_elem
            while i < offset:
                dimension.append(individual[i])
                i += 1
            sequence.append(dimension.copy())
        return sequence
