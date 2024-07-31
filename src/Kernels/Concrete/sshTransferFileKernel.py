"""
    Transfer File Concrete Operations Kernel
    @MatheusLevy
"""
import paramiko
import os

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
        except Exception as e:
            raise RuntimeError(f"Failed to connect or open SFTP: {e}")
        self.host_file= host_file_path
        self.remote_file= remote_file_path
        self._sftp = self._ssh.open_sftp()

    def upload_folder(self, local_folder, remote_folder, verbose=False):
        try:
            # Cria o diretório remoto se não existir
            try:
                self._sftp.chdir(remote_folder)
            except IOError:
                parent_folder = os.path.dirname(remote_folder)
                if parent_folder:
                    # Recorre para criar diretórios pais
                    self._sftp.mkdir(remote_folder)
                    self._sftp.chdir(remote_folder)
                    self.upload_folder(local_folder, remote_folder, verbose)
            
            # Percorre todos os arquivos e diretórios na pasta local
            for item in os.listdir(local_folder):
                local_path = os.path.join(local_folder, item)
                remote_path = os.path.join(remote_folder, item)

                if os.path.isfile(local_path):
                    # Se for um arquivo, verifique se já existe no remoto
                    if self.file_exists(remote_path):
                        if verbose:
                            print(f"Already exists: {remote_path}")
                    else:
                        self._sftp.put(local_path, remote_path)
                        if verbose:
                            print(f"{local_path} => {remote_path}")
                elif os.path.isdir(local_path):
                    # Se for um diretório, chame recursivamente
                    if verbose:
                        print(f"Directory: {local_path} => {remote_path}")
                    # Não altera o diretório remoto antes de chamar recursivamente
                    self.upload_folder(local_path, remote_path, verbose)
        except Exception as e:
            raise RuntimeError(f"Failed to upload folder: {e}")
        
    def file_exists(self, remote_path):
        try:
            self._sftp.stat(remote_path)
            return True
        except IOError:
            return False
        
    def tranferFromHostToRemote(self, isFolder=False, verbose=False):
        if isFolder:
            try:
                self.upload_folder(self.host_file, self.remote_file, verbose=verbose)
            except Exception as e:
                raise RuntimeError(f"Failed to transfer folder from host to remote: {e}")
        else:
            try:
                self._sftp.put(self.host_file, self.remote_file)
            except Exception as e:
                raise RuntimeError(f"Failed to transfer file from host to remote: {e}")


    def transferFromRemoteToHost(self):
        try:
            self._sftp.get(self.remote_file, self.host_file)
        except Exception as e:
            raise RuntimeError(f"Failed to transfer file from remote to host: {e}")
    
    def __del__(self):
        try:
            self._sftp.close()
            self._ssh.close()
        except Exception as e:
            print(f"Failed to close SFTP or SSH connection: {e}")