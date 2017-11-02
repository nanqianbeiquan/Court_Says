#coding=utf-8
import datetime
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

from ShuiWu import MSSQL

print datetime.datetime.now().strftime('%Y-%m-%d')
# print str(datetime.datetime.now())[0:10]
reload(sys)
sys.setdefaultencoding('utf8')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')
shi_qu=u'揭阳市'
MSSQL.execute_start('gd_jieyang')
url = "http://www.gdjyfy.cn/Article/Article.aspx?CategoryId=17"
host='http://www.gdjyfy.cn'
for i in range(5):
	try:
		r = requests.get(url)
		if 'id="article"'in r.text:
			break
	except:
		continue
soup=BeautifulSoup(r.text,'html5lib')
print r.text
href_list = soup.find(id='article').find('div', class_='lists').find_all(class_='list')
for href in href_list:
	link_url = href.find('a').get('href')
	i_d=re.search(r'\d{3,}',link_url).group()
	link=host+link_url
	# print link
	xiang_qing=requests.get(link)
	xiang_qing.encoding = 'utf8'
	xiang=BeautifulSoup(xiang_qing.text,'html5lib')
	nei_rong=xiang.find(class_="con article-place")
	td_list=nei_rong.find_all('p')
	tdlen=len(td_list)
	# print tdlen
	fir = []
	for i in range(tdlen):
		td = td_list[i].text.strip()
		if td!='':
			fir.append(td)
	# print len(fir)
	sec=[]
	cnn = 0
	for n in range(len(fir)):
		# cnn += 1
		nr1 = fir[n]
		sec.append(nr1)
		# print 'sec',sec
		if u'书记员' in fir[n]:
			cnn+=1
			try:
				an_hao = sec[0]
				an_you = sec[1]
				nei_rong = ' '.join(sec[2:])
			except:
				an_hao = sec[0].split(u'案由')[0]
				an_you = u'案由'+sec[0].split(u'案由')[1].split(u'当事人')[0]
				nei_rong = u'当事人'+sec[0].split(u'当事人',1)[1]
			sql = "insert into gd_jieyang VALUES('%s','%s','%s','%s','%s','%s')" %(i_d,an_hao,an_you,nei_rong,updatetime,shi_qu)
			print cnn, sql
			# print cnn,sql.encode('gbk', 'ignore')
			sec=[]
			MSSQL.execute_insert(sql)
	time.sleep(1)
MSSQL.execute_sop('gd_jieyang')






