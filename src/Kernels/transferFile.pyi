from Kernels.kernel import Kernel

class TransferFileKernel(Kernel):
    def __init__(
                self,
                host_file: str,
                remote_machine: str,
                remote_file_path: str,
                username: str,
                password: str,
                ssh_port: int = 22,
                ) -> Kernel: ...
    
    def execute(self) -> None: ...

    def __del__(self) -> None: ...