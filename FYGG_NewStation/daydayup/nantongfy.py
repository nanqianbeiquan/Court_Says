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
url = 'http://www.ntfy.gov.cn/channels/542.html'

host = 'http://www.ntfy.gov.cn'
cnt = 1
r = requests.get(url)
# print r.encoding
r.encoding = 'gb2312'
rbs = BeautifulSoup(r.text,'html5lib')
# print rbs
table_list = rbs.find('table',class_='innercontent').find_all('table')
for i in range(len(table_list)):
	if table_list[i].text=='':
		print 'mmmmiiiiaaaaaoooooo'
		continue
	if i == len(table_list)-1:
		print 'meeeeeeeee'
		continue
	afix = table_list[i].find('td').a['href']
	link = host + afix
	link_id = re.search(r'\d{4,}',link).group()
	# print i,table_list[i].find('td').text,link
	rs = requests.get(link)
	rs.encoding = 'gb2312'
	rsbs = BeautifulSoup(rs.text,'html5lib')
	# print i,rsbs
	an_you = rsbs.find(id = 'artibodyTitle').text.strip().replace('\n','').replace(' ','').replace('	','')
	# print 'an_you:',an_you
	tr_list = rsbs.find(id = 'artibody').find_all('tr')
	# print len(tr_list)
	shi_jian = tr_list[0].find_all('td')[1].text.strip()
	fa_ting = tr_list[1].find_all('td')[1].text.strip()
	shen_pan_zhang = tr_list[2].find_all('td')[1].text.strip()
	he_yi_ting = tr_list[3].find_all('td')[1].text.strip()
	shu_ji_yuan = tr_list[4].find_all('td')[1].text.strip()
	sql = "insert into ntfy VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" %(link_id,an_you,\
		shi_jian,fa_ting,shen_pan_zhang,he_yi_ting,shu_ji_yuan,today)
	print 1,cnt,sql
	cnt += 1
	try:
		cursor.execute(sql)
		conn.commit()
		print '1 %s NEW' %cnt
	except:
		print 'OLD'
for l in range(2,20):
	url_sub = 'http://www.ntfy.gov.cn/channels/542_'+str(l)+'.html'
	r = requests.get(url_sub)
	# print r.encoding
	r.encoding = 'gb2312'
	rbs = BeautifulSoup(r.text,'html5lib')
	# print rbs
	table_list = rbs.find('table',class_='innercontent').find_all('table')
	cnt = 1
	for i in range(len(table_list)):
		if table_list[i].text=='':
			print 'mmmmiiiiaaaaaoooooo'
			continue
		if i == len(table_list)-1:
			print 'meeeeeeeee'
			continue
		afix = table_list[i].find('td').a['href']
		link = host + afix
		link_id = re.search(r'\d{4,}',link).group()
		# print i,table_list[i].find('td').text,link
		rs = requests.get(link)
		rs.encoding = 'gb2312'
		rsbs = BeautifulSoup(rs.text,'html5lib')
		# print i,rsbs
		an_you = rsbs.find(id = 'artibodyTitle').text.strip().replace('\n','').replace(' ','').replace('	','')
		# print 'an_you:',an_you
		tr_list = rsbs.find(id = 'artibody').find_all('tr')
		# print len(tr_list)
		shi_jian = tr_list[0].find_all('td')[1].text.strip()
		fa_ting = tr_list[1].find_all('td')[1].text.strip()
		shen_pan_zhang = tr_list[2].find_all('td')[1].text.strip()
		he_yi_ting = tr_list[3].find_all('td')[1].text.strip()
		shu_ji_yuan = tr_list[4].find_all('td')[1].text.strip()
		sql = "insert into ntfy VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" %(link_id,an_you,\
			shi_jian,fa_ting,shen_pan_zhang,he_yi_ting,shu_ji_yuan,today)
		print l,cnt,sql
		cnt += 1

		try:
			cursor.execute(sql)
			conn.commit()
			print '%s %s NEW' %(l,cnt)
		except:
			print '%s %s OLD' %(l,cnt)
conn.close()
print 'over'
