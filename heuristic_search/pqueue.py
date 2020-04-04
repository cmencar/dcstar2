
# Importa la libreria inerente alla gestione di una pila 
import heapq as H

# La classe PriorityQueue definisce una coda con priorità. 
class PriorityQueue:

    # Viene definito il costruttore, definendo le variabili 'max_size',
    # inerente alla massima dimensione della coda, ed heap, inerente 
    # alla pila contenente le informazioni da salvare.
    def __init__(self, max_size=0):

        self.max_size = max_size
        self.heap = []


    # La funzione empty ritorna true se la coda con priorità è vuota, 
    # false altrimenti.
    def empty(self):

        return self.heap == []


    # La funzione put inserisce nell'heap un nuovo oggetto, formato 
    # da un nodo e da un valore di verità, tramite la funzione heappush 
    # della libreria heapq verificando che non superi la massima dimensione 
    # della coda con priorità. 
    # Nel caso in cui essa superi la dimensione massima, allora l'ultimo elemento 
    # inserito viene eliminato.
    def put(self, node):
        
        H.heappush(self.heap, (node, True))
        self._resize()


    # La funzione get acquisisce il primo nodo della coda con priorità 
    # rimuovendolo dalla pila. 
    # Nel caso in cui il nodo non sia valido, ovvero il valore del campo 
    # valid è false allora, in modo ricorsivo, acquisisci il primo elemento
    # della pila (e rimuovendolo da esso) per il quale il valore 
    # del campo valid sia true.
    def get(self):

        (node, valid) = H.heappop(self.heap)
        
        if not valid and not self.empty():
            return self.get()
        else:
            return node


    # La funzione find ricerca un nodo in base allo stato definito. 
    # Scandendo tutti gli elementi di heap si valuta se il valore di valid
    # sia true e se lo stato inserito viene trovato allora ritorna il valore del nodo. 
    # Se non trova nulla allora ritorna None.
    def find(self, state):
        
        for (estimated_node, valid) in self.heap:
        
            if valid and estimated_node[-1].state == state:
                return estimated_node
        
        return None


    # La funzione remove rimuove un nodo in base a quello inserito. 
    # Per rimozione si intende il settaggio del valore di verità 
    # dell'oggetto in questione a false.
    # La funzione, pertanto, ricerca il nodo desiderato tra quelli presenti
    # nell'heap e se lo trova setta il valore di verita a false, 
    # uscendo dalla funzione.
    def remove(self, node_to_remove):
        
        for i in range(len(self.heap)):
        
            (estimated_node, valid) = self.heap[i]
        
            if valid and estimated_node == node_to_remove:
        
                self.heap[i] = (estimated_node, not valid)
                return


    # La funziona resize ridimensiona l'heap nel caso in cui 
    # la sua dimensione supera quella massima definita in partenza. 
    # Nello specifico, finchè la dimensione dell'heap è maggiore 
    # di quella massima allora si rimuove l'elemento a capo della pila 
    # (ovvero l'ultimo elemento della struttura heap).
    def _resize(self):
        
        if self.max_size > 0:
        
            while len(self.heap) > self.max_size:
        
                del self.heap[-1]


