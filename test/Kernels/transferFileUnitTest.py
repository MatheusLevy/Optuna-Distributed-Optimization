import sys
sys.path.insert(0, 'src')

from Kernels.transferFile import TransferFileKernel

class TestTransferFileKernel():

    def setup_method(self, method):
        self.host_file= '/home/viplab/Documentos/Optuna-Distributed-Optimization/test/Kernels/file_teste.txt'
        self.remote_machine= "192.168.200.193"
        self.username= "viplab"
        self.password= "viplab321"
        self.ssh_port = 22
        self.remote_file_path = '/backup/file_test.txt'

    def test_create_transfer_file_kernel(self):

        kernel = TransferFileKernel(ssh_port=self.ssh_port,
                                                host_file=self.host_file,
                                                remote_machine=self.remote_machine,
                                                remote_file_path=self.remote_file_path,
                                                username=self.username,
                                                password=self.password
                                                )
        assert isinstance(kernel, TransferFileKernel)
        assert kernel is not None, "O TransferFileKernel não pode ser None"
    
    def test_transfer(self):
        kernel = TransferFileKernel(ssh_port=self.ssh_port,
                                        host_file=self.host_file,
                                        remote_machine=self.remote_machine,
                                        remote_file_path=self.remote_file_path,
                                        username=self.username,
                                        password=self.password
                                        )
        kernel.execute()
