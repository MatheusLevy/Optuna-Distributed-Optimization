from Kernels.Exceptions.kernelException import KernelExceptions

class PackageManagerException(KernelExceptions):
    def __init__(self, message, details, error) -> None:
        super().__init__(message, details, error)