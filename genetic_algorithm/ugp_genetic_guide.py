# -*- coding: utf-8 -*-

# Classe per l'acquisizione e dell'uso dell'individuo 
# creato tramite UGP
class UGPGeneticGuide:
    
    # costruttore della classe
    def __init__ (self, file_path):
        
        # definizione del genoma (l'individuo vero e proprio)
        self.genome = None
        
        # creazione dell'individuo
        self.create(file_path)
    
    
    # Metodo per la formattazione corretta dell'individuo
    # L'individuo potrebbe contenere ripetizioni e/o underscore
    # che non hanno alcua utilità nella computazione in A*
    def formatter(self, individual_genome):
        
        # definizione di una lista di stati
        listed_genome = list()
        
        # se il gene è uno stato valido e non è ripetuto
        for gene in individual_genome:
            if gene not in listed_genome and gene != "_":
                
                # inserisce il gene nella lista ed aumenta il numero di stati
                listed_genome.append(gene)
                
        # definizione dell'individuo come stringa
        self.genome = ''.join(listed_genome)
    
    
    # Funzione per la creazione degli individui
    def create(self, file_path):
        
        # apertura del file dell'individuo
        file = open(file_path, "r")
        
        # lettura dell'individuo
        individual_genome = file.readline();
        
        # chiusura del file
        file.close()
        
        # formattazione del genoma analizzando e 
        # correggendo il genoma dell'individuo
        self.formatter(individual_genome)
