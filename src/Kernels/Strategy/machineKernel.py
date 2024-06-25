"""
    Package Manager Strategy Kernel
    @MatheusLevy
"""
from abc import ABC, abstractmethod

class MachineKernel(ABC):

    @abstractmethod
    def get_partition_info(self, partition="/"):
        pass

    @abstractmethod
    def get_memmory_info(self):
        pass

    @abstractmethod
    def get_CPU_info(self):
        pass

    @abstractmethod
    def get_GPU_info(self):
        pass

    @abstractmethod
    def get_process_info(self, pid):
        pass

    @abstractmethod
    def kill_process_info(self, pid):
        pass

    @abstractmethod
    def get_process_on_gpu(self):
        pass

    @abstractmethod
    def gpu_is_used(self):
        pass