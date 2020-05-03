from abc import ABC, abstractmethod


class compression_algorithm(ABC):

    @abstractmethod
    def algorithm(self, unique_y):
        pass
