import sys
sys.path.insert(0, 'src')

class TransferFileModule:
    def __init__(self, dataset, destinyMachine, transferFileKernel):
        self.dataset_source = dataset
        self.dstMachine = destinyMachine
        self.transferFileKernel = transferFileKernel

    def is_space_on_remote(self, file_bytes, partition_free_bytes):
        return int(partition_free_bytes) > int(file_bytes)
    
    def bytes_to_gb(self, bytes_value):
        return bytes_value / (1024 ** 3)
    
    def transfer(self):
        # Importing here to avoid circular import issues
        from Kernels.Strategy.tranferFileKernel import TransferFileKernel
        from Models.Dataset import Dataset
        from Models.Machine import Machine

        # Verifying if there's enough space on the destination machine
        dataset_size = self.dataset_source.machine_kernel.get_folder_size(self.dataset_source.dataset_path)
        space_on_remote = self.dstMachine.MachineKernel.get_partition_info()['free_space']
        if not self.is_space_on_remote(dataset_size, space_on_remote):
            return -1
        self.transferFileKernel.transferFile(self.dataset_source, self.dstMachine)
        return "ok"
