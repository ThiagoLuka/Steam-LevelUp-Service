import psycopg2

from singleton.Singleton import Singleton


class DBController(metaclass=Singleton):

    def __init__(self):
        self.__check_dbs_access()

    @staticmethod
    def execute_pg(query: str):
        with DBController.__get_pg_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    @staticmethod
    def __check_dbs_access():
        try:
            DBController.__get_pg_connection()
        except Exception as e:
            print(e)

    @staticmethod
    def __get_pg_connection():
        return psycopg2.connect(DBController.__get_standard_pg_conn_str())

    @staticmethod
    def __get_standard_pg_conn_str() -> str:
        conn_str: str = ''
        with open('db_user.txt', 'r') as file:
            for line in file.readlines():
                conn_str += line.replace('\n', ' ')
        return conn_str
