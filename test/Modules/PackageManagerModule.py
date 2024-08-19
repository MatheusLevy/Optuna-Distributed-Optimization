import sys
sys.path.insert(0, 'src')
from Modules.TransferFileModule import TransferFileModule
from Kernels.Concrete.sshTransferFileKernel import SSHTransferFileKernel
from Kernels.Concrete.ubuntuMachineKernel import UbuntoMachineKernel
from Models.Dataset import Dataset
from Models.Machine import Machine
from Modules.PackageManagerModule import PackageManagerModule
from Kernels.Concrete.condaKernel import CondaKernel

class TestPackageManagerModule():
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
        self.dataset = Dataset("lucas", self.datasetMachineKernel, local_dataset_path="/home/vip-lab/dataset_optuna_test", envs={"matheus_levy_env": "/home/vip-lab/environment.yml"})
        self.dstMachine = Machine(name="mackele", dataset=self.dataset, partition="/", local_dataset_path="/home/viplab", machineKernel=self.dstMachineKernel, online=True)
        self.transfeFileKernel = SSHTransferFileKernel()
        self.transferModule = TransferFileModule(dataset=self.dataset, destinyMachine=self.dstMachine, transferFileKernel=self.transfeFileKernel)
        self.packageMangerKernel = CondaKernel(self.dstMachine)

    def test_install(self):
        packageManagerModule = PackageManagerModule(self.dataset, self.dstMachine, self.transferModule, packageManagerKernel=self.packageMangerKernel, env_name="matheus_levy_env")
        packageManagerModule.install()