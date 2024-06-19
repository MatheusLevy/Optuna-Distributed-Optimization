"""
    Transfer File Concrete Operations Kernel
    @MatheusLevy
"""
from Kernels.Strategy.tranferFileKernel import TransferFileKernel

class SSHTranferFileKernel(TransferFileKernel):
    def __init__(self,
                remote_machine: str,
                remote_file_path: str,
                username: str,
                password: str,
                host_file_path: str,
                ssh_port: int=22) -> TransferFileKernel: ...
        
    def tranferFromHostToRemote(self) -> None: ...

    def transferFromRemoteToHost(self) -> None: ...

    def __del__(self) -> None: ...