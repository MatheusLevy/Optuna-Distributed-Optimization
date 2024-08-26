import sys
sys.path.insert(0, 'src')
from Kernels.Strategy.databaseKernel import DatabaseKernel

class Dataset():
    def __init__(self, name, username, password, databaseKernel: DatabaseKernel):
        self.name = name
        self.username= username
        self.password = password
        self.databaseKernel = databaseKernel