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

shi_qu=u'玉林市'
# href_list= "http://www.zjzy.gov.cn/col79/articleinfo.php?infoid=13041"
for p in range(1, 7):
	url = 'http://ylszy.chinacourt.org/article/index/id/M8g0NzAwMTAwMiACAAA%3D/page/'+str(p)+'.shtml'
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html5lib')
	detail_list = soup.find_all('ul')[6].find_all('li')
	i = 0
	for detail in detail_list:
		i += 1
		title = detail.find('a').text
		# print 'title:', detail
		if u'开庭' in title or u'开 庭' in title:
			# href_list =detail.find('span')
			# print 'href_list:', href_list
			href_list = detail.find('span').a['href']
			i_d = re.search(r'\d{5,}', href_list).group()
			href = 'http://ylszy.chinacourt.org'+href_list
			r = requests.get(href)
			detail = BeautifulSoup(r.text, 'html5lib')
			cc = detail.find(class_='text').text.split('\n')
			klist = []
			for j in range(len(cc)):
				if cc[j].strip() != '':
					sh = cc[j].strip().replace('\n', '')
					klist.append(sh)
			# print 'klist:', len(klist), klist
			kmist = []
			cnn = 0
			for m in range(len(klist)):
				aa = klist[m]
				kmist.append(aa)
				# print 'kmist:', kmist
				if u'成员' in klist[m]:
					try:
						cnn += 1
						an_hao = kmist[0]
						nei_rong = kmist[1]
						shi_jian = kmist[2]
						fa_ting = kmist[-2]
						cheng_yuan = kmist[-1]
						sql = "insert into gx_yulin2nd VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" %\
							  (i_d,an_hao,nei_rong,shi_jian,fa_ting,cheng_yuan,updatetime,shi_qu)
						print p,i,cnn,sql
						kmist = []
					except:
						cnn += 1
						an_hao = kmist[0]
						nei_rong = kmist[1]
						shi_jian = ''
						fa_ting = kmist[-2]
						cheng_yuan = kmist[-1]
						sql = "insert into gx_nanning2nd VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" %\
							  (i_d,an_hao,nei_rong,shi_jian,fa_ting,cheng_yuan,updatetime,shi_qu)
						print p,i,cnn,u'有问题啊',sql
						kmist = []
					try:
						cursor.execute(sql)
						conn.commit()
					except:
						print 'aaaaa'