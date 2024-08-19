import sys
sys.path.insert(0, 'src')
from Models.Machine import Machine
from Models.Dataset import Dataset
from Modules.TransferFileModule import TransferFileModule
from Kernels.Strategy.packageManager import PackageManager

class PackageManagerModule():
    def __init__(self, dataset: Dataset, dstMachine: Machine, transferFileModule: TransferFileModule, packageManagerKernel: PackageManager, env_name: str):
        self.dataset = dataset
        self.dstMachine = dstMachine
        self.transferModule = transferFileModule
        self.packageManagerKernel = packageManagerKernel
        self.env = env_name

    def install(self):
        # puxar o env do dataset para a maquina de dst
        path_to_env_file = self.transferModule.transferFile(file_path=self.dataset.enviroments[self.env])
        # Instalar na maquina de destino
        self.packageManagerKernel.init_shell()
        print(f"Instaling Env on {self.dstMachine.name}")
        self.packageManagerKernel.install_from_file(file_path=path_to_env_file)