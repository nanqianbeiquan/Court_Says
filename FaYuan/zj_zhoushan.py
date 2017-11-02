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
shi_qu='舟山市'
conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

for p in range(9,16):
	url = "http://www.zscourt.cn/index.php?m=content&c=index&a=lists&catid=89&page="+str(p)
	host='http://www.qzcourt.gov.cn'
	# r = requests.get(url)
	zhu_ye=requests.get(url)
	soup=BeautifulSoup(zhu_ye.text,'html5lib')
	link_url=soup.find('ul',class_='new1')
	a_list=link_url.find_all('li')
# 	print link_url
	for i in range(len(a_list)):
		href_list=a_list[i].a['href']
		i_d=re.search(r'\d{3,}',href_list).group()
# 		print i,href_list,i_d
		p=requests.get(href_list)
		xiang_qing=BeautifulSoup(p.text,'html5lib')
		nei_rong=xiang_qing.find('div',style="padding:5px 15px;")
		td_text=nei_rong.text.split()
		firlist=[]
		for n in range(len(td_text)):
# 			if u'舟山市中级人民法院' not in td_text[n]:
			if td_text[n].strip().replace('\n','') != '':
				sh = td_text[n].strip().replace('\n','')
				firlist.append(sh)
		seclist=[]
		
		cnn = 0
		for m in range(len(firlist)):
			aa = firlist[m]
			seclist.append(aa)
			if u'开庭法庭：' in firlist[m]:
				cnn+=1
				an_hao = seclist[0]
				an_you= seclist[1]
				nei_rong = ' '.join(seclist[2:-2])
				shi_jian=seclist[-2]
				fa_ting = seclist[-1]
# 				print an_hao,shi_jian,fa_ting
				sql = "insert into zj_zhoushan VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" %(i_d,an_hao,an_you,nei_rong,fa_ting,shi_jian,updatetime,shi_qu)
				print p,i,cnn,sql
				seclist = [] 
				try:
					cursor.execute(sql)
					conn.commit()
				except:
					print 'aaaaa'

		





