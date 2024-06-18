"""
    Transfer File Operations Kernel
    @MatheusLevy
"""
import paramiko
from Kernels.kernel import Kernel

class TransferFileKernel(Kernel):
    def __init__(
                self,
                host_file, 
                remote_machine,
                remote_file_path,
                username,
                password,
                ssh_port=22):
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self._ssh.connect(hostname=remote_machine,
                        port=ssh_port,
                        username=username,
                        password=password
                        )
        except Exception:
            raise
        self.host_file = host_file
        self.remote_file_path = remote_file_path
        self._sftp = self._ssh.open_sftp()

    def execute(self):
        try:            
            self._sftp.put(self.host_file, self.remote_file_path)
            self._sftp.close()
        except:            
            raise

    def __del__(self):
        self._sftp.close()
        self._ssh.close()