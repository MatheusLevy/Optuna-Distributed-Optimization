import psycopg2
from Kernels.kernel import Kernel
import subprocess

class PostgresSQLKernel(Kernel):
    def __init__(
        self,
        database,
        user='postgres',
        password='321',
        host='localhost',
        port='5432'
    ):
        super().__init__()
        self._database = database
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        try:
            self.connection = psycopg2.connect(
                dbname=self._database,
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port
            )
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            raise

    def execute(self, sql):
        with self.connection:
            with self.connection.cursor() as cur:
                try:
                    cur.execute(sql)
                    self.connection.commit()
                except psycopg2.Error as e:
                    self.connection.rollback()
                    raise

    def exists_table_database(self, table_name):
            with self.connection:
                with self.connection.cursor() as cur:
                    try:
                        query = f"SELECT datname FROM pg_database WHERE datname='{table_name}';"
                        cur.execute(query=query)
                        return cur.fetchone()
                    except psycopg2.Error as e:
                        print(f"Error verifying database {table_name}: {e}")
                        raise

    def create_database(self, database_name, user):
        try:
            cmd = f'psql -U {self._user} -c "CREATE DATABASE {database_name} OWNER {user};"'
            subprocess.run(cmd, shell=True, text=True)
        except Exception as e:
            raise

    def user_exists():
        pass

    def create_user(self, new_user):
        pass
    def __del__(self):
        if hasattr(self, 'connection') and self.connection is not None:
            self.connection.close()