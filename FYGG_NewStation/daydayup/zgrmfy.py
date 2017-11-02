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

reload(sys)
sys.setdefaultencoding('utf8')
today = datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()
for p in range(1,37):
	url = 'http://www.court.gov.cn/fabu-gengduo-14.html?page=35'+str(p)
	host = 'http://www.court.gov.cn'
	try:
		r = requests.get(url,timeout=20)
	except:
		print 'page %s is not load ok now'
		continue
	rbs = BeautifulSoup(r.text,'html5lib')
	rt = rbs.find(class_='sec_list').find('ul')
	ll = rt.find_all('li')
	for i in range(len(ll)):
		la = ll[i].a
		linp = la['href']
		try:
			link_id = re.search(r'\d{3,}',linp).group()
		except:
			print '*******bad*id*******',p,i
			continue
		link = host + linp
		link_text = la.text.strip().replace('\n','').replace(' ','').replace('	','').replace('　','')
		# print i,link_id,link

		r1=requests.get(link)
		r1bs = BeautifulSoup(r1.text,'html5lib')
		rte = r1bs.find(class_='txt_txt')
		try:
			tt = rte.text.strip().replace('\n','').replace(' ','').replace('	','').replace('　','')
			# print i,tt
		except:
			print 'NoneType has no text'
			continue
		sql = "insert into zgrmfy VALUES ('%s','%s','%s','%s')" %(link_id,link_text,tt,today)
		print p,i,sql
		try:
			cursor.execute(sql)
			conn.commit()
			print 'NEW'
		except:
			print 'OLD'

conn.close()
