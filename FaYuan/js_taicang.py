#coding=utf-8
import datetime
import sys
import time

import MSSQL
import MySQLdb
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')
seq = requests.session()
shi_qu = u'苏州'

def run():
	host = 'http://www.jstcfy.gov.cn'
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'}
	for p in range(1, 2):
		end, start  = 20*p, (p-1)*20+1
		params = {'appid': 1,'col': 1,'columnid': 13588 ,'path': '/','permissiontype': 0,'unitid': 38911,\
				  'webid':43, 'webname':u'太仓市人民法院'}
		url = 'http://www.jstcfy.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord='+str(start)+\
			  '&endrecord='+str(end)+'&perpage=20'
		# print url
		r = seq.post(url=url, params=params,headers=headers)
		# print r.text
		soup = BeautifulSoup(r.text,'html5lib')
		item_list = soup.find_all('a')
		for item in item_list[:2]:
			# an_hao = li_list[n].a['title']
			href_1 = item.get('href')
			href = href_1.replace("\\'", '')
			url = host+ href
			# print 'aaa',url
			parse_detail(url)

def parse_detail(url):
	r = seq.get(url)
	r.encoding = 'utf-8'
	soup = BeautifulSoup(r.text,'html5lib')
	item_list = soup.find('table', id='article').find(align="left").find_all('a')
	for item in item_list:
		# print 'bbb', item
		# an_hao = li_list[n].a['title']
		href = item.get('href')
		# print 'bbb', href
		url = 'http://www.jstcfy.gov.cn'+ href
		print 'ccc',url
		down_text(url)

def down_text(url):
	conn_1 = MySQLdb.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang', db='court_notice',
						 charset='utf8')
	cursor_1 = conn_1.cursor()
	r = seq.get(url)
	r.encoding = 'gbk'
	soup = BeautifulSoup(r.text,'html5lib')
	m_list = []
	item_list = soup.text.split('\n')
	for j in range(len(item_list)):
		if item_list[j].strip().replace('\n','') != '':
			item = item_list[j].strip().replace('\n','')
			m_list.append(item)
	# print m_list
	k_list = []
	for m in range(len(m_list)):
		aa = m_list[m]
		k_list.append(aa)
		if u'地　点' in m_list[m]:
			if u'案　号'  in k_list[0].strip() or u'案号'  in k_list[0].strip():
				an_hao = k_list[0].strip()
				an_you = k_list[1].strip()
				nei_rong = k_list[2].strip()
				di_dian = k_list[-1].strip()
				shi_jian = k_list[-3].strip().replace(u'日　期：', '')+k_list[-2].strip().replace(u'时　间：', '')
			elif u'案　由'  in k_list[0].strip() or u'案由'  in k_list[0].strip():
				an_hao = ''
				an_you = k_list[0].strip()
				nei_rong = k_list[1].strip()+k_list[2].strip()
				di_dian = k_list[-1].strip()
				shi_jian = k_list[-2].strip().replace(u'开庭时间:', '')
			sql = "insert into js_taicang VALUES('%s','%s','%s','%s','%s','%s','%s')" \
				  %(an_hao,an_you,nei_rong,shi_jian,di_dian,updatetime,shi_qu)
			# print sql.encode('gbk', 'ignore')
			print sql.encode('utf8', 'ignore')
			k_list = []
			try:
				cursor_1.execute(sql)
				conn_1.commit()
			except:
				print u'数据库已有该数据'
time.sleep(0.3)
MSSQL.execute_start('js_taicang')
run()
MSSQL.execute_sop('js_taicang')
