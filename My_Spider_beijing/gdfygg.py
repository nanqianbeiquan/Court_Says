#coding=utf-8
import os
import sys
import requests
import time
from bs4 import BeautifulSoup
import datetime
import MySQLdb
import threading

reload(sys)
sys.setdefaultencoding('utf8')
conn = MySQLdb.connect(host='210.16.191.150',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

url = 'http://www.gdcourts.gov.cn/ecdomain/framework/gdcourt/hnohoambadpabboeljehjhkjkkgjbjie.jsp?gglx=1&ggbt=&countNum=12&endRowNum=12&pageclickednumber=1'
urltest = 'http://www.gdcourts.gov.cn/ecdomain/framework/gdcourt/hnohoambadpabboeljehjhkjkkgjbjie.jsp?gglx=1&ggbt=&countNum=12&endRowNum=180120&pageclickednumber=15010'
# f = open('D://hshfy.txt','a')
host = 'http://www.gdcourts.gov.cn'
print 'starttime:'+time.ctime()
# url = 'http://www.bjcourt.gov.cn/ktgg/index.htm'
# url1 = 'http://www.bjcourt.gov.cn/ktgg/index.htm?c=&court=&start=&end=&type=&p=11'
# url = 'http://www.bjcourt.gov.cn/ktgg/index.htm?c=&court=&start=&end=&type=&p=11'
r = requests.get(url)
# r = requests.session()
# r.get(url1)
# time.sleep(10)
# s = r.get(url)
content = BeautifulSoup(r.text,'html5lib')
# c_list = content.find('form').table.tbody.tr.td[2].find_all('tr')
c_list = content.find('form').find_all('tbody')[6].find_all('tr')
# print len(c_list)
for i in range((len(c_list)-3)/2):
# print i,c_list[2*i+1]
	td_list = c_list[2*i+1].find_all('td')
	an_ha0 = td_list[0].text.strip()
	# print an_hao
	link_url_proto = td_list[0].find('a').get('href').strip().replace('\n','')
	fa_yuan = td_list[1].text.strip()
	ri_qi = td_list[2].text
	che_xiao = td_list[3].text
	# print 'aaa',link_url
	link_url = ''.join(str(link_url_proto).split())
	content_url = host + link_url
	# print td_list[0]

	# print '2',content_url

	cc = requests.get(content_url)
	# print cc.content
	# time.sleep(0.5)
	ccbs = BeautifulSoup(cc.text,'html5lib')
	cc_table = ccbs.find('table',class_='table_list_B')

	# print 'aaaeg',cc_table
	cc_tr = cc_table.find_all('tr')

	an_hao = cc_tr[0].find_all('td')[1].text.strip()
	kai_ting_shi_jian = cc_tr[1].find_all('td')[1].text.strip()
	kai_ting_di_dian = cc_tr[2].find_all('td')[1].text.strip()
	dang_shi_ren = cc_tr[3].find_all('td')[1].text.strip()
	zhu_shen_fa_guan = cc_tr[4].find_all('td')[1].text.strip()
	geng_xin_shi_jian = cc_tr[5].find_all('td')[1].text.strip()
	fa_ting_yong_tu = cc_tr[6].find_all('td')[1].text.strip()
	shi_fou_che_xiao = cc_tr[7].find_all('td')[1].text.strip()
	SQL = u"INSERT INTO gdcourts VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(fa_yuan,an_hao,kai_ting_shi_jian,\
		kai_ting_di_dian,dang_shi_ren,zhu_shen_fa_guan,geng_xin_shi_jian,fa_ting_yong_tu,shi_fou_che_xiao)
	print i,SQL
	try:
		cursor.execute(SQL)
		conn.commit()
		print 'PAGE  the %s anhao %s is NEW' %(i+1,an_ha0)
	except:
		print 'PAGE  the %s anhao %s ALREADY HAVE' %(i+1,an_ha0)
conn.close()
# print 'endtime:'+time.ctime()
