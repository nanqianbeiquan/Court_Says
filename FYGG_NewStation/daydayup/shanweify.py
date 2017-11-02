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
import urllib
import urllib2
import httplib2
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf8')
today = datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

host = 'http://www.swzy.gov.cn'
rule = r'(?<=&id=).*'
rule2 = u'本院.*特此公告'
for p in range(8):
	# if p==1:
		url = 'http://www.swzy.gov.cn/newslist.aspx?page='+str(p)+'&MenuID=02020401'

		te = urllib2.urlopen(url).read()
		# print te
		tbs = BeautifulSoup(te,'html5lib')
		table_list = tbs.find(class_='mlist').find_all('li')
		for i in range(len(table_list)):
			tl = table_list[i].a
			lind = tl['href']
			link_id = re.search(rule,lind).group()
			link_text = tl.text.strip().strip(u'开庭公告')
			link = host+lind
			# print p,i,link_id,link_text
			te2 = urllib2.urlopen(link).read()
			t2bs = BeautifulSoup(te2,'html5lib')
			tiv = t2bs.find(class_='decon').text.strip().replace('\n','').\
			replace(' ','').replace('	','').replace(' ','').replace('　','')
			red = re.search(rule2,tiv).group().strip(u'特此公告')
			sql = "insert into shanweify VALUES('%s','%s','%s','%s')" %(link_id,link_text,red,today)
			print p,i,sql
			try:
				cursor.execute(sql)
				conn.commit()
				print 'NEW'
			except:
				print 'OLD'
conn.close()
