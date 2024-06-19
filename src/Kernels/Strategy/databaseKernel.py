"""
    Transfer File Strategy Kernel
    @MatheusLevy
"""
from abc import ABC, abstractmethod

class DatabaseKernel(ABC):

    @abstractmethod
    def executeSql(self, query):
        pass

    @abstractmethod
    def createDatabase(self, database_name, user):
        pass
    
    @abstractmethod
    def deleteDatabase(self, database_name):
        pass
    
    @abstractmethod
    def createUser(self):
        pass

    @abstractmethod
    def deleteUser(self):
        pass

    @abstractmethod
    def createTable(self):
        pass

    @abstractmethod
    def deleteTable(self):
        pass

    @abstractmethod
    def tableExists(self, table_name):
        pass   
    
    @abstractmethod
    def listDatabases(self):
        pass
    
    @abstractmethod
    def __del__():
        pass