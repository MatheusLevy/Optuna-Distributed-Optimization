import sys
sys.path.insert(0, 'src')


from Kernels.postgresql import PostgresSQLKernel

class TestPostgresSQLKernel():

    def setup_method(self, method):
            self.database='postgres'
            self.user='postgres'
            self.password='321'
            self.host='localhost'
            self.port='5432'
    
    def test_create_postgresql_kernel(self):
          kernel = PostgresSQLKernel(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
          )
          assert isinstance(kernel, PostgresSQLKernel)
          assert kernel is not None
          assert kernel.connection is not None

    def test_create_database(self):
        kernel = PostgresSQLKernel(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
        )
        kernel.create_database('teste_pytest', )
        assert kernel.exists_table_database('teste_pytest') is not None

