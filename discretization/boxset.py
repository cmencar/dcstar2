class BoxSet:
    def __init__(self, cut_set, data_set):
        self.augmented_cut_set = self._augment_cut_set(cut_set, data_set)
        self.data_set = data_set
        self.box_set = self._generate_box_set()

    def _augment_cut_set(self, cut_set, data_set):
        return [[data_set.features[i]["min"]] + cut_set[i] + [data_set.features[i]["max"]] for i in range(data_set.dimensions)]

    def _generate_box_set(self):
        box_set = {}
        for sample in self.data_set.samples:
            box = []
            for i in range(self.data_set.dimensions):
                j = 0
                while self.augmented_cut_set[i][j] <= sample.data[i]:
                    j += 1
                box[i] = (self.augmented_cut_set[j-1], self.augmented_cut_set[j])
            box_set[box] = sample.label

        return box_set
