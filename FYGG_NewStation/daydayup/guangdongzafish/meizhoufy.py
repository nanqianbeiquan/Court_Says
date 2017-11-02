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
import urllib
import urllib2
import httplib2
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf8')
today = datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

host = 'http://www.mzcourt.gov.cn'
rule = r'(?<=nggonggao/).*(?=\.)'
for p in range(1,15):
	# if p==5:
		url = 'http://www.mzcourt.gov.cn/fayuangonggao/kaitinggonggao/list_43_'+str(p)+'.html'

		h = httplib2.Http()
		try:
                    tec,te = h.request(url,'GET')
                except:
                    continue
		tbs = BeautifulSoup(te.decode('gbk'),'html5lib')
		try:
			li_list = tbs.find(class_='news_pic_list').find_all('li')
		except:
			print u'第%s页暂时无法打开' %p
			continue
		for i in range(len(li_list)):
			# if i ==2:
				lind = li_list[i].a['href']
				link_id = re.search(rule,lind).group().replace('/','')
				link_text = li_list[i].text.strip().replace('\n','')
				if u'无开庭' not in link_text:
					if u'开庭安排' in link_text:
						link = host+lind
						# print p,i,link,link_text
						te2h,te2 = h.request(link,'GET')
						t2bs = BeautifulSoup(te2.decode('gbk'),'html5lib')
						try:
							con = t2bs.find(class_='article_content_wrap').text
							# print '**',i,con
						except:
							print u'子页面没加载出来，继续'
							continue
						tk = con.split('\n')
						ml = []
						ct = 0

						for j in range(len(tk)):
							if tk[j].strip() !='':
								ml.append(tk[j])
								ct += 1
								# print '```.```',i,j,tk[j]
						print u'字典长度',len(ml)
						if len(ml)==1:
							tex = u'12月24日（星期二）'+ml[0]
							# print p,i,k,tex.strip()
							sql = "insert into meizhoufy VALUES ('%s','%s','%s','%s')" %(link_id,link_text,tex,today)
							try:
								print p,i,i,sql
							except:
								print p,i,
							try:
								cursor.execute(sql)
								conn.commit()
								print 'NEW'
							except:
								print 'OLD'
						for k in range(1,len(ml)):
							tex = ml[0].strip()+ml[k]
							# print p,i,k,tex
							sql = "insert into meizhoufy VALUES ('%s','%s','%s','%s')" %(link_id,link_text,tex,today)
							print p,i,k,sql
							try:
								cursor.execute(sql)
								conn.commit()
								print 'NEW'
							except:
								print 'OLD'
					else:
						link = host+lind
						# print p,i,link,link_text
						te2h,te2 = h.request(link,'GET')
						t2bs = BeautifulSoup(te2.decode('gbk'),'html5lib')
						try:
							con = t2bs.find(class_='article_content_wrap').text
							# print '**',i,con
						except:
							print u'子页面没加载出来，继续'
							continue
						tk = con.split('\n')
						ml = []
						ct = 0
						if len(tk)>100:
							cons = t2bs.find(class_='article_content_wrap').find_all('tr')
							for k in range(1,len(cons)):
								tex = cons[k].text.strip().replace('\n','').replace('	','').replace(' ','')
								# print p,i,k,tex
								sql = "insert into meizhoufy VALUES ('%s','%s','%s','%s')" %(link_id,link_text,tex,today)
								try:
									print p,i,k,sql
								except:
									print p,i,k
								try:
									cursor.execute(sql)
									conn.commit()
									print 'NEW'
								except:
									print 'OLD'
							continue
						for j in range(len(tk)):
							if tk[j].strip() !='':
								ml.append(tk[j])
								ct += 1
								# print '```.```',i,j,tk[j]
						print u'字典长度',len(ml)
						for k in range(1,len(ml)):
							tex = ml[k].strip().replace('\n','').replace('	','')
							# print p,i,k,tex
							sql = "insert into meizhoufy VALUES ('%s','%s','%s','%s')" %(link_id,link_text,tex,today)
							try:
								print p,i,k,sql
							except:
								print p,i,k
							try:
								cursor.execute(sql)
								conn.commit()
								print 'NEW'
							except:
								print 'OLD'
conn.close()
