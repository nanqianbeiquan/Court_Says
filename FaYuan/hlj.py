#coding=utf-8

import datetime
import sys
import time

import requests
from bs4 import BeautifulSoup

from ShuiWu import MSSQL

print datetime.datetime.now().strftime('%Y-%m-%d')
# print str(datetime.datetime.now())[0:10]
reload(sys)
sys.setdefaultencoding('utf-8')


updatetime = datetime.datetime.now().strftime('%Y-%m-%d')
# MSSQL.execute_start('ah_susong2nd')


def work(n_start,n_end):
	host = 'http://ssfw.hljcourt.gov.cn/ktggPage.jspx'
	# print r.text
	for p in range(n_start,n_end):
		param={'channelId': 25544, 'listsize': 33536, 'pagego': p}
		r = session.get(url=host, params=param, headers=headers)
		soup = BeautifulSoup(r.text, 'html5lib')
		href_list = soup.find('div', class_='kt_inner').find('ul', class_='kt_list').find_all('li')
		for i,item in enumerate(href_list):
			nei_rong = item.a['title']
			# print u'第%d页%d条'%(p, i), item.a['title']
			sql = "insert into hlj VALUES('%s','%s')" %(nei_rong,updatetime)
			# print u'第%d页%d条'%(p, i),sql.encode('gbk', 'ignore')
			print u'黑龙江---第%d页%d条'%(p, i),sql
			# print u'第%d页%d条'%(p, i),sql
			MSSQL.execute_insert(sql)
	time.sleep(0.3)

# def set_config():
# 	m_list = []
# 	m1 = threading.Thread(target=work,args=(1,10))
# 	m_list.append(m1)
# 	m2 = threading.Thread(target=work,args=(10,20))
# 	m_list.append(m2)
# 	m3 = threading.Thread(target=work,args=(20,30))
# 	m_list.append(m3)
# 	for m in m_list:
# 		m.start()
# 	m.join()

if __name__ == '__main__':
	MSSQL.execute_start('hlj')
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'}
	session = requests.session()
	d1 = datetime.datetime.now()
	print  'start%'*5, d1
	work(1, 400)
	# set_config()
	d2 = datetime.datetime.now()
	print  'stop#'*5, d2
	dd = d2-d1
	print dd, u'一共运行%s秒'%dd
	MSSQL.execute_sop('hlj')
