#coding=utf-8
import os
import sys
import requests
import MSSQL
from bs4 import BeautifulSoup
import datetime
import MySQLdb
import threading
import re
from ShuiWu.SpiderMan import SpiderMan

reload(sys)
sys.setdefaultencoding('utf8')

class GuangZhouSearcher(SpiderMan):
	def __init__(self):
		super(GuangZhouSearcher, self).__init__(keep_session=True)

	def run(self):
		today = datetime.datetime.now().strftime('%Y-%m-%d')
		# url = 'http://www.gzcourt.org.cn/fygg/ktgg/'
		MSSQL.execute_start('guang_zhou')
		url = 'http://www.gzcourt.gov.cn:8080/ywxt/bulletin/bulletin_1.jsp'
		conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
		cursor=conn.cursor()
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'}
		for n in range(1,169):
			param = {
			'aymc':'',
			'cbrr':'',
			'court_jc':'',
			'dsrc':'',
			'fydm':'440100',
			'ktrqend':'',
			'ktrqstart':'',
			'no':'',
			'pageIndex':n,
			'type1':'',
			'year':'',
			}
			try:
				# r = requests.post(url,data=param)
				r = self.post(url,data=param, headers=headers)
			except:
				print 'page cante %s reach' %n
				continue
			rbs = BeautifulSoup(r.text,'html5lib')
			# print rbs
			table = rbs.find(class_='font10_black')
			tr_list = table.find_all('tr')
			for i in range(1,len(tr_list)):
				# print i,tr_list[i]
				td_list = tr_list[i].find_all('td')
				kai_ting_ri_qi = td_list[1].text.strip()
				an_hao = td_list[2].text.strip()
				an_you = td_list[3].text.strip()
				zhu_shen_fa_guan = td_list[4].text.strip()
				shen_li_fa_ting = td_list[5].text.strip()
				fa_yuan_ming_cheng = td_list[6].text.strip()
				sql = "insert into gzcourt VALUES ('%s','%s','%s','%s','%s','%s','%s')" %(an_hao,an_you,kai_ting_ri_qi,\
					zhu_shen_fa_guan,shen_li_fa_ting,fa_yuan_ming_cheng,today)
				print n,i,sql
				try:
					cursor.execute(sql)
					conn.commit()
					print 'NEW'
				except:
					print 'OLD'
		MSSQL.execute_sop('guang_zhou')
		conn.close()

if __name__ == '__main__':
	searcher = GuangZhouSearcher()
	searcher.run()