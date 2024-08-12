import sys
sys.path.insert(0, 'src')
from Kernels.Concrete.ubuntuMachineKernel import UbuntoMachineKernel
from Kernels.Exceptions.MachineKernelException import MachineKernelException
from Kernels.Strategy.tranferFileKernel import TransferFileKernel
from Modules.TransferFileModule import TransferFileModule

class Machine():
    def __init__(self, username, password, host, ssh_port, dataset, online=False, transferModule= None ):
        self.username = username
        self.password = password
        self.host = host
        self.ssh_port = ssh_port
        self.online = online
        self.dataset= dataset
        self.MachineKernel = None
        self.TransferModule = transferModule
        
    def _start_MachineKernel(self):
        try:
            self.MachineKernel = UbuntoMachineKernel(username=self.username,
                                       password=self.password,
                                       host=self.host,
                                       ssh_port=self.ssh_port)
            self.online = True
            print(f"(OK) Connected to {self.host} on port {self.password}" )
        except MachineKernelException as e:
            print(f"(FAIL) Machine {self.username} in addr {self.host} set Offline due to: {e.error}")
        return self.kernel

    def _start_TransferFileModule(self):
        try:
            self.TransferModule = self._transferFileModule()
        except Exception as e:
            print(f"(FAIL) Machine {self.username} in addr {self.host} set Offline due to {e}")

    def start(self):
        self._start_MachineKernel()
        self._start_TransferFileModule()

    def _transferFileModule(self):
        trasferFileKernel = TransferFileKernel(remote_machine=self.dataset.machine_ip,
                                               remote_file_path=self.dataset.path,
                                               username=self.dataset.machine_username,
                                               password=self.dataset.machine_password,
                                               host_file_path=self.dataset.path,
                                               ssh_port=self.data.machine_ssh_port)
        sourceMachineKernel = self.dataset.kernel

        remote_machine_partition_info = self.get_partition_info(self.dataset.partition)
        file_size_bytes = sourceMachineKernel.get_folder_size(self.dataset.path)
        remote_machine_partition_free_space = remote_machine_partition_info['free_space']
        self.TransferFileModule = TransferFileModule(transFileKernel=trasferFileKernel,
                                  machineKernelDestiny=self.MachineKernel,
                                  machineKernelSource=sourceMachineKernel
                                  )
        self.hasSpaceInPartition = self.TransferFileModule.is_space_on_remote(file_size_bytes, remote_machine_partition_free_space)

class MachinaryModule():
    def __init__(self,
                machine_list,
                dataset):
        self.machines = []
        for machine_dict in machine_list:
            machine = self._create_machine(machine_dict, dataset)
            machine.start_kernel()
            self.machines.append(machine)

    def _create_machine(self, machine_dict, dataset):
        return Machine(username=machine_dict['username'],
                       password=machine_dict['password'],
                       host=machine_dict['host'],
                       ssh_port=machine_dict['ssh_port'],
                       dataset=dataset
                       )
        
    def get_online_machines(self):
        return [ machine for machine in self.machines if machine.online]
    
    def has_available_gpu(self, machine):
        gpus = machine.gpu_is_used()
        return any(gpu['in_use'] == False for gpu in gpus)
                
    def __del__(self):
        del self.machines
