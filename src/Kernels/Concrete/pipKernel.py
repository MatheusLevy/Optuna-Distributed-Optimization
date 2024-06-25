import paramiko
import sys
import time
import re
sys.path.insert(0, 'src')

from Kernels.Exceptions.packageManagerException import PackageManagerException
from Kernels.Strategy.packageManager import PackageManager

class PipKernel(PackageManager):
    def __init__(self,
                    username,
                    password=None,
                    host="localhost",
                    ssh_port=22,
                    shell= None):
        self.host = host
        self.username = username
        self.password = password
        self._ssh= paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self._ssh.connect(
                hostname=self.host,
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
        self.channel = shell
    
    def instalPip(self):
        cmd = f"apt install -y python3-pip"
        cmd = f'sudo bash -c "{cmd}"'
        try:
            session = self._ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()
            session.exec_command(cmd)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write(self.password + "\n")
            stdin.flush()
        except Exception as e:
            raise PackageManagerException(
                mensage="Error while instaling pip",
                details=f"Failed to execute command: {cmd}",
                error=e
            ) from e
        return stdout.readlines()
    
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
                    mensage="Error monitoring the command output",
                    details="Falied to fetch the output of the command",
                    error=e
                )
            if self.patterns_in_string(output, regex_patterns) or self.strings_in_string(output, text_callback):
                time.sleep(0.5)
                break    
            
    def exec_command_with_shell(self, cmd, text_callback= [], regex_callback=[]):
        try:
            cmd = cmd+"; echo '(FINISHED CODE)'\n"
            self.channel.send(cmd)
            time.sleep(0.5)
        except Exception as e:
            raise e
        try:
            self.wait_until_command_finished(
                text_callback=text_callback,
                regex_patterns=regex_callback)
        except PackageManagerException as e:
            raise e

    def install(self, package_name, version, asSudo=False):
        cmd = f"pip3 install {package_name}{version}"
        if asSudo:
            cmd = f'sudo bash -c "{cmd}"'
        if self.channel is not None:
            try:
                self.exec_command_with_shell(cmd, text_callback=["(FINISHED CODE)\r\n"])
            except PackageManagerException as e:
                raise e
            return True
       
        try:
            session = self._ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()
            session.exec_command(cmd)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            if asSudo:
                stdin.write(self.password + "\n")
                stdin.flush()
        except Exception as e:
            raise PackageManagerException(
                mensage="Error while instaling pip",
                details=f"Failed to execute command: {cmd}",
                error=e
            ) from e
        return stdout.readlines()
    
    def install_from_file(self, file_path, asSudo=False):
        cmd = f"pip3 install -r {file_path}"
        if asSudo:
            cmd = f'sudo bash -c {cmd}'
        if self.channel is not None:
            try:
                self.exec_command_with_shell(cmd, text_callback=["(FINISHED CODE)"])
            except PackageManagerException as e:
                raise e
            return True
        try:
            session = self._ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()
            session.exec_command(cmd)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            if asSudo:
                stdin.write(self.password + "\n")
                stdin.flush()
        except Exception as e:
            raise PackageManager(
                mensage="Erro while instaling requirements",
                details=f"Failed to execute: {cmd}",
                error=e
            ) from e
        return stdout.readlines()


    def uninstall(self, package_name, asSudo=False):
        cmd = f"pip3 uninstall -y {package_name}"
        if asSudo:
            cmd = f'sudo bash -c "{cmd}"'
        if self.channel is not None:
            try:
                self.exec_command_with_shell(cmd, text_callback=["(FINISHED CODE)"])
            except PackageManagerException as e:
                raise e
            return True
        try:
            session = self._ssh.get_transport().open_session()
            session.set_combine_stderr(True)
            session.get_pty()
            session.exec_command(cmd)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            if asSudo:
                stdin.write(self.password + "\n")
                stdin.flush()
        except Exception as e:
            raise PackageManagerException(
                mensage="Error while instaling pip",
                details=f"Failed to execute command: {cmd}",
                error=e
            ) from e
        session.close()
        return stdout.readlines()
    
    def __del__(self):
        self._ssh.close()