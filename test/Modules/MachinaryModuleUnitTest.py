import sys
sys.path.insert(0, 'src')

from Modules.MachinaryModule import MachinaryModule

class TestTranferFileModule():
    def setup_method(self, method):
        self.machine_list = [
            {'username': 'viplab', 'password': 'viplab321', 'host': '192.168.200.147', 'ssh_port': 22},
            {'username': 'vip-lab', 'password': 'viplab321', 'host': '192.168.200.79', 'ssh_port': 22},
            {'username': 'viplab3', 'password': 'viplab321', 'host': '192.168.200.22', 'ssh_port': 22},
        ]

    def test_online_machines(self):
        module = MachinaryModule(self.machine_list)
        onlines = module.get_online_machines()
        print(onlines)

    def test_in_use_machines(self):
        module = MachinaryModule(self.machine_list)
        onlines = module.get_online_machines()
        module._add_in_use_machines(onlines)
