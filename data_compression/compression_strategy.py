from abc import ABC, abstractmethod


class compression_strategy(ABC):

    @abstractmethod
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def algorithm(self):
        pass
