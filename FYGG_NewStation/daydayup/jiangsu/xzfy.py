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
p=93
ln = 0
lis = []
for p in range(1,93):
	url = 'http://xzzy.chinacourt.org/public/more.php?p='+str(p)+'&LocationID=0205000000&sub='
	host = 'http://xzzy.chinacourt.org'
	r = requests.get(url)
	print r.encoding
	r.encoding = 'gbk'
	rbs = BeautifulSoup(r.text,'html5lib')
	# print rbs
	tb_list = rbs.find(class_='item_pad').find_all('tbody')
	# print len(tb_list) #3
	tr_list = tb_list[1].find_all('tr')
	# print len(tr_list)
	for i in range(len(tr_list)):
		# if i==3 and u'开庭公告' in tr_list[i].text:
			tda = tr_list[i].find_all('td')[1].a
			linp = tda['href']
			link = host+linp
			link_id = re.search(r'\d{4,}',link).group()
			link_text = tda.text.strip()
			# print i,link_text,link,link_id

			r2 = requests.get(link)
			r2bs = BeautifulSoup(r2.text,'html5lib')
			cc = r2bs.find(class_='detail_content')
			# if cc.text.strip() == '':
			# 	print 'ssdfs'
			# 	break
			ccp =cc.find_all('p')
			if len(ccp)==0:
				print 'pattern changed go except'
				# continue
			# print ccp[0]
			try:
				cc_lost = cc.text[:cc.text.index('。')].strip() 
				# print cc_lost,type(cc_lost),len(ccp)
				sqlt = "insert into xzfy VALUES('%s','%s','%s','%s')"%(link_id,link_text,cc_lost,today)
				try:
                                        print p,i,sqlt
                                except:
                                        print p,i
				try:
					cursor.execute(sqlt)
					conn.commit()
					print 'try cc_lost',p,i,'NEW'
				except:
					print 'try cc_lost',p,i,'a OLD'
			except Exception as ValueError:
				ccp1 =r2bs.find('b').text.strip()
				sqlc = "insert into xzfy VALUES('%s','%s','%s','%s')"%(link_id,link_text,ccp1,today)
				try:
                                        print p,i,sqlc
                                except:
                                        print p,i
				try:
					cursor.execute(sqlc)
					conn.commit()
					print 'except pass',p,i,'NEW'
				except:
					print 'except pass',p,i,'a OLD'
				continue
			# print 'lenccp:',len(ccp)
			for j in range(len(ccp)):
				if ccp[j].text.strip() != '':
					ccpj = ccp[j].text.strip()
					# print j,ccpj
					sql = "insert into xzfy VALUES('%s','%s','%s','%s')"%(link_id,link_text,ccpj,today)
					try:
                                                print p,i,j,sql
                                        except:
                                                print p,i,j
					try:
						cursor.execute(sql)
						conn.commit()
						print 'NEW'
					except:
						print 'OLD'
conn.close()
