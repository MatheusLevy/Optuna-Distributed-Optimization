import paramiko
from scp import SCPClient
from Models.Dataset import Dataset
from Models.Machine import Machine
import os
import sys
import uuid

class SSHTransferFileKernel:
    def __init__(self):
        self.ssh = None

    @staticmethod
    def progress4(filename, size, sent, peername):
        sys.stdout.write("(%s:%s) %s's progress: %.2f%%   \r" % (peername[0], peername[1], filename, float(sent)/float(size)*100) )
        sys.stdout.flush()  # Certifique-se de que o progresso é atualizado corretamente

    @staticmethod
    def make_folder_if_not_exists(folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def transferFile(self, dataset: Dataset = None, destiny_machine: Machine = None):
        try:
            # Conectar à máquina de origem
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(dataset.get_host(), username=dataset.get_username(), password=dataset.get_password())

            print("Movendo dataset para o servidor")
            uuid_dir = str(uuid.uuid4())  # Gerar UUID
            temp_dir = f"/backup/temp/{uuid_dir}"
            self.make_folder_if_not_exists(temp_dir)

            # Transferir o dataset para o servidor
            with SCPClient(self.ssh.get_transport(), progress4=self.progress4) as scp:
                scp.get(dataset.dataset_path, temp_dir, recursive=True)

            self.ssh.close()
            
            # Conectar à máquina de destino
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(destiny_machine.get_host(), username=destiny_machine.get_username(), password=destiny_machine.get_password())
            
            print("Movendo do servidor para a máquina de destino")
            dataset_name = os.path.basename(dataset.dataset_path.rstrip('/'))
            final_destiny = os.path.join(destiny_machine.local_dataset_path)
            # Transferir a pasta temporária para a máquina de destino com o nome desejado
            with SCPClient(self.ssh.get_transport(), progress4=self.progress4) as scp:
                scp.put(os.path.join(temp_dir, dataset_name), final_destiny, recursive=True)

        except Exception as e:
            raise e
        
        finally:
            if self.ssh:
                self.ssh.close()
