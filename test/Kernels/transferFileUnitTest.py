import sys
sys.path.insert(0, 'src')

from Kernels.Concrete.sshTransferFileKernel import SSHTranferFileKernel

class TestTransferFileKernel():

    def setup_method(self, method):
        self.host_file= '/home/viplab/Documentos/Optuna-Distributed-Optimization/test/Kernels/file_teste.txt'
        self.remote_machine= "192.168.200.193"
        self.username= "viplab"
        self.password= "viplab321"
        self.ssh_port = 22
        self.remote_file_path = '/backup/file_test.txt'

    def test_CreateKernel(self):
        kernel = SSHTranferFileKernel(ssh_port=self.ssh_port,
                                                host_file_path=self.host_file,
                                                remote_machine=self.remote_machine,
                                                remote_file_path=self.remote_file_path,
                                                username=self.username,
                                                password=self.password)
        assert isinstance(kernel, SSHTranferFileKernel)
        assert kernel is not None, "O TransferFileKernel não pode ser None"
    
    def test_tranferFromHostToRemote(self):
        kernel = SSHTranferFileKernel(ssh_port=self.ssh_port,
                                                host_file_path=self.host_file,
                                                remote_machine=self.remote_machine,
                                                remote_file_path=self.remote_file_path,
                                                username=self.username,
                                                password=self.password)
        kernel.tranferFromHostToRemote()
        del kernel
    
    def test_transferFromRemoteToHost(self):
        self.host_file= '/backup/remote_file.txt'
        self.remote_file_path= '/backup/remote_file.txt'
        kernel = SSHTranferFileKernel(ssh_port=self.ssh_port,
                                                host_file_path=self.host_file,
                                                remote_machine=self.remote_machine,
                                                remote_file_path=self.remote_file_path,
                                                username=self.username,
                                                password=self.password)
        kernel.transferFromRemoteToHost()