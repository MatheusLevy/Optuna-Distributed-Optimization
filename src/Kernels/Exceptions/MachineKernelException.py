from Kernels.Exceptions.kernelException import KernelExceptions

class MachineKernelException(KernelExceptions):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)