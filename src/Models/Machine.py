import sys
sys.path.insert(0, 'src')
from Kernels.Strategy.machineKernel import MachineKernel
from Modules.TransferFileModule import TransferFileModule
from Models import Dataset


class Machine():
    def __init__(self, name:str, dataset: Dataset, partition:str="/", local_dataset_path="/" ,online:bool=False, machineKernel:MachineKernel= None):
        self.online=online
        self.dataset=dataset
        self.partition=partition
        self.local_dataset_path=local_dataset_path
        self.MachineKernel=machineKernel
        self.name=name
    
    def get_username(self):
        return self.MachineKernel.username
    
    def get_password(self):
        return self.MachineKernel.password
    
    def get_ssh(self):
        return self.MachineKernel.ssh
    
    def get_host(self):
        return self.MachineKernel.host

    # def _create_transferFileModule(self):
    #     trasferFileKernel = SSHTranferFileKernel(remote_machine=self.dataset.source_ip,
    #                                            remote_file_path=self.dataset.path,
    #                                            username=self.dataset.machine_username,
    #                                            password=self.dataset.machine_password,
    #                                            host_file_path=self.local_dataset_path,
    #                                            ssh_port=self.dataset.source_ssh)
    #     sourceMachineKernel = self.dataset.kernel

    #     remote_machine_partition_info = self.get_partition_info(self.dataset.partition)
    #     file_size_bytes = sourceMachineKernel.get_folder_size(self.dataset.path)
    #     remote_machine_partition_free_space = remote_machine_partition_info['free_space']
    #     self.TransferFileModule = TransferFileModule(transFileKernel=trasferFileKernel,
    #                               machineKernelDestiny=self.MachineKernel,
    #                               machineKernelSource=sourceMachineKernel
    #                               )
    #     self.hasSpaceInPartition = self.TransferFileModule.is_space_on_remote(file_size_bytes, remote_machine_partition_free_space)