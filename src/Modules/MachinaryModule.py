import sys
sys.path.insert(0, 'src')
from Models import Machine
from Modules.TransferFileModule import TransferFileModule
class MachinaryModule():
    def __init__(self,
                machines,
                dataset,
                database):
        self.machines= machines
        self.dataset= dataset
        self.database = database
    
    def _start_machines(self):
        for machine in self.machines:
            machine.start()
    def _transferDataset(self, machine):
        transferModule = TransferFileModule(dataset=self.dataset, destinyMachine=machine, transferFileKernel=machine.TransferFileKernel)
        transferModule.transferDataset()

    def run(self):
        self._start_machines()
        self.database.buildDatabase()
        for machine in self.machines:
            if not machine.has_space():
                print(f"Máquina {machine.name} não tem espaço de armazenamento")
                continue
            machine.PakageManagerKernel.installEnv()
            self._transferDataset(machine)

        
    def get_online_machines(self):
        return [ machine for machine in self.machines if machine.online]
    
    def has_available_gpu(self, machine):
        gpus = machine.gpu_is_used()
        return any(gpu['in_use'] == False for gpu in gpus)
                
    def __del__(self):
        del self.machines
