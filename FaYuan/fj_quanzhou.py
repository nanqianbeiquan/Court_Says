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
shi_qu = '泉州市'
conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor = conn.cursor()

for n in range(1, 100):
	url = "http://www.qzcourt.gov.cn/News/ktgg/Index_"+str(n) + '.html'
	host = 'http://www.qzcourt.gov.cn'
	# r = requests.get(url)
	zhu_ye = requests.get(url)
	soup = BeautifulSoup(zhu_ye.text, 'html5lib')
	link_url = soup.find(class_='new4').find_all('a')
	# print link_url
	for i in range(len(link_url)):
		href_list = link_url[i].get('href')
		href = host+href_list
		# print "href:", href
		if 'DetailPage' in href:
			i_d = re.search(r'\d{3,}', href).group()
			# print i,href_list,href,i_d
			xiang_qing=requests.get(href)
			xiang=BeautifulSoup(xiang_qing.text,'html5lib')
			nei_rong=xiang.find_all(class_="xl64")
			len_nr=len(nei_rong)
			for s in range(len_nr/10):
					an_hao=nei_rong[s*10+1].text.strip()
					cheng_ban_ren=nei_rong[s*10+2].text.strip()
					shu_ji_yuan=nei_rong[s*10+3].text.strip()
					he_yi_ting=nei_rong[s*10+4].text.strip()
					ming_cheng=nei_rong[s*10+5].text.strip()
					shen_li=nei_rong[s*10+6].text.strip()
					sj_dd=nei_rong[s*10+7].text.strip().replace('\n','')     #sj_dd 时间+地点
					xuan_pan=nei_rong[s*10+8].text.strip()
					pei_shen=nei_rong[s*10+9].text.strip()
# 					print s,i_d,an_hao,cheng_ban_ren,shu_ji_yuan,cheng_yuan,shi_you,shen_li,sj_dd,xuan_pan,pei_shen
					sql = "INSERT INTO fj_quanzhou VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(i_d,an_hao,cheng_ban_ren,shu_ji_yuan,he_yi_ting,ming_cheng,shen_li,sj_dd,xuan_pan,pei_shen,updatetime,shi_qu)
					print i,sql.encode('gbk','ignore')
					try:
						cursor.execute(sql)
						conn.commit()
					except:
						print 'aaaaa'
