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
# for a in range(1,22):
conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()
p=15
ln = 0
lis = []
for p in range(1,5):
	url = 'http://wxzy.chinacourt.org/public/more.php?p='+str(p)+'&LocationID=1001000000&sub='
	host = 'http://wxzy.chinacourt.org'
	r = requests.get(url)
	# print r.encoding
	r.encoding = 'gb2312'
	rbs = BeautifulSoup(r.text,'html5lib')
	# print rbs
	link_list = rbs.find_all('a')[30:70]
	for i in range(len(link_list)):
		# if i == 4:
			linp = link_list[i]['href'] 
			link = host+linp
			# print i ,link_list[i],link
			bt = requests.get(link)
			btbs = BeautifulSoup(bt.text,'html5lib')
			# print btbs.text
			b_list = btbs.find(class_='detail_content').find_all('p')
			# print b_list.text,type(b_list.text)
			ln = 0
			lis = []
			for j in range(len(b_list)):
				if b_list[j].text.strip()!='':
					nr = b_list[j].text
					lis.append(nr)
					# print ln,j,b_list[j].text
					ln += 1
			print 'lenslis:',len(lis)
			if len(lis)==0:
				print 'irregular rules'
				continue
			for s in range(len(lis)/7):
				try:
					shi_jian = lis[s*7]
					an_hao = lis[s*7+1].split('：',1)[1].strip()
					an_you = lis[s*7+2].split('：',1)[1].strip()
					fa_ting = lis[s*7+3].split('：',1)[1].strip()
					shen_pan_zhang = lis[s*7+4].split('：',1)[1].strip()
					he_yi_ting = lis[s*7+5].split('：',1)[1].strip()
					shu_ji_yuan = lis[s*7+6].split('：',1)[1].strip()
				except Exception as IndexError:
					print 'yaoshoula'
					break

				sql = "insert into wxfy VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(an_hao,an_you,shi_jian,fa_ting,shen_pan_zhang,he_yi_ting,shu_ji_yuan,today)
				try:
                                        print p,i,s,sql
                                except:
                                        print p,i,s
				try:
					cursor.execute(sql)
					conn.commit()
					print 'NEW'
				except:
					print 'Maybe Old'
conn.close()
			# waw = b_list.text.split(' ')
			# for m in range(len(waw)):
			# 	# print m,waw[m],type(waw[m])
			# 	# if m==2:
			# 		# print waw[m]
			# 		c = waw[m].split('\n')
			# 		for n in range(len(c)):
			# 			print m,n,c[n]
			# aa = []
			# for s in range(len(b_list)):
			# 	# if s == 18:
			# 		# print s,b_list[s].text
			# 		aa.append(b_list[s].text.strip('\n\n'))
			# # print le n(aa)
			# for mn in range(len(aa)):
				
			# 	print mn,aa[mn],type(aa[mn])
			# 	if aa[mn]==u'':
			# 		print 'aaaaaaaaaaaa',mn
