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
    def install_from_file(self, file_path):
        pass
    
    @abstractmethod
    def __del__(self):
        pass