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
# print str(datetime.datetime.now())[0:10]

reload(sys)
sys.setdefaultencoding('utf-8')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

shi_qu = u'北海市'
# href_list= "http://www.zjzy.gov.cn/col79/articleinfo.php?infoid=13041"
for p in range(1,12):
	url = 'http://bhzy.chinacourt.org/public/more.php?p='+str(p)+'&LocationID=1001000000&sub=00'
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html5lib')
	detail = soup.find(class_='bodyTable').find(class_='Eitem_pad')
	# print 'detail:', detail
	item_list =detail.find_all('tr')
	i = 0
	for item in item_list[:-1]:
		i += 1
		title = item.find(class_='td_line').text
		href_list = item.find(class_='td_line').a['href']
		i_d = re.search(r'\d{3,}', href_list).group()
		href = 'http://bhzy.chinacourt.org'+href_list
		r = requests.get(href)
		detail = BeautifulSoup(r.text, 'html5lib')
		nei_rong = detail.find('span', class_='detail_content').text.strip().replace(' ', '')
		sql = "insert into gx_beihai2nd VALUES('%s','%s','%s','%s','%s')" %\
			  (i_d,title,nei_rong,updatetime,shi_qu)
		print p,i,sql.decode('gbk', 'ignore')
		try:
			cursor.execute(sql)
			conn.commit()
		except:
			print 'aaaaa'





