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
shi_qu='阳江市'
conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()
headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Connection':'keep-alive',
'Host':'www.gdyjfy.gov.cn',
'Referer':'http://www.gdyjfy.gov.cn/sfgk/splc/',
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/45.0',
}
for n in range(291,801):
	url = "http://www.gdyjfy.gov.cn/sfgk/splc/?p"+str(n)+'.html'
	host='http://www.gdyjfy.gov.cn/sfgk/splc/'
	# r = requests.get(url)
	zhu_ye=requests.get(url ,headers=headers)
	zhu_ye.encoding='utf8'
	zy=BeautifulSoup(zhu_ye.text,'html5lib')
	zy_url=zy.find_all("a", target="_blank")
	urllen=len(zy_url)
# 	print zy
	for i in range(urllen): 
# 		print i,zy_url[i]
		href_list=zy_url[i].get('href')
		if 'html' in href_list:
			href=host+href_list
# 		if '（' in zy_url[i].text:
			i_d=re.search(r'\d{4,}',href_list).group()
			xiang_qing=requests.get(href)
			xiang_qing.encoding='utf8'
			nei_rong=BeautifulSoup(xiang_qing.text,'html5lib')
			nr=nei_rong.find(class_="showsp")
			nr_td=nr.text.strip().replace('\n','').replace(' ','').replace('  ','') 
			an_hao=nr_td.split('：',8)[1].strip(u'案由：')
			an_you=nr_td.split('：',8)[2].strip(u'主审法官：')
			zhu_shen=nr_td.split('：',8)[3].strip(u'书记员：')
			shu_ji_yuan=nr_td.split('：',8)[4].strip(u'当事人：')
			dang_shi_ren=nr_td.split('：',8)[5].strip(u'立案时间：')
			li_an=nr_td.split('：',8)[6].strip(u'结案时间：')
			jie_an=nr_td.split('：',8)[7].strip(u'案件状态：')
			zhuang_tai=re.search(u'案件状态.*通',nr_td).group().strip(u'案件状态：').strip(u'通')
	
# 			print i,an_hao,an_you,zhu_shen,shu_ji_yuan,dang_shi_ren,li_an,jie_an,zhuang_tai

			sql = "INSERT INTO gd_yangjiang VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(i_d,an_hao,an_you,zhu_shen,shu_ji_yuan,dang_shi_ren,li_an,jie_an,zhuang_tai,updatetime,shi_qu)
			print n,i,sql.encode('utf8','ignore')
			try:
				cursor.execute(sql)
				conn.commit()
			except:
				print 'aaaaa'
	time.sleep(4)






