#coding=utf-8
import os
import sys
import requests
import time
from bs4 import BeautifulSoup
import datetime
import MySQLdb
import threading
import re
from selenium import webdriver
print datetime.datetime.now().strftime('%Y-%m-%d')
reload(sys)
sys.setdefaultencoding('GBK')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='210.16.191.150',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

href_link='http://www.tzcourt.gov.cn/e/action/ShowInfo.php?classid=82&id=3161'
cc = requests.get(href_link)
content=BeautifulSoup(cc.text,'html5lib')
# print content

for s in range(len(content.find_all('span'))):
# for s in range(len(content.find_all('span')[:-2])):
# for s in range((len(content.find_all('span')[:-2]))/14-1):
#    td_list = content.find_all('span')[s].text.strip()
    td_list = content.find_all('span')
#     an_hao = td_list[14*s+18].text.strip()
#     print s,td_list[s].text.strip()
    shi_qu=u'泰州市'
    if s>=7:
        an_hao = td_list[14*s+18].text.strip()
        an_you = td_list[14*s+20].text.strip()
        zhu_shen = td_list[14*s+22].text.strip()
        ri_qi = td_list[14*s+24].text
        shi_jian = td_list[14*s+26].text
        fa_ting = td_list[14*s+28].text
         
    else:
        an_hao = td_list[14*s+20].text.strip()
        an_you = td_list[14*s+22].text.strip()
        zhu_shen = td_list[14*s+24].text.strip()
        ri_qi = td_list[14*s+26].text
        shi_jian = td_list[14*s+28].text
        fa_ting = td_list[14*s+30].text
    time=ri_qi+' ' +shi_jian
    print s,an_hao,an_you,zhu_shen,ri_qi,shi_jian,fa_ting
#     sql = "INSERT INTO js_taizhou VALUES('%s','%s','%s','%s','%s','%s','%s')" %(fa_ting,time,an_hao,an_you,zhu_shen,updatetime,shi_qu)
#     print s,sql.encode('utf8','ignore')
#     try:
#         cursor.execute(sql)
#         conn.commit()
#     except:
#         print 'aaaaa'
     