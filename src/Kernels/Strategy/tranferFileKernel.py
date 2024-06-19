"""
    Transfer File Strategy Kernel
    @MatheusLevy
"""
from abc import ABC, abstractmethod

class TransferFileKernel(ABC):

    @abstractmethod
    def tranferFromHostToRemote(self):
        pass
    
    @abstractmethod
    def transferFromRemoteToHost(self):
        pass

    @abstractmethod
    def __del__(self):
        pass
