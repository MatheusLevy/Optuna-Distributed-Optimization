import sys
sys.path.insert(0, 'src')
from Kernels.Strategy.tranferFileKernel import TransferFileKernel
from Kernels.Strategy.machineKernel import MachineKernel
from Models.Dataset import Dataset

# Transfer File Pipeline:
# 1. Verificar se existe espaço na maquina de origem
#   -> Se não existir capturar exceção e tratar
# 2. Transferir arquivo
#   -> Se ocorrer erro capturar e tratar

class TransferFileModule():
    def __init__(self, dataset: Dataset, destinyMachineKernel: MachineKernel, transferFileKernel:TransferFileKernel):
        self.dataset_source = dataset
        self.dstMachine = destinyMachineKernel
        self.transferFileKernel = transferFileKernel

    def is_space_on_remote(self, file_bytes, partition_free_bytes):
        return (int(partition_free_bytes) > int(file_bytes))
    
    def bytes_to_gb(self, bytes_value):
        return bytes_value / (1024 ** 3)
    
    def transfer(self):
        # verificar se existe espaço na maquina de destino
        dataset_size = self.dataset_source.machine_kernel.get_folder_size(self.dataset_source.dataset_path)
        space_on_remote = self.dstMachine.get_partition_info()
        if not self.is_space_on_remote(dataset_size, space_on_remote):
            return -1
        self.transferFileKernel.transferFile(self.dataset_source, self.dstMachine)
        return "ok"