from Kernels.Exceptions.kernelException import KernelExceptions

class MachineKernelException(KernelExceptions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)