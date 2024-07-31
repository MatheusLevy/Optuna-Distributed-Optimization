import sys
sys.path.insert(0, 'src')
from Modules.TransferFileModule import TransferFileModule
from Kernels.Concrete.sshTransferFileKernel import SSHTranferFileKernel
from Kernels.Concrete.ubuntuMachineKernel import UbuntoMachineKernel

class TestTranferFileModule():
    def setup_method(self, method):
        self.transferFileKernel = SSHTranferFileKernel(
            remote_machine="192.168.200.147",
            remote_file_path="/home/viplab/Documentos/Pasta_Teste_Optuna",
            host_file_path="/backup/Pasta_Teste_Optuna",
            ssh_port=22,
            username="viplab",
            password="viplab321"
        )
        self.machineKernelDestiny = UbuntoMachineKernel(
            username="viplab",
            password="viplab321",
            host="192.168.200.147",
            ssh_port=22
        )

        self.machineKernelSoruce = UbuntoMachineKernel(
            username="viplab",
            password="viplab321",
            host="localhost",
            ssh_port=22
        )

        self.TransferFileModule = TransferFileModule(transFileKernel=self.transferFileKernel,
                                                    machineKernelDestiny=self.machineKernelDestiny,
                                                    machineKernelSource=self.machineKernelSoruce)
    
    def test_TransferFile(self):
        self.TransferFileModule.transferFile(partition="/")
