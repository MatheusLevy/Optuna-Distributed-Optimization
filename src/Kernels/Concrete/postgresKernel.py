"""
    Postgres Concrete Kernel
    @MatheusLevy
"""
from Kernels.Strategy.databaseKernel import DatabaseKernel
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
            print(f'Error connecting: {e}')
            raise

    def executeSql(self, query):
        try:
            self.cur.execute(query=query)
            if self.cur.description is not None:
                return self.cur.fetchall()
        except psycopg2.Error:
            raise
        
    def createDatabase(self, database_name, user):
        try:
            cmd = f'psql -U {self.user} -c "CREATE DATABASE {database_name} OWNER {user};"'
            return subprocess.run(cmd, shell=True, text=True, capture_output=True)
        except Exception:
            raise

    def deleteDatabase(self, database_name):
        try:
            cmd = f'psql -U {self.user} -c "DROP DATABASE {database_name};"'
            return subprocess.run(cmd, shell=True, text=True, capture_output=True)
        except Exception:
            raise

    def createUser(self, username, password):
        try:
            cmd = f'psql -U {self.user} -c "CREATE USER {username} WITH PASSWORD \'{password}\';"'
            return subprocess.run(cmd, shell=True, text=True, capture_output=True)
        except Exception:
            raise

    def deleteUser(self, username):
        try:
            cmd = f'psql -U {self.user} -c "DROP USER IF EXISTS {username};"'
            return subprocess.run(cmd, shell=True, text=True, capture_output=True)
        except Exception:
            raise

    def createTable(self, table_name, columns):
        try:
            query = f"""
                CREATE TABLE {table_name} (
                    {', '.join(columns)}
                );
            """
            cmd = f"psql -U {self.user} -c '{query}'"
            return subprocess.run(cmd, shell=True, text=True, capture_output=True)
        except Exception:
            raise

    def deleteTable(self, table_name):
        try:
            query = f'DROP TABLE IF EXISTS {table_name} CASCADE;'
            self.cur.execute(query)
            self.connection.commit()
        except Exception:
            raise
        
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
            exists = self.cur.fetchone()[0]
            return exists
        except psycopg2.Error as e:
            print(f'Error checking table existence: {e}')
            raise
    
    def listDatabases(self):
        try:
            query = "SELECT datname FROM pg_database WHERE datistemplate = false;"
            result= self.executeSql(query=query)
            return result
        except psycopg2.Error:
            raise

    def __del__(self):
        if hasattr(self, 'cur') and self.cur is not None:
            self.cur.close()
        if hasattr(self, 'connection') and self.connection is not None:
            self.connection.close()
    