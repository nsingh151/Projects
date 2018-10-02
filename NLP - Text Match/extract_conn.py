import termcolor
import pyodbc
import pandas as pd

'''
 Class to make db connections, pull data from sql and store in dataframe in pandas

'''

class Sql_connection():


    def __init__(self, connection_info,
                 db='glglive', verbose=1):
        """
        homogenizes the rules of engagement for interacting the the database
        :param connection_info: dict: keys with hostname, username, password
        :param db: str: name of the DB to connect to
        """
        self.verbose = verbose
        self.connection_info = connection_info
        self.db = db
        self.db_conn = self.connection()
        self.test_connection()

    def connection(self, db=None):
        """
        Create a connection that will last the entirety of the object
        :param db: name of the DB to connect to
        :return: dict: {conn: <pyodbc connection object>, cursor: <pyodbc cursor object>}
        """

        if db is None:
            db = self.db

        con_str = """
                DRIVER={{ODBC Driver 13 for SQL Server}};
                SERVER={hostname};
                UID={username};
                PWD={password};
                DATABASE=""".format(**self.connection_info)
        con_str = '{}{};'.format(con_str, db)
        conn = pyodbc.connect(con_str, autocommit=True)
        cursor = conn.cursor()
        return {'conn': conn, 'cursor': cursor}

    def query(self, sql, ret_type='GET'):
        """
        Execute a query against the DB
        :param sql: str: actual SQL query string to be executed
        :param ret_type: str: [PUT, GET]. PUT writes to DB & returns nothing, GET is read only
        :return: pandas.DataFrame (GET only)
        """

        cursor = self.db_conn['cursor']
        conn = self.db_conn['conn']
        if ret_type == 'PUT':
            cursor.execute(sql)
            conn.commit()
            if self.verbose == 2:
                print(colored('Executed query succesfully:', 'green'))
                print(sql)
            return None
        elif ret_type == 'GET':
            data = pd.read_sql(sql, conn)
            if self.verbose == 2:
                print(colored('Executed query succesfully:', 'green'))
                print(data)
            return data

    def test_connection(self, db='GLGLIVE'):
        """
        Simple connection test
        :param db: name of the DB to test a connection against. Defaults to GLGLIVE
        :return: None (throws error on bad connection)
        """

        if self.verbose > 1:
            print('Testing Database Connectivity')

        try:
            sql = "select * from sysdatabases where name = '{}'".format(db)
            sys_data = self.query(sql, 'GET')
            assert not sys_data.empty
            if self.verbose > 1:
                print(colored('Connection Established with {} DB'.format(db), 'green'))
        except Exception as e:
            raise ConnectionError(colored('{}\nconnection failed against {}'.format(e, db), 'red'))
        return None
    

## Connection String 
DATABASE = {
    # --------------------
    'hostname': '***.**.*.**',  -- your DB server name
    # --------------------
    'username': '****',           -- Username
    'password': '******'      -- Password
}
