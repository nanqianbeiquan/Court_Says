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
import urllib2
import httplib2
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf8')
today = datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

host = 'http://ndzy.chinacourt.org'
rule = r'\d+'
for p in range(1,8):
	# if p == 1:
		url = 'http://ndzy.chinacourt.org/public/more.php?p='+str(p)+'&LocationID=0502000000&sub='

		h = httplib2.Http()
		a,b = h.request(url,'GET')
		# print a,'***',b.decode('gbk')
		ta = b.decode('gbk')
		# print 'type',type(ta)
		tbs = BeautifulSoup(ta,'html5lib')
		span = tbs.find_all(class_='font_text')[3].find_all('table')[0]

		# print p,span
		tr_list = span.find_all('tr')
		for i in range(len(tr_list)):
			link_text = tr_list[i].text.strip().replace('·','').replace(' ','').replace('	','').replace('\n','')
			link_p= tr_list[i].find_all('td')[1].a['href']
			link = host+link_p
			link_id = re.search(rule,link_p).group()
			# print i,link_text,link,link_id
			c,d = h.request(link,'GET')
			dbs = BeautifulSoup(d,'html5lib')
			cn = dbs.find(class_='detail_content')
			# print cn,type(cn)
			con = cn.text.strip().replace('\n','').replace(' ','').replace(' ','').split(u'特此公告')[0]
			# print p,i,con
			sql = "insert into ningdefy VALUES ('%s','%s','%s','%s')" %(link_id,link_text,con,today)
			print p,i,sql
			try:
				cursor.execute(sql)
				conn.commit()
				print 'NEW'
			except:
				print 'OLD'
conn.close()
