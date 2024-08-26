import sys
sys.path.insert(0, 'src')

from Modules.DatabaseModule import DatabaseModule
from Kernels.Concrete.postgresKernel import PostgresKernel
from Models.Database import Dataset

class TestTranferFileModule():
    def setup_method(self, method):
        self.databaseKenrel = PostgresKernel(
            database='postgres',
            user='postgres',
            password='321',
            host='localhost',
        )
        self.database = Dataset(name="optuna_pytest", username="levy", password="321", databaseKernel= self.databaseKenrel)

    def test_buildDatabaseWithOwner(self):
        datamodule =DatabaseModule(database=self.database)
        datamodule.buildDatabase()

    def test_destructDatabse(self):
        datamodule = DatabaseModule(database=self.database)
        datamodule.destructDatabase()