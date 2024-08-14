import sys
sys.path.insert(0, 'src')
from Models import Machine
from Modules.TransferFileModule import TransferFileModule

class MachinaryModule():
    def __init__(self,
                machine_list,
                dataset):
        self.machines = []
        for machine_dict in machine_list:
            machine = self._create_machine(machine_dict, dataset)
            machine.start()
            self.machines.append(machine)

    def _create_machine(self, machine_dict, dataset):
        return Machine(machine_dict["username"],
                       machine_dict["password"],
                       machine_dict["host"],
                       machine_dict["ssh_port"],
                       dataset,
                       partition=machine_dict["partition"],
                       local_dataset_path=machine_dict["local_dataset_path"],
                                            )
    def _create_transferFileModule(self):
        return TransferFileModule()

    # def _create_transfileKernel(self):
        
    def get_online_machines(self):
        return [ machine for machine in self.machines if machine.online]
    
    def has_available_gpu(self, machine):
        gpus = machine.gpu_is_used()
        return any(gpu['in_use'] == False for gpu in gpus)
                
    def __del__(self):
        del self.machines
