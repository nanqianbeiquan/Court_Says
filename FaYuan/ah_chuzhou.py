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
shi_qu=u'滁州市'
# print str(datetime.datetime.now())[0:10]
reload(sys)
sys.setdefaultencoding('utf-8')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

w = requests.get('http://www.czfy.gov.cn/html/ktgg/index.html')
w.encoding='utf-8'
soup = BeautifulSoup(w.text,'html5lib')
# 	print 222
zhu_ye1 = soup.find(width='766')
zhu_ye2=zhu_ye1.find_all(align='center')[1].find_all('a')
# 	zhu_ye2=zhu_ye1.find_all(align='center')[1].find_all('tr')
for n in range(len(zhu_ye2)):
	zhu_ye = zhu_ye2[n]
	if u'(2' in zhu_ye.text:
		href=zhu_ye.get('href')
		i_d=re.search(r'\d{4,}',href).group()
# 		print n,href,zhu_ye.text,i_d
		cc = requests.get(href)
		cc.encoding='utf-8'
		xiang_qing = BeautifulSoup(cc.text,'html5lib')
  
		nei_rong1=xiang_qing.find(class_='a6')
		nei_rong3=nei_rong1.text.strip().replace('\n','').replace(' ','').replace('  ','')
		nei_rong2=nei_rong1.text.strip().split()
		an_hao=nei_rong3.split('案　由：')[0]
		an_you1=nei_rong1.text.strip().split()[3]
		an_you=u'案'+an_you1
# 		for i in range(len(nei_rong2)):
		nei_rong = ' '.join(nei_rong2[4:])
		sql = "insert into ah_chuzhou2nd VALUES('%s','%s','%s','%s','%s')" %(an_hao,an_you,nei_rong,updatetime,shi_qu)
		print '1',sql
		try:
			cursor.execute(sql)
			conn.commit()
		except:
			print 'aaaaa'  

for p in range(2,111):
	url='http://www.czfy.gov.cn/html/ktgg/index_'+str(p)+'.html'
# 	print url
	r = requests.get(url)
	r.encoding='utf-8'
	soup = BeautifulSoup(r.text,'html5lib')
# 	print 222
	zhu_ye1 = soup.find(width='766')
	zhu_ye2=zhu_ye1.find_all(align='center')[1].find_all('a')
# 	zhu_ye2=zhu_ye1.find_all(align='center')[1].find_all('tr')
	for n in range(len(zhu_ye2)):
		zhu_ye= zhu_ye2[n]
		if u'(2' in zhu_ye.text:
			href=zhu_ye.get('href')
# 			print n,href,zhu_ye.text
			cc = requests.get(href)
			cc.encoding='utf-8'
			xiang_qing = BeautifulSoup(cc.text,'html5lib')
 
			nei_rong1=xiang_qing.find(class_='a6')
			nei_rong3=nei_rong1.text.strip().replace('\n','').replace(' ','').replace('  ','')
			nei_rong2=nei_rong1.text.strip().split()
			an_hao=nei_rong3.split('案　由：')[0]
			an_you1=nei_rong1.text.strip().split()[3]
			an_you=u'案'+an_you1			
			nei_rong = ' '.join(nei_rong2[4:])
			sql = "insert into ah_chuzhou2nd VALUES('%s','%s','%s','%s','%s')" %(an_hao,an_you,nei_rong,updatetime,shi_qu)
			print p,n,sql
			try:
				cursor.execute(sql)
				conn.commit()
			except:
				print 'aaaaa'  