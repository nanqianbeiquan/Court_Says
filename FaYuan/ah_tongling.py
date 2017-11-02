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

# host='http://www.jsczfy.gov.cn/ktgg/'
# soup = BeautifulSoup(r.text,'html5lib')
# print soup.prettify()

shi_qu=u'铜陵市'
# href_list= "http://www.zjzy.gov.cn/col79/articleinfo.php?infoid=13041"
for p in range(1,7):
	url = 'http://www.tlcourt.gov.cn/content/channel/53f5b7649a05c2e402215423/page-'+str(p)+'/'
	host='http://www.tlcourt.gov.cn'
	zhu_ye=requests.get(url)
	soup=BeautifulSoup(zhu_ye.text,'html5lib')
	link_url=soup.find('ul',class_='is-listnews')
	a_list=link_url.find_all('li')
	for i in range(len(a_list)):
		bt=a_list[i].text.strip()
		href_list=a_list[i].a['href']
		if u'开庭公告' in bt:
			href=host+href_list
			cc=requests.get(href)
			cc.encoding='utf-8'
			xiang_qing=BeautifulSoup(cc.text,'html5lib')
			nei_rong1=xiang_qing.find(class_='is-newscontnet')
			# print nei_rong1
			nei_rong2=nei_rong1.text.split('\n')
			klist=[]
			an_hao=""
			an_you=""
			nei_rong=""
			yuan_gao=""
			bei_gao=""
			shang_su_ren=""
			bei_shang_su_ren=""
			dang_shi_ren=""			 		
			for j in range(len(nei_rong2)):
			    if   nei_rong2[j].strip().replace('开庭公告','').replace('开 庭 公 告','').replace('\n','') != '':
			        nei_rong3=nei_rong2[j].strip().replace('开庭公告','').replace('开 庭 公 告','').replace('\n','')
			        klist.append(nei_rong3)
			#         print nei_rong3
	 		              
			kmist = []
			kthird=[]
			cnn=0
			for m in range(len(klist)):
			    aa = klist[m]
			    kmist.append(aa)
			#     print  aa
			    if u'0分' in klist[m]  or u'5分' in klist[m]:
			        cnn+=1
			#         print cnn,aa
			        an_hao=kmist[0]
			        an_you=kmist[1]
			        nei_rong = ' '.join(kmist[2:])
			        sql = "insert into ah_tongling2nd VALUES('%s','%s','%s','%s')" %(an_hao,an_you,nei_rong,updatetime)
			        print p,i,cnn,sql.decode('gbk', 'ignore')
			        kmist = []
			        try:
			            cursor.execute(sql)
			            conn.commit()
			        except:
			            print 'aaaaa'      





