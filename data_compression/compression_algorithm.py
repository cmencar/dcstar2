from abc import ABC, abstractmethod


class compression_algorithm(ABC):

    @abstractmethod
    def init_prot(self, unique_y):
        pass

    @abstractmethod
    def vector_quantization(self, p_init):
        pass
