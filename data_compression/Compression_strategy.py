from abc import ABC, abstractmethod


class Compression_strategy(ABC):

    @abstractmethod
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def algorithm(self):
        pass
