#coding=utf-8
import os
import sys
import requests
import time
from bs4 import BeautifulSoup
import datetime
import MySQLdb
import json
import threading
import re
from selenium import webdriver
from pip.cmdoptions import src
print datetime.datetime.now().strftime('%Y-%m-%d')
# print str(datetime.datetime.now())[0:10]
reload(sys)
sys.setdefaultencoding('utf8')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')
shi_qu = u'佛山市'
conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

url='http://219.130.221.114/KTGG/KTGG/getKTGG'

headers = {'User-Agent'
# 'Accept':'*/*',
# 'Accept-Encoding':'gzip, deflate',
# 'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
# 'Connection':'keep-alive',
# 'Content-Length':'68',
# 'Host':'www.njfy.gov.cn',
# 'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
# 'Host':'219.130.221.114',
# 'Referer':'http://219.130.221.114/dataImport/demo.html',
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'
}
for n in range(1,10):
	param = {
	'index':n,
	'pageSize':'10',
	'sltCourtPlace':'',
	'txtCaseName':'',
	'txtDate':'',
	'txtKeyword':'',
	}
# browser=webdriver.Firefox()
	r = requests.post(url,data=param, headers =headers)
	# print r.text
	content = json.loads(r.text)
	for i,item in enumerate(content):
		an_hao = item['ah']
		an_you = item['ay']
		kai_ting_ri_qi = item['ktsj']
		fa_ting = item['ktdd']
		shu_ji_guan = item['sjy']
		dang_shi_ren = item['dsrmc'].replace('<br/>', '')
		sql = "insert into gd_foshan VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" %(an_hao,an_you,\
		kai_ting_ri_qi,fa_ting,shu_ji_guan,dang_shi_ren,updatetime,shi_qu)
		print u'第%d页第%d条' %(n, i),sql
		try:
			cursor.execute(sql)
			conn.commit()
		except:
			print 'aaaaa'

