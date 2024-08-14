import sys
sys.path.insert(0, 'src')
from Models.Machine import Machine
from Kernels.Strategy.machineKernel import MachineKernel
from Kernels.Concrete.ubuntuMachineKernel import UbuntoMachineKernel

class MachineKernelFactory():
    def getMachineKernel(self, type: str, machine: Machine) -> MachineKernel:
        if type == "Ubuntu":
            return UbuntoMachineKernel(host=machine.host,
                                       password=machine.password,
                                       username=machine.password,
                                       ssh_port=machine.ssh_port)
        else:
            raise ValueError(f"Machine type unknow {type}")