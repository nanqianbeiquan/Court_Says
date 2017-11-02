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
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf8')
today = datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

host = 'http://www.npfy.gov.cn'
# url = 'http://www.npfy.gov.cn/e/action/ListInfo/?classid=20'
#0~71
rule = r'(?<=&id=).*'
for p in range(72):
	# if p == 71:
		url = 'http://www.npfy.gov.cn/e/action/ListInfo/index.php?page='+str(p)+'&classid=20&totalnum=1796'
		t=urllib2.urlopen(url)
		tt = t.read().decode('gbk')
		# print tt
		bs = BeautifulSoup(tt,'html5lib')
		cc = bs.find(class_='newslist')
		li_list = cc.find_all('li')
		print len(li_list)
		for i in range(len(li_list)):
			link_text = li_list[i].text.strip().replace('\n','')
			link_p = li_list[i].a['href']
			link_id = re.search(rule,link_p).group()
			link = host+link_p
			# print p,i,link,link_id
			st = urllib2.urlopen(link).read().decode('gbk')
			bst = BeautifulSoup(st,'html5lib')
			con = bst.find(class_='pageshows').find(class_='pageconpage').text.strip().replace('\n','').replace('	','').replace('　　','').replace('  ','',)
			# print i,con
			sql = "insert into nanpingfy VALUES ('%s','%s','%s','%s')" %(link_id,link_text,con,today)
			print p,i,sql
			try:
				cursor.execute(sql)
				conn.commit()
				print 'NEW'
			except:
				print 'OLD'
conn.close()
