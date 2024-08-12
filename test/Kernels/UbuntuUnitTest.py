import sys
sys.path.insert(0, 'src')

from Kernels.Concrete.ubuntuMachineKernel import UbuntoMachineKernel

class TestUbuntuKernel():
    def setup_method(self, method):
        self.username= "viplab"
        self.password="viplab321"

    
    def test_get_partition_info(self):
        kernel = UbuntoMachineKernel(
            username=self.username,
            password=self.password,
        )
        info = kernel.get_partition_info(partition="/backup")
        assert info is not None
        assert info != ""

    def test_get_memmory_inf(self):
        kernel = UbuntoMachineKernel(
            username=self.username,
            password=self.password,
        )
        info = kernel.get_memmory_info()
        assert info is not None
        assert info != ""

    def test_get_cpu_info(self):
        kernel = UbuntoMachineKernel(
            username=self.username,
            password=self.password,
        )  
        info = kernel.get_CPU_info()
        assert info is not None
        assert info != ""

    def test_get_gpu_info(self):
        kernel = UbuntoMachineKernel(
            username=self.username,
            password=self.password,
        )  
        info = kernel.get_GPU_info()
        assert info is not None
        assert info != ""

    def test_get_process_info(self):
        kernel = UbuntoMachineKernel(
            username=self.username,
            password=self.password,
        )  
        info = kernel.get_process_info(pid=1867)
        assert info is not None
        assert info != ""

    def test_kill_process_info(self):
        kernel = UbuntoMachineKernel(
            username=self.username,
            password=self.password,
        )  
        info = kernel.kill_process_info(pid=18101)
        assert info is not None
        assert info == ''

    def test_gpu_is_used(self):
        kernel = UbuntoMachineKernel(
            username=self.username,
            password=self.password,
        )  
        print(kernel.gpu_is_used())