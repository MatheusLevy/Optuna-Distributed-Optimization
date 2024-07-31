from Kernels.Strategy.packageManager import PackageManager
from Kernels.Exceptions.packageManagerException import PackageManagerException
import paramiko
import time
import re

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
                message="Error connecting via ssh to machine",
                details="Failed to connect",
                error=e
            ) from e
    
    def wait_shell_be_ready(self, timeout=30):
        seconds_elapsed = 0
        while not self.channel.recv_ready():
            if (seconds_elapsed >timeout):
                raise PackageManagerException(
                    message="Timout on invoked Shell",
                    details=f"Shell was not ready, so timeout of: {timeout}"
                )
            time.sleep(1)
            seconds_elapsed+=1

    def init_shell(self, timeout=30):
        try:
            self.channel = self._ssh.invoke_shell()
        except Exception as e:
            raise PackageManagerException(
                message="Error while invoking shell",
                error=e
            )
        try: 
            self.wait_shell_be_ready(timeout)
        except PackageManagerException as e:
            raise e

    def init_conda_env(self, env_name, timeout=30):
        self.env_name = env_name
        try:
            self.init_shell()
        except PackageManagerException as e:
            raise e
        
        cmd = f"conda activate {env_name}\n"
        try:
            self.channel.send(cmd)
        except Exception as e:
            raise PackageManagerException(
                message="Error while send command",
                details=f"Failed executing command: {cmd}",
                error=e
            ) from e
        
        try:
            self.wait_shell_be_ready(timeout)
        except PackageManagerException as e:
            raise e
        
        output = self.channel.recv(2048)   
        return output
    
    def patterns_in_string(self, string, patterns):
        for pattern in patterns:
            if re.match(pattern, string):
                return True
        return False
    
    def strings_in_string(self, string, strings):
            for text in  strings:
                if text in string:
                    return True
            return False
            
    def wait_until_command_finished(self, regex_patterns=[''], text_callback=['']):
        while True:
            try:
                output = self.channel.recv(1024).decode()
            except Exception as e:
                raise PackageManagerException(
                    message="Error monitoring the command output",
                    details="Falied to fetch the output of the command",
                    error=e
                )
            if self.patterns_in_string(output, regex_patterns) or self.strings_in_string(output, text_callback):
                time.sleep(0.5)
                break      
               
    def install(self, package_name, version=""):
        cmd = f"conda install -y -q {package_name}{version}" + "; echo '(FINISHED CODE)'\n"
        try:
            self.channel.send(cmd)
            time.sleep(0.5)
        except Exception as e: 
            raise PackageManagerException(
                message="Error during package install",
                details=f"Failed to run the command: {cmd}",
                error=e
            )
        try:
            self.wait_until_command_finished(
                text_callback=["(FINISHED CODE)\r\n"]
            )
        except PackageManagerException as e:
            raise e

    def install_from_file(self, file_path):
        cmd = f"conda env create -f {file_path}" + "; echo '(FINISHED CODE)'\n"
        try:
            self.channel.send(cmd)
            time.sleep(0.5)
        except Exception as e:
            raise PackageManagerException(
                message="Error during env install",
                details="Failed to install from file",
                error=e
            ) from e
        try:
            self.wait_until_command_finished(
                text_callback=["FINISHED CODE"]
            )
        except PackageManagerException as e:
            raise e
        
    def uninstall(self, package_name):
        cmd = f"conda remove -y -q {package_name}" +  "; echo '(FINISHED CODE)'\n"
        try:
            self.channel.send(cmd)
            time.sleep(0.5)
        except Exception as e: 
            raise PackageManagerException(
                message="Error during package remove",
                details=f"Failed to run the command: {cmd}",
                error=e
            )
        try:
            self.wait_until_command_finished(
                text_callback=["FINISHED CODE"]
            )
        except PackageManagerException as e:
            raise e
    
    def __del__(self):
        self._ssh.close()