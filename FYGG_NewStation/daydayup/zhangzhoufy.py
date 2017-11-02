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

host = 'http://www.zzcourt.gov.cn'  #辣鸡网站，共18页5~9页打不开，频繁登录封ip半个小时
rule = r'\d+(?=\.)'
headers = {
'Host':'www.zzcourt.gov.cn',
'Referer':'http://www.zzcourt.gov.cn',
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'
}
# hel = urllib.urlencode(headers)
for p in range(7,10):
	# if p == 15:
		url = 'http://www.zzcourt.gov.cn/plus/list.php?tid=22&TotalResult=243&PageNo='+str(p)

		h = httplib2.Http()
		c1,c2 = h.request(url,'GET',headers=headers)
		# print c2
		c2bs = BeautifulSoup(c2,'html5lib')
		ul = c2bs.find(class_='news_ul mt15')
		try:
			li_list = ul.find_all('li')
		except:
			print u'网页%s没内容，继续' %p
			continue
		for i in range(len(li_list)):

			lind = li_list[i].a['href']
			link_id = re.search(rule,lind).group()
			link = host + lind
			link_text = li_list[i].span.text.strip().replace('\n','')+' '+li_list[i].a.text.strip().replace('\n','')
			# print p,i,link_text,link,link_id
			c3,c4 = h.request(link,'GET',headers=headers)
			c4bs = BeautifulSoup(c4,'html5lib')
			c4c = c4bs.find(class_='news_xiangxi')
			try:
				a = c4c.text.strip()
			except:
				print u'网页%s的%s不存在' %(p,i)
				continue
			if c4c.text.strip() == '':
				tex = c4bs.find(class_='xiangxi_head').text.strip()
				sql = "insert into zzcourt VALUES ('%s','%s','%s','%s')" %(link_id,link_text,tex,today)
				try:
                                    print 'if',p,i,sql
                                except:
                                    print 'if',p,i
				try:
					cursor.execute(sql)
					conn.commit()
					print 'NEW'
				except:
					print 'OLD'
			else:
				cp = c4c.find_all('p')
				# print 'else',p,i,'lencp',len(cp)
				if len(cp) == 0:
					tex = c4c.text.strip()
					sql = "insert into zzcourt VALUES ('%s','%s','%s','%s')" %(link_id,link_text,tex,today)
					try:
                                            print p,i,sql
                                        except:
                                            print p,i
					try:
						cursor.execute(sql)
						conn.commit()
						print 'NEW'
					except:
						print 'OLD'
				elif len(cp) > 0:
					cnt=1
					for k in range(len(cp)):
						if cp[k].text.strip() != '' and len(cp[k].text.strip())>10: 
							tex = cp[k].text.strip().replace('\n','')
							# print 'else22',p,i,k,tex,len(tex)
							sql = "insert into zzcourt VALUES ('%s','%s','%s','%s')" %(link_id,link_text,tex,today)
							#print p,i,cnt,sql
							cnt += 1
							try:
								cursor.execute(sql)
								conn.commit()
								print 'NEW'
							except:
								print 'OLD'

conn.close()
