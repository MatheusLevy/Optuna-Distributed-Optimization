import sys
sys.path.insert(0, 'src')

from Kernels.Concrete.sshTransferFileKernel import SSHTransferFileKernel
from Models.Dataset import Dataset
from Models.Machine import Machine
from Factories.MachineKernelFactory import MachineKernelFactory


class TestTransferFileKernel():

    def setup_method(self, method):
        factory = MachineKernelFactory()
        datasetMachineKernel = factory.getMachineKernel(type= "Ubuntu", host="192.168.200.197", username="vip-lab", password="viplab321", ssh_port=22)
        self.dataset = Dataset(name= "lucas",
                               local_dataset_path="/home/vip-lab/dataset_optuna_test",
                               machine_kernel=datasetMachineKernel)
        

        self.destinyMachineKernel= factory.getMachineKernel(type="Ubuntu", host="192.168.200.147", username="viplab", password="viplab321", ssh_port=22)
        self.destinyMachine = Machine(name="mackele",
                                      dataset=self.dataset,
                                      partition="/",
                                      local_dataset_path="/home/viplab",
                                      machineKernel= self.destinyMachineKernel
                                      )
        self.sshTransferFileKernel = SSHTransferFileKernel()

    def teste_transferFile(self):
        self.sshTransferFileKernel.transferFile(dataset=self.dataset, destiny_machine=self.destinyMachine)  