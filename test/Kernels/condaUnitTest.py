import sys
sys.path.insert(0, 'src')

from Kernels.Concrete.condaKernel import CondaKernel

class TestCondaKernel():
    def setup_method(self, method):
        self.username = "viplab"
        self.userpassword = "viplab321"

    def test_createConnection(self):
        kernel = CondaKernel(username=self.username, password=self.userpassword, host="localhost", ssh_port=22)
        assert kernel is not None
        del kernel

    def test_invoke_shell(self):
        kernel = CondaKernel(username=self.username, password=self.userpassword, host="localhost", ssh_port=22)
        out = kernel.init_conda_env(env_name="optuna")
        assert kernel.channel is not None
        print(out)

    def test_install(self):
        kernel = CondaKernel(username=self.username, password=self.userpassword, host="localhost", ssh_port=22)
        kernel.init_conda_env("optuna")
        kernel.install(package_name="numpy")
        del kernel