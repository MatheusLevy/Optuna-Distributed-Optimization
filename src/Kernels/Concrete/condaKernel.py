from Kernels.Strategy.packageManager import PackageManager
from Kernels.Exceptions.packageManagerException import PackageManagerException
import paramiko
import time

class CondaKernel(PackageManager):
    def __init__(self,
                 username,
                 password,
                 host="localhost",
                 ssh_port=22):
        self.username=username,
        self.password=password,
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.channel = None
        self.env_name= None
        try:
            self._ssh.connect(
                hostname=host,
                port=ssh_port,
                username=username,
                password=password
            )
        except Exception as e:
            raise PackageManagerException(
                mensage="Error connecting via ssh to machine",
                details="Failed to connect",
                error=e
            ) from e
        
    def init_conda_env(self, env_name):
        self.env_name = env_name
        try:
            self.channel = self._ssh.invoke_shell()
            while not self.channel.recv_ready():
                time.sleep(1)
        except Exception as e:
            raise PackageManagerException(
                mensage="Error while invoking shell",
                error=e
            )
        cmd = f"conda activate {env_name}\n"
        try:
            self.channel.send(cmd)
        except Exception as e:
            raise PackageManagerException(
                mensage="Error while send command",
                details=f"Failed executing command: {cmd}",
                error=e
            ) from e
        output= None
        if self.channel.recv_ready():
            output = self.channel.recv(1024)
        return output
    
    def install(self, package_name, version=""):
        cmd = f"conda install -y -q {package_name}{version}\n"
        try:
            self.channel.send(cmd)
            time.sleep(1)  # Aguarda um momento para que o comando seja processado inicialmente

            while True:
                output = self.channel.recv(1024).decode()
                print(output)
                print('Executing transaction: ...working...' in output or '# All requested packages already installed.' in output)
                if 'Executing transaction: ...working...' in output or '# All requested packages already installed.' in output:
                    time.sleep(1)
                    break
        except Exception as e:
            raise Exception(f"Error executing installation command: {e}")

    

    def uninstall(self, host, package_name):
        return super().uninstall(host, package_name)
    
    def __del__(self):
        self._ssh.close()