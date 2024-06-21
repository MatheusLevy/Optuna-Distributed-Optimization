"""
    Package Manager Strategy Kernel
    @MatheusLevy
"""
from abc import ABC, abstractmethod

class PackageManager(ABC):
    @abstractmethod
    def install(self, package_name, version):
        pass

    @abstractmethod
    def uninstall(self, package_name):
        pass

    @abstractmethod
    def __del__(self):
        pass