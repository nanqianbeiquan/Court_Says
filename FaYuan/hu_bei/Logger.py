# coding=utf-8

import os
import sys
from codecs import open
import platform
import time
import datetime


def get_time():
    return time.strftime('%X', time.localtime())


def get_today():
    """
    获取当前日期
    :return: 格式化的日期
    :rtype: str
    """
    return str(datetime.date.today())

parent_dir = os.path.join(os.path.dirname(__file__), '../logs')
# print parent_dir
if platform.system() == 'Windows':
    encoding = 'gb2312'
    line_breaks = '\r\n'
else:
    encoding = 'utf-8'
    line_breaks = '\n'


def write(msg, name='', print_msg=False):
    global parent_dir, line_breaks
    if type(msg) != unicode:
        msg = msg.decode('utf-8', 'ignore')
    logs_dir = os.path.join(parent_dir, get_today())
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    file_name = os.path.join(logs_dir, "log_"+name+".txt")
    f = open(file_name, 'a', 'utf-8', 'ignore')
    prefix = get_time() + ' -> '
    msg = msg.replace(line_breaks, line_breaks + ' ' * len(prefix))
    if print_msg:
        print prefix + msg+line_breaks,
    f.write(prefix + msg+line_breaks)
    f.close()

# if __name__ == '__main__':
#     write('12345\n'*10)
#     write('54321\n'*10)
