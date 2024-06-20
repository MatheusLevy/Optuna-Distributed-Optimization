import sys
sys.path.insert(0, 'src')

from Kernels.Concrete.postgresKernel import PostgresKernel
import subprocess

class TestPostgresSQLKernel():

      def setup_method(self, method):
            self.database='postgres'
            self.user='postgres'
            self.password='321'
            self.host='localhost'
            self.port='5432'

      def test_createKernel(self):
            kernel =  PostgresKernel(
                  database=self.database,
                  user=self.user,
                  password=self.password,
                  host=self.host,
                  port=self.port
            )
            assert isinstance(kernel, PostgresKernel)
            assert kernel is not None
            del kernel

      def test_executeSql(self):
            kernel =  PostgresKernel(
                  database=self.database,
                  user=self.user,
                  password=self.password,
                  host=self.host,
                  port=self.port
            )
            assert kernel is not None
            cmd = f'psql -U {self.user} -c "CREATE TABLE teste_py1 (id SERIAL PRIMARY KEY);"'
            subprocess.run(cmd, shell=True, text=True, capture_output=True)
            cmd = f'psql -U {self.user} -d {self.database} -c "INSERT INTO teste_py1 (id) VALUES (1);"'
            subprocess.run(cmd, shell=True, text=True, capture_output=True)
            results = kernel.executeSql(query="SELECT * FROM teste_py1;")
            assert results == [(1,)]
            kernel.deleteTable('teste_py1')
            del kernel

      def test_createDatabase(self):
            kernel =  PostgresKernel(
                  database=self.database,
                  user=self.user,
                  password=self.password,
                  host=self.host,
                  port=self.port
            )

            result = kernel.createDatabase(database_name='teste_pytest', owner='postgres')
            assert result is not None            
            assert result.stdout == 'CREATE DATABASE\n'
            assert result.stderr == ''
            kernel.deleteDatabase('teste_pytest')
            del kernel

      def test_deleteDatabase(self):
            kernel =  PostgresKernel(
                  database=self.database,
                  user=self.user,
                  password=self.password,
                  host=self.host,
                  port=self.port
            )
            
            kernel.createDatabase(database_name='teste_pytest', owner='postgres')
            result = kernel.deleteDatabase(database_name='teste_pytest')
            assert result is not None
            assert result.stdout == 'DROP DATABASE\n'
            assert result.stderr == ''

      def test_createUser(self):
            kernel =  PostgresKernel(
                  database=self.database,
                  user=self.user,
                  password=self.password,
                  host=self.host,
                  port=self.port
            )
                        
            result = kernel.createUser(username='test_user', password='123')
            assert result is not None
            assert result.stderr == ''
            kernel.deleteUser(username='test_user')
            del kernel

      def test_deleteUser(self):
            kernel =  PostgresKernel(
                  database=self.database,
                  user=self.user,
                  password=self.password,
                  host=self.host,
                  port=self.port
            )

            kernel.createUser(username='teste_pytest', password='123')
            result = kernel.deleteUser(username='teste_pytest')
            assert result is not None
            assert result.stdout == 'DROP ROLE\n'
            assert result.stderr == ''
            del kernel

      def test_createTable(self):
            kernel =  PostgresKernel(
                  database=self.database,
                  user=self.user,
                  password=self.password,
                  host=self.host,
                  port=self.port
            )
            table_name = 'teste_pytest2'
            columns = [
            'id SERIAL PRIMARY KEY',
            'nome VARCHAR(100)',
            'idade INTEGER',
            'email VARCHAR(100)'
            ]
            kernel.createTable(table_name=table_name, columns=columns)

            kernel.deleteTable(table_name=table_name)
            del kernel

      def test_deleteTable(self):
            kernel =  PostgresKernel(
                  database=self.database,
                  user=self.user,
                  password=self.password,
                  host=self.host,
                  port=self.port
            )
            table_name = 'teste'
            columns = [
            'id SERIAL PRIMARY KEY',
            'nome VARCHAR(100)',
            'idade INTEGER',
            'email VARCHAR(100)'
            ]
            kernel.createTable(table_name=table_name, columns=columns)
            kernel.deleteTable(table_name=table_name)
            del kernel

      def test_tableExists(self):
            kernel =  PostgresKernel(
                  database=self.database,
                  user=self.user,
                  password=self.password,
                  host=self.host,
                  port=self.port
            )
            table_name = 'tabela_verifica'
            columns = [
            'id SERIAL PRIMARY KEY',
            'nome VARCHAR(100)',
            'idade INTEGER',
            'email VARCHAR(100)'
            ]
            kernel.createTable(table_name, columns)
            result = kernel.tableExists(table_name)
            kernel.deleteTable(table_name)
            assert result is not None
            assert result is True
            del kernel

      def test_list_databases(self):
            kernel =  PostgresKernel(
                  database=self.database,
                  user=self.user,
                  password=self.password,
                  host=self.host,
                  port=self.port
            )
            result = kernel.listDatabases()    
            assert result is not None
            del kernel

      def test_databaseExists(self):
           kernel =  PostgresKernel(
                  database=self.database,
                  user=self.user,
                  password=self.password,
                  host=self.host,
                  port=self.port
            )
           kernel.createDatabase(owner=self.user, database_name="teste_database" )
           result = kernel.databaseExists("teste_database")
           assert result is not None
           assert result is True
           kernel.deleteDatabase("teste_database")
           del kernel