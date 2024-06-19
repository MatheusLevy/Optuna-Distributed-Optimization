"""
    Transfer File Concrete Operations Kernel
    @MatheusLevy
"""
import paramiko
from Kernels.Strategy.tranferFileKernel import TransferFileKernel

class SSHTranferFileKernel(TransferFileKernel):
    def __init__(self,
                remote_machine,
                remote_file_path,
                username,
                password,
                host_file_path,
                ssh_port=22):
        super().__init__()
        self._ssh= paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self._ssh.connect(
                hostname=remote_machine,
                port=ssh_port,
                username=username,
                password=password)
        except Exception:
                raise
        self.host_file= host_file_path
        self.remote_file= remote_file_path
        self._sftp = self._ssh.open_sftp()
    
    def tranferFromHostToRemote(self):
        try:
            self._sftp.put(self.host_file, self.remote_file)
        except Exception:
            raise

    def transferFromRemoteToHost(self):
        try:
            self._sftp.get(self.remote_file, self.host_file)
        except Exception:
            raise

    def __del__(self):
        self._sftp.close()
        self._ssh.close()