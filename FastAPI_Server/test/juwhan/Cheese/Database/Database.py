import pymysql
from Database.constant import *
class Database:
    def __init__(self) -> None:

        self.conn=None
        self.cur=None
        self.__connect_db()
        
    def __connect_db(self):
        self.conn=pymysql.connect(host=HOST,user=USER,password=PASSWORD,db=DB_NAME,charset='utf8')
        self.cur=self.conn.cursor()      

    def send_query(self,type,sql):
        pass

    def __read_data(table,sql):
        pass

    def __write_data(table,sql):
        pass

    def __modify_data(table,sql):
        pass

    def __delete_data(table,sql):
        pass