from abc import ABC, abstractmethod

class Kernel(ABC):
    
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def __del__(self):
        pass