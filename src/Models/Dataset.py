import sys
from Kernels.Strategy.machineKernel import MachineKernel
sys.path.insert(0, 'src')

class Dataset():
    def __init__(self, name: str, machine_kernel: MachineKernel, local_dataset_path:str, envs: dict= None):
        self.name = name
        self.machine_kernel = machine_kernel
        self.dataset_path = local_dataset_path
        self.enviroments= envs
        self.size = self._get_size()
        
    def get_username(self):
        return self.machine_kernel.username
    
    def get_password(self):
        return self.machine_kernel.password
    
    def get_ssh(self):
        return self.machine_kernel.ssh
    
    def get_host(self):
        return self.machine_kernel.host
    
    def _get_size(self):
        return self.machine_kernel.get_folder_size(self.dataset_path)