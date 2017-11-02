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

shi_qu=u'龙岩市'
conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()
for i in range(1,41):
	host='http://fjlyzy.chinacourt.org/'
	url = "http://fjlyzy.chinacourt.org/public/more.php?p="+str(i)+"&LocationID=0501000000&sub=" 
# 	http://fjlyzy.chinacourt.org/public/more.php?p=2&LocationID=0501000000&sub=
# 	url = "http://sdfy.chinacourt.org/article/index/id/MzDLNzAwNTAwNCACAAA%3D/page/%s.shtml" %i
	r = requests.get(url)
	zhu_ye = BeautifulSoup(r.text,'html5lib')
	link=zhu_ye .find_all(class_="td_line")
# 	print zhu_ye
	# print soup.find_all("span",class_="left").get_attribute('href')
	# for ss in soup.find_all("span",class_="left").get_attribute('href'):
	for ss in range(len(link)):
		link_url=link[ss].a['href']
		link_bt=link[ss].text.strip().replace('\n','').replace(' ','').replace('  ','')     # link_bt 含链接的标题内容
		i_d=re.search(r'\d{3,}',link_url).group()
		href_list=host+link_url
		if u'法庭'  in link_bt or u'审理' in link_bt:
# 		print link_url,type(link_url)
# 			print ss,id,href_list,link_bt
			p= requests.get(href_list)
			xiang_qing=BeautifulSoup(p.text,'html5lib')
			nei_rong=xiang_qing.title.text.strip().replace('\n','').replace(' ','').replace('  ','') [:-11]
#  			print ss,id,nei_rong,updatetime,shi_qu 
 			sql = "INSERT INTO fj_longyan VALUES('%s','%s','%s','%s')" %(i_d,nei_rong,updatetime,shi_qu)
			print sql+";"
			try:
				cursor.execute(sql)
				conn.commit()
			except:
				print 'aaaaa'
