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
shi_qu=u'泰州市'
conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

for p in range(0,8):
	url = "http://www.tzcourt.gov.cn/e/action/ListInfo/index.php?page="+str(p)+"&classid=82&totalnum=143"
# 	url = "http://www.tzcourt.gov.cn/e/action/ListInfo/?classid=82"
	r = requests.get(url)
	so = BeautifulSoup(r.text,'html5lib')
	soup=so.find(class_='box',cellspacing='0')
	ul_list=soup.find_all('ul')
	# print soup
	link=soup.find_all('a')
	# print len(link)
	for i in range(len(link)):
		href_link=soup.find_all('a')[i].get('href')
		gong_shi=soup.find_all('a')[i].text
		if u'开庭告示' in gong_shi or u'庭审告示' in gong_shi:
			i_d=re.search(r'\d{3,}',href_link).group()
	# 		print href_link,gong_shi
			cc= requests.get(href_link)
			content=BeautifulSoup(cc.text,'html5lib')
			table=content.find(id='text')
			tr_element_list = table.find_all('tr')
			# td_element_list = content.find_all('td')
	# 		print 'len(tr)' ,len(tr_element_list [1:])
			for tr_element in tr_element_list [1:]:
				td_element_list = tr_element.find_all('td')
				an_hao = td_element_list[0].text.strip().replace('\n','')
				an_jian_ming_chen =  td_element_list[1].text.strip().replace('\n','')
				zhu_shen =  td_element_list[2].text.strip().replace('\n','')
				ri_qi =  td_element_list[3].text.strip().replace('\n','')
				fa_ting =  td_element_list[4].text.strip().replace('\n','')
	# 			print i,an_hao ,an_jian_ming_chen,zhu_shen,ri_qi,fa_ting
				sql = "INSERT INTO js_taizhou VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" %(i_d,an_hao ,an_jian_ming_chen,zhu_shen,ri_qi,fa_ting,updatetime,shi_qu)
				print p,i,sql.encode('utf8','ignore')
				try:
					cursor.execute(sql)
					conn.commit()
				except:
					print 'aaaaa'		     




