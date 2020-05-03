from abc import ABC, abstractmethod


class Compression(ABC):

    @abstractmethod
    def algorithm(self, unique_y):
        pass
