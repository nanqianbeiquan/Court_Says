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
sys.setdefaultencoding('utf-8')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

host='http://www.szzjfy.com/'
for p in range(1,10):
	url='http://www.szzjfy.com/gonggao.asp?second_id=10001&page='+str(p)
	r = requests.get(url)
	# r.encoding='utf-8'
	soup = BeautifulSoup(r.text,'html5lib')
	zhu_ye = soup.find(class_='news_02').find(class_='list_news_02')
	# print url
	li_list = zhu_ye.find_all('li')
	for n in range(len(li_list)):
		biao_ti=li_list[n].text
		href = host+li_list[n].a['href']
		if biao_ti:
			i_d=re.search(r'\d{3,}',href).group()
	# 		print href_list,href,i_d
			cc = requests.get(href)
			# cc.encoding= 'utf-8'
			xiang_qing = BeautifulSoup(cc.text, 'html5lib')
			p_account = len(xiang_qing.find(class_='article_02').find_all('p'))
			# print 'p_account', p_account
			if p_account==2:
				nei_rong = xiang_qing.find(class_='article_02').find_all('p')[0].text
				cheng_yuan = xiang_qing.find(class_='article_02').find_all('p')[1].text
			elif p_account>2:
				nei_rong = xiang_qing.find(class_='article_02').find_all('p')[0].text
				cheng_yuan = xiang_qing.find(class_='article_02').find_all('p')[2].text
			else:
				nei_rong = xiang_qing.find(class_='article_02').find_all('div')[0].text
				cheng_yuan = xiang_qing.find(class_='article_02').find_all('div')[2].text
			an_hao = biao_ti
# 			print p,n,nei_rong,an_hao,cheng_ban_ren
			sql = "insert into ah_suzhou2nd VALUES('%s','%s','%s','%s','%s')" %(i_d,an_hao,nei_rong,cheng_yuan,updatetime)
			print p,n,sql.decode('gbk', 'ignore')
			try:
				cursor.execute(sql)
				conn.commit()
			except:
				print 'aaaaa'