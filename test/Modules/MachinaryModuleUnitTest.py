import sys
sys.path.insert(0, 'src')

from Modules.MachinaryModule import MachinaryModule
from Models.Dataset import Dataset

class TestTranferFileModule():
    def setup_method(self, method):
        self.machine_list = [
            {'username': 'viplab', 'password': 'viplab321', 'host': '192.168.200.147', 'ssh_port': 22},
            {'username': 'vip-lab', 'password': 'viplab321', 'host': '192.168.200.79', 'ssh_port': 22},
            {'username': 'viplab3', 'password': 'viplab321', 'host': '192.168.200.22', 'ssh_port': 22},
        ]
        self.dataset = Dataset("localhost", "viplab", "viplab321", "22", "/backup/teste_data"
                               )
    def test_online_machines(self):
        module = MachinaryModule(dataset=self.dataset, machine_list=self.machine_list)
        onlines = module.get_online_machines()
        print(onlines)
        