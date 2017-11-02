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
sys.setdefaultencoding('utf8')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')
shi_qu='肇庆市'

MSSQL.execute_start('gd_zhaoqing')
for p in range(1, 100):
	url = "http://ssfw.gdzqfy.gov.cn/ktxx.aspx?cateId=15&page="+str(p)
	host='http://www.qzcourt.gov.cn'
	# r = requests.get(url)
	zhu_ye=requests.get(url )
	soup=BeautifulSoup(zhu_ye.text,'html5lib')
	table_element=soup.find(id='tbData')
	tr_list=table_element.find_all('tr')
	trlen=len(tr_list)
# 	print trlen
	for tr in tr_list[1:]:
		td_list=tr.find_all('td')
		for td in td_list:
			ri_qi=td_list[0].text.strip()
			shi_jian=td_list[1].text.strip()
			fa_ting=td_list[2].text.strip()
			an_hao=td_list[3].text.strip()
			an_you=td_list[4].text.strip()
			zhu_shen=td_list[5].text.strip()
			dang_shi_ren=td_list[6].text.strip()			
# 		print p,ri_qi,shi_jian,fa_ting,an_hao,an_you,zhu_shen,dang_shi_ren
		sql = "INSERT INTO gd_zhaoqing VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(an_hao,ri_qi,shi_jian,fa_ting,an_you,zhu_shen,dang_shi_ren,updatetime,shi_qu)
		print p,sql.encode('utf8','ignore')
		MSSQL.execute_insert(sql)
	time.sleep(0.5)
MSSQL.execute_sop('gd_zhaoqing')







