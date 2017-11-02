# coding=utf-8
import mysql.connector
import time
import MySQLdb

config = {'host': '172.16.0.20',
          'user': 'fengyuanhua',
          'password': 'huayuanfeng',
          'port': 3306,
          'database': 'court_notice',
          'charset': 'utf8'
          }

config2 = {'host': '172.16.0.20',
           'user': 'fengyuanhua',
           'password': 'huayuanfeng',
           'port': 3306,
           'database': 'job_info',
           'charset': 'utf8'
           }

# config = {'host': '192.168.1.28',
#           'user': 'bigdata1',
#           'password': 'aaBigDataZZ123$',
#           'port': 3306,
#           'database': 'dataterminaldb',
#           'charset': 'utf8'
#           }

connection = mysql.connector.connect(**config)
cursor = connection.cursor()


def execute_query(sql):
    global connection, cursor
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except mysql.connector.errors.OperationalError:
        connection.close()
        print u'mysql连接断开,重新连接...'
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        return execute_query(sql)


def execute_update(sql):
    global connection, cursor
    try:
        cursor.execute(sql)
        commit()
    except mysql.connector.errors.OperationalError:
        connection.close()
        print u'mysql连接断开,重新连接...'
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        execute_update(sql)


def execute_many_update(sql, args):
    cursor.executemany(sql, args)
    commit()


def commit():
    global connection
    connection.commit()


def set_auto_commit_to(auto_commit):
    connection.autocommit = auto_commit


def data_to_mysql(sql):
    try:
        job_conn = MySQLdb.connect(host='172.16.0.20', port=3306, user='fengyuanhua', passwd='huayuanfeng',
                                   db='job_info', charset='utf8')
        job_cursor = job_conn.cursor()
        try:
            job_cursor.execute(sql)
            job_conn.commit()
        except Exception as e:
            print e
    except Exception as e:
        if e[0] == 2003:
            time.sleep(7)
            data_to_mysql(sql)

# if __name__ == '__main__':
#     while True:
#         test_sql = 'select * from  tyc.job_info'
#         res = execute_query(test_sql)
#         print res
#         # test_sql = "SHOW STATUS LIKE 'Qcache%'"
#         # res = execute_query(test_sql)
#         # print res[2]
#         time.sleep(2)
