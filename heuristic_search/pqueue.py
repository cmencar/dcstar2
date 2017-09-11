import heapq as hq


class PriorityQueue:
    def __init__(self, max_size=0):
        self.max_size = max_size
        self.heap = []

    def empty(self):
        return self.heap == []

    def put(self, node):
        hq.heappush(self.heap, (node, True))
        self._resize()

    def get(self):
        (node, valid) = hq.heappop(self.heap)
        if not valid:
            return self.get()
        else:
            return node

    def find(self, state):
        for (estimated_node, valid) in self.heap:
            if valid and estimated_node[-1].state == state:
                return estimated_node
        return None

    def remove(self, node_to_remove):
        for i in range(len(self.heap)):
            (estimated_node, valid) = self.heap[i]
            if valid and estimated_node == node_to_remove:
                self.heap[i] = (estimated_node, not valid)
                return

    def _resize(self):
        if self.max_size > 0:
            while len(self.heap) > self.max_size:
                del self.heap[-1]


