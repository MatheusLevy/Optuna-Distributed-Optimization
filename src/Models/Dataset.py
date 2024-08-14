import sys
sys.path.insert(0, 'src')

class Dataset():
    def __init__(self, source_ip, source_username, source_password, source_ssh_port, source_path, machineKernel):
        self.source_ip=source_ip
        self.source_username=source_username
        self.source_password=source_password
        self.source_ssh=source_ssh_port
        self.source_path=source_path
        self.source_machine_kernel=machineKernel
