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
url = 'http://ptzy.chinacourt.org/article/index/id/MzAuNzAwNzAwNCACAAA%3D.shtml'
host = 'http://ptzy.chinacourt.org'
r = requests.get(url)
rbs = BeautifulSoup(r.text,'html5lib')
li_list = rbs.find_all(class_='yui3-g list_br')[1].find_all('li')
for i in range(len(li_list)):
	# if i ==1:
		at = li_list[i].find_all('span')[0].a
		linp = at['href']
		link = host+linp
		link_id = re.search(r'\d{6,}',linp).group()
		link_text = at.text.strip()
		# print i,li_list[i].text,link
		r1 = requests.get(link)
		# print r1.content
		r1bs = BeautifulSoup(r1.text,'html5lib')
		# print r1bs
		ta = r1bs.find(class_='detail').find_all('div')[6]
		tap = ta.find_all('p')
		# print i,len(tap)
		if len(tap)==0:
			ash = ta.text.split('\n\n')
			for j in range(len(ash)):
				te = ash[j].strip().replace(' ','').replace('	','').replace('\n','')
				# print 'cccccc',i,j,ash[j].strip().replace(' ','').replace('	','').replace('\n','')
				sql = "insert into putianfy values('%s','%s','%s','%s')" %(link_id,link_text,te,today)
				print i,j, sql
				try:
					cursor.execute(sql)
					conn.commit()
					print 'NEW'
				except:
					print 'OLD'
		if len(tap)==1:
			if i == 39:
				bsh = ta.text.split('。')
				for k in range(len(bsh)):
					if bsh[k].strip()!='':
						te = bsh[k].strip().replace(' ','').replace('	','').replace('\n','')
						# print 'aaaaa',k,bsh[k].strip().replace(' ','').replace('	','').replace('\n','')
						sql = "insert into putianfy values('%s','%s','%s','%s')" %(link_id,link_text,te,today)
						print i,k,sql
						try:
							cursor.execute(sql)
							conn.commit()
							print 'NEW'
						except:
							print 'OLD'
			if i == 40:
				bsh = ta.text.split(' ')
				for k in range(len(bsh)):
					te = bsh[k].strip().replace(' ','').replace('	','').replace('\n','')
					# print '*****',i,k,bsh[k].strip().replace(' ','').replace('	','').replace('\n','')
					sql = "insert into putianfy values('%s','%s','%s','%s')" %(link_id,link_text,te,today)
					print i,k,sql
					try:
						cursor.execute(sql)
						conn.commit()
						print 'NEW'
					except:
						print 'OLD'
		else:
			for k in range(len(tap)):
				te = tap[k].text.strip().replace(' ','').replace('	','').replace('\n','')

				# print 'bbbbb',k,tap[k].text.strip().replace(' ','').replace('	','').replace('\n','')
				sql = "insert into putianfy values('%s','%s','%s','%s')" %(link_id,link_text,te,today)
				print i,k,sql
				try:
					cursor.execute(sql)
					conn.commit()
					print 'NEW'
				except:
					print 'OLD'

conn.close()
