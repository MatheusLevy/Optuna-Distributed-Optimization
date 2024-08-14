import sys
sys.path.insert(0, 'src')
from Models.Machine import Machine
from Kernels.Strategy.machineKernel import MachineKernel
from Kernels.Concrete.ubuntuMachineKernel import UbuntoMachineKernel

class MachineKernelFactory():
    def getMachineKernel(self, type: str, host, password, username, ssh_port) -> MachineKernel:
        if type == "Ubuntu":
            return UbuntoMachineKernel(host=host,
                                       password=password,
                                       username=username,
                                       ssh_port=ssh_port)
        else:
            raise ValueError(f"Machine type unknow {type}")