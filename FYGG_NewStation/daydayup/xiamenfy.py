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
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf8')
today = datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()
host = 'http://202.101.105.162:8099/court/ktgg/'
for p in range(1,4):

	url = 'http://202.101.105.162:8099/court/ktgg/ktgg_list_'+str(p)+'.xhtml?page='+str(p)

	r = requests.get(url)
	rbs = BeautifulSoup(r.text,'html5lib')
	print rbs
	tr_list = rbs.find_all(class_='xmfyw_sxl_ctab f_c t14 h14')[1].find_all('tr')
	print len(tr_list)
	for i in range(1,len(tr_list)):
		td = tr_list[i].find_all('td')[5].a
		linp = td['href']
		link_id = re.search(r'\d{6,}',linp).group()
		link = host + linp
		# print i,tr_list[i].text,link
		r1=requests.get(link)
		r1bs = BeautifulSoup(r1.text,'html5lib')
		r_tr = r1bs.find(class_='xmfyw_sxl_ctab t14').find_all('tr')

		fa_yuan_ming_cheng = r_tr[0].find_all('td')[1].text.strip()
		an_hao = r_tr[1].find_all('td')[1].text.strip()
		kai_ting_shi_jian = r_tr[2].find_all('td')[1].text.strip()
		kai_ting_di_dian = r_tr[3].find_all('td')[1].text.strip()
		fa_guan = r_tr[4].find_all('td')[1].text.strip()
		cheng_ban_ting = r_tr[5].find_all('td')[1].text.strip()
		shu_ji_yuan = r_tr[6].find_all('td')[1].text.strip()
		an_jian_shuo_ming = r_tr[7].find_all('td')[1].text.strip()

		sql = "insert into xiamenfy VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(link_id,an_hao,fa_yuan_ming_cheng,\
			kai_ting_shi_jian,kai_ting_di_dian,fa_guan,cheng_ban_ting,shu_ji_yuan,an_jian_shuo_ming,today)
		print p,i,sql
		try:
			cursor.execute(sql)
			conn.commit()
			print 'NEW'
		except:
			print 'OLD'

conn.close()


