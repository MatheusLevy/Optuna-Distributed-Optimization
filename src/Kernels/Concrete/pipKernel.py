import paramiko
from Kernels.Strategy.packageManager import PackageManager
from Kernels.Exceptions.packageManagerException import PackageManagerException

class PipKernel(PackageManager):
    def __init__(self,
                    username,
                    password=None,
                    host="localhost",
                    ssh_port=22):
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
    
    def install(self, package_name, version, asSudo=False):
        cmd = f"pip3 install {package_name}{version}"
        if asSudo:
            cmd = f'sudo bash -c "{cmd}"'
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
    
    def uninstall(self, package_name, asSudo=False):
        cmd = f"pip3 uninstall -y {package_name}"
        if asSudo:
            cmd = f'sudo bash -c "{cmd}"'
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
    
    def __del__(self):
        self._ssh.close()