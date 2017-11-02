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
sys.setdefaultencoding('utf-8')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

host = 'http://sqzy.chinacourt.org'
url="http://sqzy.chinacourt.org/article/index/id/MzBONDBIMTAwNCACAAA%3D/page/2.shtml" 
cc = requests.get(url)
# print cc.encoding
cc.encoding = 'utf-8'
content=BeautifulSoup(cc.text,'html5lib')
# print content 
td=content.find_all('a',target="_blank")
nian_list=content.find_all('span',class_="right")
# print nian_list
cnn = 0


for s in range(len(td)):
    href_link=td[s].get('href')
#     print s, href_link,td[s].text.strip()
    if u'人民法院' in td[s].text.strip():
#         print cnn,href_link
#         print s, href_link,td[s].text.strip()
        cnn +=1
        shi_qu=u'宿迁市'
        link=host+href_link
#         print cnn,link,td[s].text.strip()
        pp = requests.get(link)
        aa = BeautifulSoup(pp.text,'html5lib')
        bt=aa.find_all('div',class_="b_title")[0].get_text()
        sj=re.search(r'\d{1,}.*\d{1,}',bt).group()
        i_d=re.search(r'\d{6,}',link).group()
        shi_jian=str(2012)+u'年'+sj+u'日'
        shi_qu=u'宿迁市'   
        dd=aa.find_all('p',class_="MsoNormal")
        for t in range(len(dd)):
            nei_rong1 = dd[t].text.strip() 
#             print id,nei_rong,shi_jian,updatetime,shi_qu
            sql = "INSERT INTO js_suqian VALUES('%s','%s','%s','%s','%s')" %(i_d,nei_rong1,shi_jian,updatetime,shi_qu)
            print s,sql
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                print "aaaaaa"
        xiang_qing2=aa.find_all('p',class_="p0")
        for c in range(len( xiang_qing2)):
            nei_rong2 = xiang_qing2[c].text.strip() 
            sql = "INSERT INTO js_suqian VALUES('%s','%s','%s','%s','%s')" %(i_d,nei_rong2,shi_jian,updatetime,shi_qu)
            print s,sql
            try:
                cursor.execute(sql)
                conn.commit()     
            except:
                print "aaaaaa"
        xiang_qing3=aa.find_all('p')
        for c in range(len( xiang_qing3)):
            nei_rong3 = xiang_qing3[c].text.strip() 
            sql = "INSERT INTO js_suqian VALUES('%s','%s','%s','%s','%s')" %(i_d,nei_rong3,shi_jian,updatetime,shi_qu)
            print s,sql
            try:
                cursor.execute(sql)
                conn.commit()     
            except:
                print "aaaaaa"
                
