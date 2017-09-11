import pandas as pd



class Dataset:
    def __init__(self, file_name)
        self.file_name = file_name
        self.data_frame = pd.read_csv(file_name)
        self.dimensions = self.data_frame.shape[1] - 1 #remove label column
        self.features = {}

