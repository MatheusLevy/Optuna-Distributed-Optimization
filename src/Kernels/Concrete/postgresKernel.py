"""
    Postgres Concrete Kernel
    @MatheusLevy
"""
from Kernels.Strategy.databaseKernel import DatabaseKernel
from Kernels.Exceptions.databaseKernelExceptions import DatabaseException
import psycopg2
import subprocess

class PostgresKernel(DatabaseKernel):
    def __init__(
            self,
            database,
            user='postgres',
            password='321',
            host='localhost',
            port='5432'
            ):
        self.user= user
        try:
            self.connection = psycopg2.connect(
                dbname= database,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cur = self.connection.cursor()
        except psycopg2.Error as e:
            raise DatabaseException(
                mensage="Error while initing PostgresKernel Object",
                details="Failed to create connection with database",
                error=e) from e

    def executeSql(self, query):
        try:
            self.cur.execute(query=query)
            if self.cur.description is not None:
                return self.cur.fetchall()
        except psycopg2.Error as e:
            raise DatabaseException(
                mensage="Error wihile executing query",
                error=e
            ) from e
        
    def createDatabase(self, database_name, owner):
        try:
            cmd = f'psql -U {self.user} -c "CREATE DATABASE {database_name} OWNER {owner};"'
            return subprocess.run(cmd, shell=True, text=True, capture_output=True)
        except subprocess.SubprocessError as e:
            raise DatabaseException(
                mensage="Error while creating database via subprocess",
                details=f"Failed to execute comand: {cmd}",
                error=e
            ) from e
            

    def deleteDatabase(self, database_name):
        try:
            cmd = f'psql -U {self.user} -c "DROP DATABASE {database_name};"'
            return subprocess.run(cmd, shell=True, text=True, capture_output=True)
        except subprocess.SubprocessError as e:
            raise DatabaseException(
                mensage="Error while deleting database via subprocess",
                details=f"Failed to execute command: {cmd}",
                error=e
            )
        
    def createUser(self, username, password):
        try:
            cmd = f'psql -U {self.user} -c "CREATE USER {username} WITH PASSWORD \'{password}\';"'
            return subprocess.run(cmd, shell=True, text=True, capture_output=True)
        except subprocess.SubprocessError as e:
            raise DatabaseException(
                mensage="Error while creating user via subprocess",
                details=f"Failed to execute command: {cmd}",
                error=e
            ) from e

    def deleteUser(self, username):
        try:
            cmd = f'psql -U {self.user} -c "DROP USER IF EXISTS {username};"'
            return subprocess.run(cmd, shell=True, text=True, capture_output=True)
        except subprocess.SubprocessError as e:
            raise DatabaseException(
                mensage="Error while deleting user via subprocess",
                details=f"Falied to execute command: {cmd}",
                error=e
            ) from e

    def createTable(self, table_name, columns):
        try:
            query = f"""
                CREATE TABLE {table_name} (
                    {', '.join(columns)}
                );
            """
            cmd = f"psql -U {self.user} -c '{query}'"
            return subprocess.run(cmd, shell=True, text=True, capture_output=True)
        except subprocess.SubprocessError as e:
            raise DatabaseException(
                mensage="Error while creating table via subprocess",
                details=f"Failed to execute command: {cmd}",
                error=e
            ) from e

    def deleteTable(self, table_name):
        try:
            query = f'DROP TABLE IF EXISTS {table_name} CASCADE;'
            self.cur.execute(query)
        except psycopg2.Error as e:
            raise DatabaseException(
                mensage="Erro while deleting table with cursor to database",
                details=f"Failed to execute query: {query}",
                error=e
            ) from e
        try:
            self.connection.commit()
        except psycopg2.Error as e:
            raise DatabaseException(
                mensage="Erro while commiting changes to database",
                error=e
            ) from e  
        
    def tableExists(self, table_name):
        try:
            query = """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = %s
                );
            """
            self.cur.execute(query, (table_name,))
        except psycopg2.Error as e:
            raise DatabaseException(
                mensage="Error while verifying table with cursor to database",
                details=f"Failed to excute query: {query}",
                error=e
            ) from e
        try:
            exists = self.cur.fetchone()[0]
        except psycopg2.Error as e:
            raise DatabaseException(
                mensage="Error while fetching one from cursor",
                details="Error on self.cur.fetchone()[0]",
                error=e
            ) from e
        return exists
    
    def databaseExists(self, database_name):
        try:
            query = """
                SELECT EXISTS (
                    SELECT 1
                    FROM pg_database
                    WHERE datname = %s
                );
            """
            self.cur.execute(query, (database_name,))
        except psycopg2.Error as e:
            raise DatabaseException(
                mensage="Error while verifying database with cursor to database",
                details=f"Failed to exectue query: {query}",
                error=e
            ) from e
        try:
            exists = self.cur.fetchone()[0]
        except psycopg2.Error as e:
            raise DatabaseException(
                mensage="Error while fething on from cursor",
                details="Error on self.cur.fetchone()[0]",
                error=e
            )    
        return exists
        

    def listDatabases(self):
        try:
            query = "SELECT datname FROM pg_database WHERE datistemplate = false;"
            result= self.executeSql(query=query)
        except DatabaseException as e:
            raise e
        return result
 
    def __del__(self):
        if hasattr(self, 'cur') and self.cur is not None:
            self.cur.close()
        if hasattr(self, 'connection') and self.connection is not None:
            self.connection.close()
    