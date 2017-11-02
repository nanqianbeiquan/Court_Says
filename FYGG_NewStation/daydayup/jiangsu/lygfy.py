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

url = 'http://www.lygfy.gov.cn/fygg/ktgg/index.html'
# url = 'http://www.lygfy.gov.cn/fygg/ktgg/index1.html'

r = requests.get(url)
r.encoding = 'gb2312'
rbs = BeautifulSoup(r.text,'html5lib')
# print rbs
table_list = rbs.find_all('table')
tr_list = table_list[8].find_all('tr')
conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

cnt = 0
cnt2 = 1
for i in range(len(tr_list)):
	lind = tr_list[i]
	if u'开庭公告' in lind.text and lind.text != None:
		la=lind.a
		link = la['href']

		# print cnt,la.text,'254',link
		if cnt <6:
			r2 = requests.get(link)
			r2.encoding = 'gb2312'
			r2bs = BeautifulSoup(r2.text,'html5lib')
			rp = r2bs.find_all(class_='MsoNormal')
			try:
				an_you = rp[0].text.split('：')[1]
				an_hao = rp[1].text.split('：')[1]
				he_yi_ting = rp[2].text.split('：')[1]
				kai_ting_shi_jian = rp[3].text.split('：')[1]
				kai_ting_di_dian = rp[4].text.split('：')[1]
			except:
				an_you = rp[1].text.split('：')[1]
				an_hao = rp[2].text.split('：')[1]
				he_yi_ting = rp[3].text.split('：')[1]
				kai_ting_shi_jian = rp[4].text.split('：')[1]
				kai_ting_di_dian = rp[5].text.split('：')[1]
			sql = "insert into lygfy values('%s','%s','%s','%s','%s','%s')" %(an_hao,an_you,kai_ting_shi_jian,kai_ting_di_dian,he_yi_ting,today)
			# print cnt, sql
			try:
				cursor.execute(sql)
				conn.commit()
				print 'new'
			except:
				print 'old'
		if cnt>=9 and cnt <13:
			print cnt,link
			rt = requests.get(link)
			rt.encoding = 'gb2312'
			rtbs = BeautifulSoup(rt.text,'html5lib')
			rp = rtbs.find_all(class_='MsoNormal')
			cnt2 = 1
			mn = []
			for j in range(len(rp)):
				if rp[j].text.strip() != '':
					mn.append(rp[j].text.strip().split('：',1)[1])
					# print cnt2,rp[j].text,type(rp[j].text)

					# cnt2 += 1
			# print len(mn),mn[0]
			for i in range(len(mn)/5):
				an_you = mn[i*5]
				an_hao = mn[i*5+1]
				he_yi_ting = mn[i*5+2]
				kai_ting_shi_jian = mn[i*5+3]
				kai_ting_di_dian = mn[i*5+4]
				sql = "insert into lygfy values('%s','%s','%s','%s','%s','%s')" %(an_hao,an_you,kai_ting_shi_jian,kai_ting_di_dian,he_yi_ting,today)
				try:
                                        print cnt,sql
                                except:
                                        print cnt
				try:
					cursor.execute(sql)
					conn.commit()
					print 'new'
				except:
					print 'old'


		cnt += 1
conn.close()
