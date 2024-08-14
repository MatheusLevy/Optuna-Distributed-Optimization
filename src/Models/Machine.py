import sys
sys.path.insert(0, 'src')
from Kernels.Strategy.machineKernel import MachineKernel
from Modules.TransferFileModule import TransferFileModule
from Models import Dataset


class Machine():
    def __init__(self, username: str, password: str, host: str, ssh_port: int, dataset: Dataset, partition:str="/", local_dataset_path="/" ,online:bool=False,
                  transferModule:TransferFileModule= None, machineKernel:MachineKernel= None):
        self.username=username
        self.password=password
        self.host=host
        self.ssh_port=ssh_port
        self.online=online
        self.dataset=dataset
        self.partition=partition
        self.local_dataset_path=local_dataset_path
        self.MachineKernel=machineKernel
        self.TransferModule=transferModule


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