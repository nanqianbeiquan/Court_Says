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

		self.url0 = 'http://www.zhcourt.gov.cn/courtweb/front/ggxxList/J40-splc-up-1-?gglx=kt#up' #u'珠海市中级人民法院'
		self.host = 'http://www.zhcourt.gov.cn'

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
			'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'
			}
			# print headers
			return headers


		
	def mysql_conn(self):

		self.conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
		self.cursor=self.conn.cursor()

	def url_deal(self,n): #u'url改造工厂'
		urlo = self.url0
		url = 'http://www.zhcourt.gov.cn/courtweb/front/ggxxList/J40-splc-down-'+str(n)+'-?gglx=kt#up'
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
		ta = bs.find_all('table')[6].find_all('tr')#[5].find_all('td')[6].find_all('table')[1:-2]
		# for i in range(len(ta)):
		# 	tr_list = ta[i].find_all('tr')#[0]
		# 	# print i,ta_list.text
		# # 	continue
		# 	if len(tr_list)==10:
		# 		print '******************',i,'****************',tr_list[0]
		
		for i in range(len(ta)):
			# if i == 1:
				self.l = i
				tr_list = ta[i].td.a
				# print i,tr_list
				linka = tr_list.get('href')
				link_id = self.re_search(r'\d+',linka)
				link = self.host + linka
				self.an_hao = tr_list.text.strip()
				# print i,link_id,an_hao
				bs = self.quest_getout(link,self.headers_deal())
				self.sub_page(bs)



		# 	an_hao = tr_list[0].find_all('td')[1].text.strip()
		# 	an_you = tr_list[0].find_all('td')[3].text.strip()
		# 	kai_ting_shi_jian = tr_list[0].find_all('td')[5].text.strip()
		# 	kai_ting_di_dian = tr_list[1].find_all('td')[1].text.strip()
		# 	zhu_shen_fa_guan = tr_list[1].find_all('td')[3].text.strip()
		# 	he_yi_ting = tr_list[1].find_all('td')[5].text.strip()
		# 	yuan_gao = tr_list[2].find_all('td')[1].text.strip()
		# 	bei_gao = tr_list[2].find_all('td')[3].text.strip()

		# 	sql = "insert into gzhsfy VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(an_hao,an_you,kai_ting_shi_jian,\
		# 		kai_ting_di_dian,zhu_shen_fa_guan,he_yi_ting,yuan_gao,bei_gao,today)
		# 	print p,i,sql
		# 	self.data_in(sql)


			# if an_hao != '':
			# 	# print 'ft2d'
			# 	# break
			# 	kai_ting_shi_jian = td_list[1].text.strip()+' '+td_list[2].text.strip()
			# 	kai_ting_di_dian = td_list[3].text.strip()
			# 	cheng_ban_fa_guan = td_list[4].text.strip()
			# 	dang_shi_ren = td_list[5]['title'].strip()
			# 	an_you = td_list[6]['title'].strip()

			# 	sql = "insert into ningbofy VALUES ('%s','%s','%s','%s','%s','%s','%s')" %(an_hao,an_you,dang_shi_ren,\
			# 		kai_ting_shi_jian,kai_ting_di_dian,cheng_ban_fa_guan,today)
			# 	print 'page:',p,'line:',i,sql
			# 	self.data_in(sql)
			# # continue
			# # # self.f=i
			# # linka = tr_list[i].find_all('td')[1].a['href']

			# # self.link_text = tr_list[i].text.strip().replace('\n','').replace('  ','')
			# # link = self.host + linka
			# # self.link_id = self.re_search(r'\d+',linka)
			# # # print i,link,link_text,link_id
			# # te = self.quest_getout(link)
			# # self.sub_page(te)

	def sub_page(self,te):  #第一页链接过去的内容，第二子页处理
		bs = self.beaut_souping(te)
		try:
			ph = bs.find('fieldset')
		except:
			print 'last page %s data get' %p
			exit(0) 
		tr_list = ph.find_all('tr')

		kai_shi_shi_jian = tr_list[0].find_all('td')[1].text.strip()
		jie_shu_shi_jian = tr_list[0].find_all('td')[3].text.strip()
		kai_ting_di_dian = tr_list[1].find_all('td')[1].text.strip()
		zhu_shen_fa_guan = tr_list[1].find_all('td')[3].text.strip()
		fa_ting_yong_tu = tr_list[2].find_all('td')[1].text.strip()
		kai_ting_zhuang_tai = tr_list[2].find_all('td')[3].text.strip()

		sql = "insert into zhuhaify Values('%s','%s','%s','%s','%s','%s','%s','%s')" %(self.an_hao,kai_shi_shi_jian,jie_shu_shi_jian,\
			kai_ting_di_dian,zhu_shen_fa_guan,fa_ting_yong_tu,kai_ting_zhuang_tai,today)
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
	for i in range(0,490):
		# if i == 1:
			p = i
			url = cla.url_deal(i)

			headers = cla.headers_deal()
			t = cla.quest_getout(url,headers)

			rin = cla.beaut_souping(t)
			# print rin
			cla.text_analysis(rin)
