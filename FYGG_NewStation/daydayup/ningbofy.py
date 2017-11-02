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
# 	'cid':7507,
# 	'data':'{:data_0:}|{:data_1:}|1000',
# 	'help_kpi_id':'',
# 	}
# 	headers = {
# 	'Accept':'*/*',
# 	'Accept-Encoding':'gzip, deflate',
# 	'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
# 	'Connection':'keep-alive',
# 	'Content-Length':53,
# 	'Content-Type':'application/x-www-form-urlencoded',
# 	'Cookie':"""ASP.NET_SessionId=pvthvxy1e4y5yuuablifto3l; jixiao_yan=2; jixiao_yan1=2; jixiao_ways_id=; jixiao_menu_task_id
# =; jixiao_task_list=; jixiao_task_name_list=; jixiao_task_start=1; jixiao_help_name=%e6%89%80%e6%9c%89
# %e5%bc%80%e5%ba%ad; jixiao_task_id=0; jixiao_round_id=0; urdate=cid=7506""",
# 	'Host':'ygsf.nbcourt.gov.cn',
# 	'Referer':'http://ygsf.nbcourt.gov.cn/treemanager.aspx?cid=7507&data={:data_0:}|{:data_1:}|1000',
# 	'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
# 	'X-Requested-With':'XMLHttpRequest',
# 	}
	
	def __init__(self):  # u'初始化参数等等'

		self.url0 = 'http://ygsf.nbcourt.gov.cn/services/gettree.aspx?start=&page=treemanager.aspx' #u'宁波阳光司法网'
		self.host = 'http://ygsf.nbcourt.gov.cn/pubserver.aspx?datas=727F28FAAA329671C4263813824E120BDB9A686F8885851832418CB5376A62D8AA9AE7093E551E9A'

	def param_deal(self,n): # u'参数修改，n为页数'
		cc = '{:data_0:}|{:data_1:}|'+str(n)
		param = {
				'cid':7507,
				'data':cc,
				'help_kpi_id':'',
				}
		return param

	def headers_deal(self,n):
			headers = {
				# 'Accept':'*/*',
				# 'Accept-Encoding':'gzip, deflate',
				# 'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
				# 'Connection':'keep-alive',
				# 'Content-Length':53,
				'Content-Type':'application/x-www-form-urlencoded',
				# 'Cookie':'ASP.NET_SessionId=pvthvxy1e4y5yuuablifto3l; jixiao_yan=2; jixiao_yan1=2; jixiao_ways_id=; jixiao_menu_task_id\
				# =; jixiao_task_list=; jixiao_task_name_list=; jixiao_task_start=1; jixiao_help_name=%e6%89%80%e6%9c%89\
				# %e5%bc%80%e5%ba%ad; jixiao_task_id=0; jixiao_round_id=0; urdate=cid=7506',
				# 'Host':'ygsf.nbcourt.gov.cn',
				# 'Referer':'http://ygsf.nbcourt.gov.cn/treemanager.aspx?cid=7507&data={:data_0:}|{:data_1:}|'+str(n),
				'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
				# 'X-Requested-With':'XMLHttpRequest',
				}
			return headers


		
	def mysql_conn(self):

		self.conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
		self.cursor=self.conn.cursor()

	def url_deal(self): #u'url改造工厂'
		urlo = self.url0
		url = 'http://ygsf.nbcourt.gov.cn/services/gettree.aspx?start=&page=treemanager.aspx'
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
		ta = bs.find(class_='table')
		# for i in range(len(ta)):
		# 	tr_list = ta[i].find_all('tr')
		# 	if len(tr_list)>10:
		# 		print '******************',i,'****************',tr_list[0]
		tr_list = ta.find_all('tr')
		for i in range(1,len(tr_list)):
			td_list = tr_list[i].find_all('td')

			an_hao = td_list[0].text.strip()
			if an_hao != '':
				# print 'ft2d'
				# break
				kai_ting_shi_jian = td_list[1].text.strip()+' '+td_list[2].text.strip()
				kai_ting_di_dian = td_list[3].text.strip()
				cheng_ban_fa_guan = td_list[4].text.strip()
				dang_shi_ren = td_list[5]['title'].strip()
				an_you = td_list[6]['title'].strip()

				sql = "insert into ningbofy VALUES ('%s','%s','%s','%s','%s','%s','%s')" %(an_hao,an_you,dang_shi_ren,\
					kai_ting_shi_jian,kai_ting_di_dian,cheng_ban_fa_guan,today)
				print 'page:',p,'line:',i,sql
				self.data_in(sql)
			# continue
			# # self.f=i
			# linka = tr_list[i].find_all('td')[1].a['href']

			# self.link_text = tr_list[i].text.strip().replace('\n','').replace('  ','')
			# link = self.host + linka
			# self.link_id = self.re_search(r'\d+',linka)
			# # print i,link,link_text,link_id
			# te = self.quest_getout(link)
			# self.sub_page(te)

	def sub_page(self,te):  #第一页链接过去的内容，第二子页处理
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
	for i in range(1,8045):
		# if i == 1:
			p = i

			url = cla.url_deal()
			# print url
			# continue
			param=cla.param_deal(i)
			headers = cla.headers_deal(i)
			t = cla.quest_postout(url,param,headers)
			rin = cla.beaut_souping(t)
			# print rin
			cla.text_analysis(rin)
