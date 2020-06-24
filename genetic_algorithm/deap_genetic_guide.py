# -*- coding: utf-8 -*-

from deap import creator, base, tools, algorithms

from genetic_algorithm.genetic_evolution import GeneticEvolution

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
                 mutation_rate, mating_rate, selected_individuals):
        
        # definizione della probabitlià di mutazione dell'individuo
        self.mutation_rate = mutation_rate
        
        # definizione della probabitlià di accoppiamento dell'individuo
        self.mating_rate = mating_rate
        
        # creazione dell'oggetto per la definizione del massmo valore del fitness
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        
        # creazione dell'oggetto per la definizione dell'individuo
        creator.create("Individual", list, fitness = creator.FitnessMax)

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
        self.toolbox.register("mate", tools.cxUniformPartialyMatched, indpb = 0)
        
        # definizione del metodo di mutazione dell'individuo figlio
        # tramite un rimescolamento degli attributi atomici, con una
        # percentuale di mutazione pari a mutation_rate
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb = mutation_rate)
        
        # definizione del metodo di selezione degli individui tramite 
        # una competizione formata tra un numero di individui pari a
        # tournament_selected
        self.toolbox.register("select", tools.selTournament, tournsize = selected_individuals)
        
        # definizione del metodo di valutazione degli individui.
        # Viene passata la funzione di valutazione implementata
        # specificatamente da un tipo di problem
        self.toolbox.register("evaluate", evaluate_fun)
           
        
    # Metodo per la valutazione dell'individuo
    def evaluate(self, individual):
        pass
    
    
    # Metodo per la generazione dell'individuo
    def generate(self):
        pass


    # Metodo per la generazione e la restituzione dei migliori individui
    # secondo l'algoritmo genetico
    def evolve(self, population_size, generations, selected_best):
        
        # definisce l'insieme degli indivdui invocando il metodo population.
        # Tale metodo crea un insieme di individui la cui quantità è pari
        # a population_size e vengono definiti secondo la generate_fun passata
        # in fase di creazione della classe
        population = self.toolbox.population(n = population_size)
        
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
            
            # per ogni figlio nella progenie si valuta se possiede dei geni
            # ripetuti che possono compromettere il risultato finale
            for son in offspring:
                
                # il figlio rivalutato sarà colui che non possiede ridondanze 
                # tra gli attributi
                revaluted_son = []
                
                # per ogni attributo del figlio analizzato
                for gene in son:
                    
                    # se l'attributo non è stato inserito nel
                    # figlio rivalutato, allora non è una ridondanza
                    if gene not in revaluted_son:
                        revaluted_son.append(gene)
                        
                    # altrimenti essa è definita come una ridondanza e
                    # sarà epurata dal figlio rivalutato
                    else:
                        revaluted_son.append(0)
                        
                # il figlio rivalutato sarà parte della progenie da
                # analizzare nella nuova generazione
                son = revaluted_son
                
            # definizione di una mappa che conterrà i valori delle
            # valutazioni degli individui della progenie
            fitness = self.toolbox.map(self.toolbox.evaluate, offspring)
            
            # definizione di una mappatura tra ogni individuo della
            # progenie e la sua valutazione
            for fit, ind in zip(fitness, offspring):
                ind.fitness.value = fit
                
            # infine, si scelgono un'insieme di individui dalla
            # progenie di grandezza pari alla dimensione della popolazione
            # La selezione viene definita dall'algoritmo di selezione per torneo
            # suun numero pari a selected_individual individui
            population = self.toolbox.select(offspring, k = len(population))
            
        
        # Dopo il completamento di tutte le generazioni vengono selezionati
        # un insieme di individui, il cui numero è pari a selected_best,
        # la cui fitness è in assoluto la migliore della popolazione
        return tools.selBest(population, selected_best, fit_attr="fitness.value")
        
        


        
        