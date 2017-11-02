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

shi_qu=u'南宁市'
# href_list= "http://www.zjzy.gov.cn/col79/articleinfo.php?infoid=13041"
for p in range(1, 6):
	url = 'http://nnzy.chinacourt.org/article/index/id/M0g3MzAwNTAwNCACAAA%3D/page/'+str(p)+'.shtml'
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html5lib')
	detail_list = soup.find_all('ul')[4].find_all('li')
	i = 0
	for detail in detail_list:
		i += 1
		title = detail.find('a').text
		# print 'title:', title
		if u'开庭公告' in title:
			# href_list =detail.find('span')
			# print 'href_list:', href_list
			href_list =detail.find('span').a['href']
			i_d = re.search(r'\d{5,}', href_list).group()
			href = 'http://nnzy.chinacourt.org'+href_list
			r = requests.get(href)
			detail = BeautifulSoup(r.text, 'html5lib')
			cc = detail.find_all(class_='text')[1].text.split('\n')
			# print 'len_cc:', len(cc)
			klist=[]
			for j in range(len(cc)):
				# print cc[j]
				if cc[j].strip() != '':
					sh = cc[j].strip().replace('\n', '')
					klist.append(sh)
			# print 'klist:', klist
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
						sql = "insert into gx_nanning2nd VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" %\
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
						print p,i,cnn,sql
						kmist = []
					try:
						cursor.execute(sql)
						conn.commit()
					except:
						print 'aaaaa'





