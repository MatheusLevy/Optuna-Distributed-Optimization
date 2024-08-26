import sys
sys.path.insert(0, 'src')

class DatabaseModule():
    def __init__(self, database) -> None:
        self.database = database

    def buildDatabase(self):
        self.database.databaseKernel.createUser(username=self.database.username, password=self.database.password)
        self.database.databaseKernel.createDatabase(database_name=self.database.name, owner=self.database.username)

    def destructDatabase(self):
        self.database.databaseKernel.deleteDatabase(database_name=self.database.name)
        self.database.databaseKernel.deleteUser(username=self.database.username)