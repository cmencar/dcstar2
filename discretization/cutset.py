import math


class CutSet:
    def __init__(self, cut_base, cut_set=None):
        self.cut_base = cut_base
        self.cut_set = cut_set or [[] and cut_base_1 for cut_base_1 in cut_base]

    def num_of_cuts(self):
        return sum([len(cut_set_1) for cut_set_1 in self.cut_set])

    def min_cut_space(self):
        return min(
                [min([(cut_set_1[i+1]-cut_set_1[i]) for i in range(len(cut_set_1)-1)])
                 for cut_set_1 in self.cut_set if cut_set_1 != []] + [math.inf]
                )

    def num_of_active_dims(self):
        return sum([(1 if len(cut_set_1) > 0 else 0) for cut_set_1 in self.cut_set])

    def successors(self):
        new_cuts = [set(self.cut_base[i]).difference(set(self.cut_set[i])) for i in range(len(self.cut_base))]
        new_cuts_purged = [
            [nc for nc in new_cuts[i] if self.cut_set[i] == [] or nc > self.cut_set[i][-1]]
            for i in range(len(self.cut_base))
            ]

        generated_successors = []
        for i in range(len(self.cut_base)):
            for nc in new_cuts_purged[i]:
                successor = self.cut_set.copy()
                successor[i] += [nc]
                generated_successors.append(successor)

        return generated_successors
