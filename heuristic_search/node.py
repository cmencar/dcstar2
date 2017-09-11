class Node:
    def __init__(self, state, parent_node=None):
        self.state = state
        self.parent = parent_node

    def path(self):
        if self.parent is None:
            return [self.state]
        else:
            return self.parent.path() + [self.state]
