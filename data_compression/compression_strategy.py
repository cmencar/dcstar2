from abc import ABC, abstractmethod


class compression_strategy(ABC):

    @abstractmethod
    def algorithm(self, unique_y):
        pass
