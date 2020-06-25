import heapq as H


# Class that define a priority queue containing several nodes ordered by priority value
class PriorityQueue:

    # Class constructor
    # @max_size: priority queue max dimension
    def __init__(self, max_size = 0):
        self.max_size = max_size
        self.heap = []


    # Method for acquiring if the priority queue is empty
    def empty(self):
        return self.heap == []


    # Method for inserting a node in the priority queue, placing it in the right position in the order relation
    # @node: node to be inserted in priority queue
    def put(self, node):
        H.heappush(self.heap, (node, True))
        self._resize()


    # Method for acquiring a node from priority queue. The node returned is the first element in the order relation
    # and, consequently, the one with the greatest priority value
    def get(self):
        (node, valid) = H.heappop(self.heap)
        if not valid:
            return self.get()
        else:
            return node


    # Method for acquiring the node referring to passed state.
    # @state: basis on which to search
    def find(self, state):
        for (estimated_node, valid) in self.heap:
            if valid and estimated_node[-1].state == state:
                return estimated_node
        return None


    # Method for removing a particular node
    # @node_to_remove: node to be removed
    def remove(self, node_to_remove):
        for i in range(len(self.heap)):
            (estimated_node, valid) = self.heap[i]
            if valid and estimated_node == node_to_remove:
                self.heap[i] = (estimated_node, not valid)
                return
                

    # Method for resizing the priority queue. If the defined max_size is greater than zero the operation is made,
    # otherwise the structure remain unchanged
    def _resize(self):
        if self.max_size > 0:
            while len(self.heap) > self.max_size:
                del self.heap[-1]
