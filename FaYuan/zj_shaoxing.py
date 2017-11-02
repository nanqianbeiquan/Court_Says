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
print datetime.datetime.now().strftime('%Y-%m-%d')
# print str(datetime.datetime.now())[0:10]
reload(sys)
sys.setdefaultencoding('utf8')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')
shi_qu=u'绍兴市'
conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()


url = "http://www.sxcourt.gov.cn/PaiQiList.asp"
# host='http://www.qzcourt.gov.cn'
# r = requests.get(url)
zhu_ye=requests.get(url )
zhu_ye.encoding = 'gbk'
soup=BeautifulSoup(zhu_ye.text,'html5lib')
table_element=soup.find('table',bgcolor='#D4D0C8')
tr_list=table_element.find_all('tr')
trlen=len(tr_list)
# 	print trlen
cnn=0
for tr in tr_list[1:]:
	cnn+=1
	td_list=tr.find_all('td')
	for td in td_list:
		fa_ting=td_list[0].text.strip()
		kai_ting_ri_qi=td_list[1].text.strip()
		an_hao=td_list[2].text.strip()
		an_you=td_list[3].text.strip()
		dang_shi_ren=td_list[4].text.strip()
		cheng_ban_bu_men=td_list[5].text.strip()
		shen_pan_zhang=td_list[6].text.strip()			
# 	print cnn,fa_ting,kai_ting_ri_qi,an_hao,an_you,dang_shi_ren,cheng_ban_bu_men,shen_pan_zhang
	sql = "INSERT INTO zj_shaoxing VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(fa_ting,kai_ting_ri_qi,an_hao,an_you,dang_shi_ren,cheng_ban_bu_men,shen_pan_zhang,updatetime,shi_qu)
	print cnn,sql.encode('utf8','ignore')
	try:
		cursor.execute(sql)
		conn.commit()
	except:
		print 'aaaaa'







