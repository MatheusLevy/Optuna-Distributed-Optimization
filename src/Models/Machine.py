import sys
sys.path.insert(0, 'src')
from Kernels.Strategy.machineKernel import MachineKernel
from Kernels.Strategy.packageManager import PackageManager
from Models import Dataset


class Machine():
    def __init__(self, name:str, dataset: Dataset, partition:str="/", local_dataset_path="/", online:bool=False, machineKernel:MachineKernel= None, packageManagerKernel: PackageManager= None):
        self.online=online
        self.dataset=dataset
        self.partition=partition
        self.local_dataset_path=local_dataset_path
        self.MachineKernel=machineKernel
        self.PakageManagerKernel = packageManagerKernel
        self.name=name
    
    def get_username(self):
        return self.MachineKernel.username
    
    def get_password(self):
        return self.MachineKernel.password
    
    def get_ssh(self):
        return self.MachineKernel.ssh
    
    def get_host(self):
        return self.MachineKernel.host