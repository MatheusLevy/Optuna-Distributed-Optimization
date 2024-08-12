import sys
sys.path.insert(0, 'src')
from Kernels.Strategy.tranferFileKernel import TransferFileKernel
from Kernels.Strategy.machineKernel import MachineKernel

# Transfer File Pipeline:
# 1. Verificar se existe espaço na maquina de origem
#   -> Se não existir capturar exceção e tratar
# 2. Transferir arquivo
#   -> Se ocorrer erro capturar e tratar

class TransferFileModule():
    def __init__(self,
                 transFileKernel: TransferFileKernel,
                 machineKernelDestiny: MachineKernel,
                 machineKernelSource: MachineKernel):
        
        self.TransferFilerKernel = transFileKernel
        self.machineKernelDestiny = machineKernelDestiny
        self.machineKernelSource = machineKernelSource

    def is_space_on_remote(self, file_bytes, partition_free_bytes):
        return (int(partition_free_bytes) > int(file_bytes))
    
    def bytes_to_gb(self, bytes_value):
        return bytes_value / (1024 ** 3)

    def transferFile(self,
                     partition="/"):
        remote_machine_partition_info = self.machineKernelDestiny.get_partition_info(partition)
        file_size_bytes = self.machineKernelSource.get_folder_size(self.TransferFilerKernel.host_file)
        remote_machine_partition_free_space = remote_machine_partition_info['free_space']
        if not self.is_space_on_remote(file_size_bytes, remote_machine_partition_free_space):
            print(f"Não há espaço disponivel na partição {partition} na maquina remota {self.machineKernelDestiny.host}")
            print(f"Espaço Disponivel: {self.bytes_to_gb(int(remote_machine_partition_free_space)):.2f}Gb")
            print(f"Tamanho da transferência: {self.bytes_to_gb(int(file_size_bytes)):.2f}Gb")
            return False
        print("Transferindo Arquivos para o destino...")
        try:
            self.TransferFilerKernel.tranferFromHostToRemote(isFolder=True, verbose=True)
        except Exception as e:
            print("Erro durante a transferência", e)
            return False
        print("Transferencia finalizada")
        return True
    
    def __del__(self):
        del self.TransferFilerKernel
        del self.machineKernelDestiny
        del self.machineKernelSource