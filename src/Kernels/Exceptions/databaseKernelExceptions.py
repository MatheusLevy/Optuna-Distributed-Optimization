from Kernels.Exceptions.kernelException import KernelExceptions

class DatabaseException(KernelExceptions):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)