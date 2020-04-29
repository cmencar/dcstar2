from abc import ABC, abstractmethod
from typing import List


class compression_algorithm(ABC):

    @abstractmethod
    def init_prot(self, unique_y):
        pass

    @abstractmethod
    def vector_quantization(self, p_init):
        pass
