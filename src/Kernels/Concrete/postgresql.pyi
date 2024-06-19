from Kernels.kernel import Kernel
from typing import Optional

class PostgresSQLKernel(Kernel):
    def __init__(
            self,
            database: str,
            user: str='postgres',
            password:str='321',
            host:str='localhost',
            port:str='5432'
                ) -> Kernel: ...
    
    def execute(
            self,
            query: Optional[str],
            sql: Optional[str]) -> None: ...

    def __del__(self) -> None: ...