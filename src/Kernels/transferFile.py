import string
import paramiko

class TransferFileKernel():
    def __init__(self, ssh_port: int, host_file: string, 
                 remote_machine: string, remote_file_path:string,  username: string, password: string) -> object:
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(hostname=remote_machine,
                        port=ssh_port,
                        username=username,
                        password=password
                        )
        except Exception as e:
            raise
        self.host_file = host_file
        self.remote_file_path = remote_file_path
        self.sftp = self.ssh.open_sftp()

    def transfer(self):
        try:            
            self.sftp.put(self.host_file, self.remote_file_path)
            self.sftp.close()
        except:            
            raise

    def __del__(self):
        self.sftp.close()
        self.ssh.close()