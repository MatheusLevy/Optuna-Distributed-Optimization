import sys
sys.path.insert(0, 'src')
from Modules.TransferFileModule import TransferFileModule
from Kernels.Concrete.sshTransferFileKernel import SSHTransferFileKernel
from Kernels.Concrete.ubuntuMachineKernel import UbuntoMachineKernel
from Models.Dataset import Dataset
from Models.Machine import Machine

class TestTranferFileModule():
    def setup_method(self, method):
        self.datasetMachineKernel = UbuntoMachineKernel(username="vip-lab",
                                                        password="viplab321",
                                                        host="192.168.200.197",
                                                        ssh_port=22)
        self.dstMachineKernel = UbuntoMachineKernel(username="viplab",
                                                    password="viplab321",
                                                    host="192.168.200.147",
                                                    ssh_port=22
                                                    )
        self.dataset = Dataset("lucas", self.datasetMachineKernel, local_dataset_path="/home/vip-lab/dataset_optuna_test")
        self.dstMachine = Machine(name="mackele", dataset=self.dataset, partition="/", local_dataset_path="/home/viplab", machineKernel=self.dstMachineKernel, online=True)
        self.transfeFileKernel = SSHTransferFileKernel()
        self.transferModule = TransferFileModule(dataset=self.dataset, destinyMachineKernel=self.dstMachine, transferFileKernel=self.transfeFileKernel)

    def test_TransferFile(self):
        self.transfeFileKernel.transferFile(dataset=self.dataset, destiny_machine=self.dstMachine)