import sys
sys.path.insert(0, 'src')

from Kernels.Concrete.pipKernel import PipKernel
from Kernels.Concrete.condaKernel import CondaKernel

class TestPipKernel():
    def setup_method(self, method):
        self.username = "viplab"
        self.userpassword = "viplab321"

    def test_CreateConnection(self):
        kernel = PipKernel(self.username, password=self.userpassword, host="localhost", ssh_port=22)
        assert kernel is not None
        del kernel

    def test_InstallPip(self):
        kernel = PipKernel(self.username, password=self.userpassword, host="localhost", ssh_port=22)
        out = kernel.instalPip()
        assert out is not None
        del kernel

    def test_install_not_sudo(self):
        condaK = CondaKernel(username=self.username,
                             password=self.userpassword,
                             )
        condaK.init_conda_env("optuna")
        kernel = PipKernel(self.username, password=self.userpassword, host="localhost", ssh_port=22, shell=condaK.channel)
        out = kernel.install(package_name="pandas", version="==2.2.2", asSudo=False)
        assert out is not None
        del kernel

    def test_install_as_sudo(self):
        kernel = PipKernel(self.username, password=self.userpassword, host="localhost", ssh_port=22)
        out = kernel.install(package_name="numpy", version="==1.24.4", asSudo=True)
        assert out is not None
        del kernel

    def test_unistall(self):
        kernel = PipKernel(self.username, password=self.userpassword, host="localhost", ssh_port=22)
        out = kernel.uninstall(package_name="numpy", asSudo=False)
        assert out is not None
        del kernel

    def test_install_from_file(self):
        kernel = PipKernel(self.username, password=self.userpassword, host="localhost", ssh_port=22)
        out = kernel.install_from_file("/home/viplab/requirements.txt")
        del kernel

