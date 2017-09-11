from discretization.cutset import CutSet


class DiscretizationProblem:
    def __init__(self, cut_base):
        self.start_state = CutSet(cut_base)
        self.unique_successors = True

    def g(self, path):
        cut_set = path[-1]
        g1 = cut_set.num_of_cuts()
        g2 = -cut_set.min_cut_space
        g3 = cut_set.nnum_of_active_dims()
        return g1, g2, g3
    
    def h(self, cut_set):
        return cut_set.min_cuts_to_add()

    def estimate_cost(self, path):
        (g1, g2, g3) = self.g(self, path)
        h1 = self.h(self, path[-1])
        return g1 + h1, g2, g3

    def goal(self, cut_set):
        return cut_set.pure()

    def successors(self, cut_set):
        return cut_set.successors()
