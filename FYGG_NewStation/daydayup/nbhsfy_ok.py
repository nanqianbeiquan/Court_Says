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



class court_mighty(object):

	param = {}
	headers = {}
	
	def __init__(self):  # u'初始化参数等等'

		self.url0 = 'http://www.nbhsfy.cn/more.jsp?cid=004001&page=1' #u'宁波海事法院'
		self.host = 'http://www.nbhsfy.cn'

		
	def mysql_conn(self):

		self.conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
		self.cursor=self.conn.cursor()

	def url_deal(self,n): #u'url改造工厂'
		urlo = self.url0
		url = 'http://www.nbhsfy.cn/more.jsp?cid=004001&page='+str(n)
		print url
		return url

	def quest_getout(self,url):  #httplib2

		h = httplib2.Http()
		he,co = h.request(url,'GET')
		return co

	def quest_getout1(self,url): #urllib2

		req = urllib2.urlopen(url).read()
		return req

	def quest_getout2(self,url): #requests

		r = requests.get(url)
		print r.encoding
		#r.encoding = 'gbk'  #u'乱码情况使用'
		return r

	def quest_postout(self,url): #httplib2

		data = urllib.encode(param)    #u'带参数的需要对参数进行加工'
		h = httplib2.Http()
		he,co = h.request(url,'POST',data,headers)
		return co

	def quest_postout1(self,url): #urllib2

		data = urllib.encode(param)
		req = httplib2.Request(url)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
		con = opener.open(req,data).read()
		return con

	def quest_postout2(self,url): #requests

		r = requests.post(url,data,headers)
		# print r.encoding
		# r.encoding = 'gbk'
		return r




	def beaut_souping(self,thn): # Beautifulsoup处理网页文本,有乱码情况

		mat = thn
		bs = BeautifulSoup(mat,'html5lib')
		return bs

	def re_search(self,rule,strings):
		res = re.search(rule,strings).group()
		return res

	def text_analysis(self,bs):
		ta = bs.find_all('table')
		# for i in range(len(ta)):
		# 	tr_list = ta[i].find_all('tr')
		# 	if len(tr_list)>10:
		# 		print '******************',i,'****************',tr_list[0]
		tr_list = ta[9].find_all('tr')
		for i in range(len(tr_list)):
			# print i,tr_list[i]
			self.f=i
			linka = tr_list[i].find_all('td')[1].a['href']

			self.link_text = tr_list[i].text.strip().replace('\n','').replace('  ','')
			link = self.host + linka
			self.link_id = self.re_search(r'\d+',linka)
			# print i,link,link_text,link_id
			te = self.quest_getout(link)
			self.sub_page(te)

	def sub_page(self,te):
		bs = self.beaut_souping(te)
		ph = bs.find(id='Zoom2')
		p_list = ph.find_all('p')
		for i in range(len(p_list)):
			# print i,p_list[i]

			tex = p_list[i].text.strip().replace('\n','').replace('　','')
			if tex != '':
				sql = "insert into nbhsfy VALUES('%s','%s','%s','%s')" %(self.link_id,self.link_text,tex,today)
				print p,self.f,i,sql
				self.data_in(sql)



	def data_in(self,sql):
		try:
			self.cursor.execute(sql)
			self.conn.commit()
			print 'NEW'
		except:
			print 'OLD'



if __name__ == '__main__':
	cla = court_mighty()
	cla.mysql_conn()
	for i in range(2,12):
		# if i == 1:
			p=i
			url = cla.url_deal(i)
			t = cla.quest_getout(url)
			rin = cla.beaut_souping(t)
			# print rin
			cla.text_analysis(rin)

	# pass
