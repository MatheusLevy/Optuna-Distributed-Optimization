import sys
sys.path.insert(0, 'src')
from Kernels.Concrete.sshTransferFileKernel import  SSHTranferFileKernel
from Models.Machine import Machine
from Models.Dataset import Dataset

class TransferFileKernelFactory():
    def getTramsferFileKernel(self, type:str="ssh", machine:Machine=None, dataset:Dataset=None):
        if type == "SSH":
            return SSHTranferFileKernel(
                
            )
        else:
            raise ValueError(f"Transfer File type unknow {type}")