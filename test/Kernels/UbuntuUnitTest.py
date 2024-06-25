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
    
    def test_get_memmory_inf(self):
        kernel = UbuntoMachineKernel(
            username=self.username,
            password=self.password,
        )
        info = kernel.get_memmory_info()

    def test_get_cpu_info(self):
        kernel = UbuntoMachineKernel(
            username=self.username,
            password=self.password,
        )  
        info = kernel.get_CPU_info()

    def test_get_gpu_info(self):
        kernel = UbuntoMachineKernel(
            username=self.username,
            password=self.password,
        )  
        a = kernel.get_GPU_info()
        print(a)