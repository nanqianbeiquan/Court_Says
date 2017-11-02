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

# 	param = {

# 	}
# 	headers = {
# 	'Accept':'*/*',
# 	'Accept-Encoding':'gzip, deflate',
# 	'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',

# 	'Content-Type':'application/x-www-form-urlencoded',
# 	'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
# 	}
	
	def __init__(self):  # u'初始化参数等等'

		self.url0 = 'http://www.zsfy.gov.cn/pqkt.asp' #u'中山市中级人民法院'
		self.host = 'http://14.215.113.28:8180'

	def param_deal(self,n): # u'参数修改，n为页数'
		cc = '{:data_0:}|{:data_1:}|'+str(n)
		param = {
				'cid':7507,
				'data':cc,
				'help_kpi_id':'',
				}
		return param

	def headers_deal(self):
			headers = {
			# 'Accept-Encoding':'gzip, deflate',
			'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
			}
			# print headers
			return headers


		
	def mysql_conn(self):

		self.conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
		self.cursor=self.conn.cursor()

	def url_deal(self,n): #u'url改造工厂'
		urlo = self.url0

		url = 'http://www.zsfy.gov.cn/pqkt.asp?currpage='+str(n)
		print url
		return url

	def quest_getout(self,url,headers):  #httplib2

		h = httplib2.Http()
		he,co = h.request(url,'GET',headers=headers)
		return co

	def quest_getout1(self,url,headers): #urllib2
		req = urllib2.Request(url,headers=headers)
		requ = urllib2.urlopen(req).read()
		return requ

	def quest_getout2(self,url,headers): #requests,可接headers
		print url

		r = requests.get(url,headers=headers)
		# r = requests.get(url,headers)
		print r.encoding
		#r.encoding = 'gbk'  #u'乱码情况使用'
		return r.text

	def quest_postout(self,url,param,headers): #httplib2

		data = urllib.urlencode(param)    #u'带参数的需要对参数进行加工'
		print data
		h = httplib2.Http()
		he,co = h.request(url,'POST',data,headers)
		# he,co = h.request(url,'POST',data)
		return co.decode('utf-8')

	def quest_postout1(self,url): #urllib2

		data = urllib.urlencode(param)
		req = httplib2.Request(url)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
		con = opener.open(req,data).read()
		return con

	def quest_postout2(self,url,data): #requests

		# r = requests.post(url,data,headers)
		r = requests.post(url,data)
		# print r.encoding
		# r.encoding = 'gbk'
		return r.text




	def beaut_souping(self,thn): # Beautifulsoup处理网页文本,有乱码情况

		mat = thn
		bs = BeautifulSoup(mat,'html5lib')
		return bs

	def re_search(self,rule,strings): #正则截取匹配内容
		res = re.search(rule,strings).group()
		return res

	def text_analysis(self,bs):   #第一页网站数据抓取
		ta = bs.find('tr',align='center')
		divList = ta.find_all('div')
		lenDiv = len(divList)
		for i in range(lenDiv-2):
			# print 'oao',i,divList[i].table.tbody.find_all('tr')[0].text.strip().split(':')[1]
			an_hao = divList[i].table.tbody.find_all('tr')[0].text.strip().split(':')[1]
			an_you = divList[i].table.tbody.find_all('tr')[1].text.strip().split('：')[1]
			dang_shi_ren = divList[i].table.tbody.find_all('tr')[2].text.strip().split('：')[1]
			kai_ting_time = divList[i].table.tbody.find_all('tr')[3].text.strip().split('：')[1]
			kai_ting_place = divList[i].table.tbody.find_all('tr')[4].text.strip().split('：')[1]
			sql = "insert into zhongshanfy VALUES('%s','%s','%s','%s','%s','%s')" %(an_hao,an_you,dang_shi_ren,\
				kai_ting_time,kai_ting_place,today)
			print p,i,sql
			self.data_in(sql)


			# # self.link_text = tr_list[i].text.strip().replace('\n','').replace('  ','')
			# # link = self.host + linka
			# # self.link_id = self.re_search(r'\d+',linka)
			# # # print i,link,link_text,link_id
			# # te = self.quest_getout(link)
			# # self.sub_page(te)

	def sub_page(self,te):  #第一页链接过去的内容，第二子页处理
		bs = self.beaut_souping(te)
		# print bs
		# try:
		# 	divs = bs.find('fieldset')
		# except:
		# 	print 'last page %s reach,go break' %p
		# 	exit(0)

		# print divs
		try:
			ph = bs.find('fieldset')
		except:
			print 'last page %s data get' %p
			exit(0) 
		tr_list = ph.find_all('tr')

		kai_shi_shi_jian = tr_list[0].find_all('td')[1].text.strip()
		jie_shu_shi_jian = tr_list[0].find_all('td')[3].text.strip()
		kai_ting_di_dian = u'第'+tr_list[1].find_all('td')[1].text.strip()+u'法庭'
		zhu_shen_fa_guan = tr_list[1].find_all('td')[3].text.strip()
		fa_ting_yong_tu = tr_list[2].find_all('td')[1].text.strip()
		# kai_ting_zhuang_tai = tr_list[2].find_all('td')[3].text.strip()

		# kai_shi_shi_jian = divs.find_all(class_='item')[0].find_all('li')[0].text.strip()
		# jie_shu_shi_jian = divs.find_all(class_='item')[0].find_all('li')[1].text.strip()
		# kai_ting_di_dian = divs.find_all(class_='item1')[0].find_all('li')[0].text.strip()
		# zhu_shen_fa_guan = divs.find_all(class_='item1')[0].find_all('li')[1].text.strip()
		# fa_ting_yong_tu = divs.find_all(class_='item')[1].find_all('li')[0].text.strip()
		# kai_ting_zhuang_tai = divs.find_all(class_='item')[1].find_all('li')[1].text.strip()

		sql = "insert into chaozhoufy Values('%s','%s','%s','%s','%s','%s','%s')" %(self.an_hao,kai_shi_shi_jian,jie_shu_shi_jian,\
			kai_ting_di_dian,zhu_shen_fa_guan,fa_ting_yong_tu,today)
		print p,self.l,sql
		self.data_in(sql)

		# for i in range(len(tr_list)):
		# 	print i,tr_list[i]

			# tex = p_list[i].text.strip().replace('\n','').replace('　','')
			# if tex != '':
			# 	sql = "insert into nbhsfy VALUES('%s','%s','%s','%s')" %(self.link_id,self.link_text,tex,today)
			# 	print p,self.f,i,sql
			# 	self.data_in(sql)



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
	for i in range(0,370):
		# if i == 0:
			p = i
			url = cla.url_deal(i)

			headers = cla.headers_deal()
			t = cla.quest_getout(url,headers)

			rin = cla.beaut_souping(t)
			# print rin
			cla.text_analysis(rin)
