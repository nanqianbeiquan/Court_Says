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
shi_qu=u'马鞍山市'
# print str(datetime.datetime.now())[0:10]
reload(sys)
sys.setdefaultencoding('utf-8')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

host='http://maszy.chinacourt.org'
for p in range(1, 6):
	url='http://maszy.chinacourt.org/article/index/id/MyhONDBIMyAOAAA%3D/page/'+str(p)+'.shtml'
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html5lib')
	zhu_ye = soup.find(id='list', class_='font14 dian_a')
	li_list = zhu_ye.find_all('li')
	print 'len(li_list)', len(li_list)
	for n in range(len(li_list)):
	# for n in range(16, 17):
		biao_ti = li_list[n].a['title']
		href_list = li_list[n].a['href']
		href = host+href_list
		if u'开庭公告' in biao_ti:
			i_d = re.search(r'\d{5,}', href_list).group()
			cc = requests.get(href)
			# cc.encoding='utf-8'
			xiang_qing = BeautifulSoup(cc.text,'html5lib')
			if u'详细内容请点击链接' in xiang_qing:
				pass
			else:
				nei_rong1 = xiang_qing.find(class_='detail')
				nei_rong2 = nei_rong1.find_all('div')[6]
				# print nei_rong2
				len_tr = len(nei_rong2.find_all('tr'))
				print 'tr_list:', p, n, len_tr
				if len_tr > 1:
					nei_rong2.find_all('tr')
					tr_list = nei_rong2.find_all('tr')
					for tr in tr_list[1:]:
						nei_rong = tr.text.replace('\n', 'br')
						sql = "insert into ah_maanshan2nd VALUES('%s','%s','%s','%s')" % (i_d,nei_rong,updatetime,shi_qu)
						print u'表格:', p, n, sql
						try:
							cursor.execute(sql)
							conn.commit()
						except:
							print 'aaaaa'
				else:
					nei_rong3 = nei_rong2.text.split('\n')
					klist = []
					for j in range(len(nei_rong3)):
						if nei_rong3[j].strip().replace('\n', '') != u'':
							nr1 = nei_rong3[j].replace('\n', '')
							klist.append(nr1)
					kmist = []
					cnn = 0
					for m in range(len(klist)):
						nei_rong = klist[m]
						sql = "insert into ah_maanshan2nd VALUES('%s','%s','%s','%s')" % (i_d,nei_rong,updatetime,shi_qu)
						print u'文本',p,n,sql
						kmist = []
						try:
							cursor.execute(sql)
							conn.commit()
						except:
							print 'aaaaa'