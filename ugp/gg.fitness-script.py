import sys

# dimensione massima dell'individuo
INDIVIDUAL_SIZE = 16

# apertura del documento contenente i file .in da valutare
# da parte di UGP.exe
individuals_to_evaluate_file = open("individualsToEvaluate.txt","r")

# lettura di tutti i file .in da valutare
individual_files = individuals_to_evaluate_file.readlines();

# chiusura del documento
individuals_to_evaluate_file.close()

# per ogni riga trovata (ovvero per ogni file da valutare)
for file in individual_files:
    
    # elimina il carattere di backslash dal nome del file
    if file.endswith('\n'):
        file = file[:-1]
        
    # apertura in lettura del file dell'individuo da valutare
    individual_file = open(file, "r") 
    
    # acquisizione del genoma dell'individuo
    individual = individual_file.readline();
    
    # chiusura del file dell'individuo
    individual_file.close()

    # definizione di una lista per l'individuo formattato
    formatted_individual = list()
    
    # definizione del contatore degli stati dell'individuo
    i = 0

    # per ogni gene nell'individuo
    for gene in individual:

        # se il gene è uno stato valido e non è ripetuto
        if gene != "_" and gene != "\n":
            if gene not in formatted_individual:
            
                # inserisce il gene nella lista ed aumenta il numero di stati
                formatted_individual.append(gene)
                i = i + 1

    # definizione dell'individuo come stringa
    individual = ''.join(formatted_individual)   

    # definizione del valore della fitness
    fitness = i / INDIVIDUAL_SIZE
    
    
    # apertura del file della fitness
    fitnessFile = open("fitness.out","a")
    
    # scrittura della fitness nel file
    fitnessFile.write(str(fitness))
    
    # chiusura del file
    fitnessFile.close()


    # apertura del file dell'individuo
    individual_file = open(file, "w") 
    
    # scrittura dell'individuo corretto senza caratteri inutili
    individual_file.write(individual)
    
     # chiusura del file
    individual_file.close()
    
    
    # apertura del file dell'individui valutati
    evaluated_individual = open("evaluatedIndividual.txt", "a")
    
    # scrittura dell'individuo nella lista degli individui valutati
    evaluated_individual.write(individual + ", " + str(fitness) + " \n")
    
    # chiusura del file
    evaluated_individual.close()
    
