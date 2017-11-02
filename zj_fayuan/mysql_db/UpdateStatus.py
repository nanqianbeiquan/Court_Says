# coding=utf-8
import datetime
from MySQL import *

MySQL_court = MySQL(config)
MySQL_job = MySQL(config2)
today = datetime.datetime.now().strftime('%Y-%m-%d')


def update_start_status(name):
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_sql = "UPDATE ktgg_job set status=0,start_time= '%s' , updatetime= '%s' where name='%s' " % (
        start_time, today,name)
    MySQL_job.execute_update(start_sql)


def update_end_status(name):
    stop_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stop_sql = "UPDATE ktgg_job set status=1 ,stop_time='%s' where name='%s' " % (stop_time,name)
    MySQL_job.execute_update(stop_sql)
