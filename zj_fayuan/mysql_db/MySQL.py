# coding=utf-8

import mysql.connector
import time
#import TimeUtils


config = {'host': '172.16.0.20',
          'user': 'zhangxiaogang',
          'password': 'gangxiaozhang',
          'port': 3306,
          'database': 'court_notice',
          'charset': 'utf8mb4'
          }

config2 = {'host': '172.16.0.20',
          'user': 'zhangxiaogang',
          'password': 'gangxiaozhang',
          'port': 3306,
          'database': 'job_info',
          'charset': 'utf8mb4'
          }

class MySQL():
    def __init__(self,config):
        self.config=config
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()


    def execute_query(self,sql):
        #global connection, cursor
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.errors.OperationalError:
            print u'mysql连接断开,重新连接...'
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
            return self.execute_query(sql)


    def execute_update(self,sql):
        #global connection, cursor
        try:
            self.cursor.execute(sql)
            self.commit()

        except mysql.connector.errors.OperationalError:
            print u'mysql连接断开,重新连接...'
            print self.config
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
            self.execute_update(sql)


    def execute_many_update(self,sql, args):
        self.cursor.executemany(sql, args)
        self.commit()


    def execute_update_without_commit(self,sql):
        #global connection, cursor
        self.cursor.execute(sql)


    def commit(self):
        #global connection
        self.connection.commit()


    def set_auto_commit_to(self,auto_commit):
        self.connection.autocommit = auto_commit

    def update_begin(self,sql):
        #global connection, cursor
        try:
            self.cursor.execute(sql)
            self.commit()

        except mysql.connector.errors.OperationalError:
            print u'mysql连接断开,重新连接...'
            print self.config
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
            self.execute_update(sql)



if __name__ == '__main__':
    pass
    #res = execute_query("select date(now())")
    #print str(res[0][0]) == TimeUtils.get_today()


