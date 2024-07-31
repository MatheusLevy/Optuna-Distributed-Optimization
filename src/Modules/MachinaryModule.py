import sys
sys.path.insert(0, 'src')
from Kernels.Concrete.ubuntuMachineKernel import UbuntoMachineKernel
from Kernels.Exceptions.MachineKernelException import MachineKernelException
class Machine():
    def __init__(self, username, password, host, ssh_port, online=False):
        self.username = username
        self.password = password
        self.host = host
        self.ssh_port = ssh_port
        self.online = online
        self.kernel = None
    
    def start_kernel(self):
        try:
            self.kernel = UbuntoMachineKernel(username=self.username,
                                       password=self.password,
                                       host=self.host,
                                       ssh_port=self.ssh_port)
            self.online = True
            print(f"(OK) Connected to {self.host} on port {self.password}" )
        except MachineKernelException as e:
            print(f"(FAIL) Machine {self.username} in addr {self.host} set Offline due to: {e.error}")
        return self.kernel

class MachinaryModule():
    def __init__(self,
                machine_list):
        self.machines = []
        for machine_dict in machine_list:
            machine = self._create_machine(machine_dict)
            machine.start_kernel()
            self.machines.append(machine)
        
    def _create_machine(self, machine_dict):
        return Machine(username=machine_dict['username'],
                       password=machine_dict['password'],
                       host=machine_dict['host'],
                       ssh_port=machine_dict['ssh_port'])
        
    def get_online_machines(self):
        return [ machine for machine in self.machines if machine.online]
