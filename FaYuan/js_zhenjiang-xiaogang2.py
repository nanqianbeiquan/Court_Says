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

conn = MySQLdb.connect(host='210.16.191.150',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

# host='http://www.jsczfy.gov.cn/ktgg/'
# soup = BeautifulSoup(r.text,'html5lib')
# print soup.prettify()

shi_qu=u'镇江市'
# href_list= "http://www.zjzy.gov.cn/col79/articleinfo.php?infoid=13041"
url = 'http://www.zjzy.gov.cn/col79/articlecolumn.php?colid=79'
# param = {
# 	'colid':79,
# 	'currpage':n,
# }
r = requests.get(url)
r.encoding='GBK'
rbs = BeautifulSoup(r.text,'html5lib')
bs = rbs.find_all('table')
# for i in range(len(bs)):
# 	if len(bs[i].find_all('tr'))>12:
# 		print '******',i,'*****',bs[i].find_all('tr')[1]
# print 'error'
tr_list = bs[21].find_all('tr')
for i in range(1,len(tr_list)-3):
	# if i == 3:
		link = tr_list[i].find_all('td')[2].a['href']
		# print '***************',i,link
		# if i == 1:
		r2 = requests.get(link)
		r2.encoding='GBK'
		r2bs = BeautifulSoup(r2.text,'html5lib')
		cc = r2bs.find(class_='x_content').text.split('\n')
		klist=[]
		for j in range(len(cc)):
			if cc[j].strip().replace('\n','') != '':
				sh = cc[j].strip().replace('\n','')
				klist.append(sh)
				# print j,cc[j] 
		print len(klist)
		kmist = []
		cnn = 0
		for m in range(len(klist)):
			# print u'第'+str(i)+u'行',m,klist[m]
			# continue
			aa = klist[m]
			kmist.append(aa)
			if u'时　间：' in klist[m]:
				# print 'miao',m,klist[m]
				cnn+=1
				an_hao = kmist[0]
				an_you = kmist[1]
				contxt = ' '.join(kmist[2:])
				sql = "insert into js_zhenjiang VALUES('%s','%s','%s','%s')" %(an_hao,an_you,contxt,updatetime)
				print i,cnn,sql
				kmist = []       




				

		    
		



# #正式内容	
# # for ss in range(len(soup.find_all("td",width="630"))):
# # # 
# # 	link_url=soup.find_all("td",width="630")[ss].a['href']
# # 	id=re.search(r'\d{5,}',link_url).group()
# # # 	print ss,id 
# # 
# # 	content_url=host+id+'.shtml'
# # # 	print ss,content_url
# # 	cc= requests.get(content_url)
# # # 	ccbs=BeautifulSoup(cc.text,'html5lib')
# #     print cc.content
# # 	neirong=ccbs.title.text.strip()
# # 	print ss,id,neirong,updatetime
# # 		sql = "INSERT INTO sd_gaoyuan VALUES('%s','%s','%s')" %(id,neirong,updatetime)



# # 		print sql+";"
# # 		cursor.execute
# #         cursor.execute(sql)
# #         conn.commit()



