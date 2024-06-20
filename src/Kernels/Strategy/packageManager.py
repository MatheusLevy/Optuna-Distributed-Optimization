"""
    Package Manager Strategy Kernel
    @MatheusLevy
"""
from abc import ABC, abstractmethod

class PackageManager(ABC):
    @abstractmethod
    def install(self, host, package_name, version):
        pass

    @abstractmethod
    def uninstall(self, host, package_name):
        pass