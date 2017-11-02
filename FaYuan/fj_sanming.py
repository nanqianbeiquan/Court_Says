#coding=utf-8
import datetime
import re
import sys

import MySQLdb
import requests
from bs4 import BeautifulSoup

from ShuiWu import MSSQL

print datetime.datetime.now().strftime('%Y-%m-%d')
# print str(datetime.datetime.now())[0:10]
reload(sys)
sys.setdefaultencoding('utf8')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')

shi_qu=u'三明市'
conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()
MSSQL.execute_start('fj_sanming')
url = 'http://www.smzjfy.com/spgk/fygg/ktgg/'
host='http://www.smzjfy.com'
headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Connection':'keep-alive',
'Host':'www.smzjfy.com',
'Referer':'http://www.smzjfy.com/spgk/fygg/ktgg/',
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
}

for g in range (1,10):
	param = {
		'flagshowlst	':'',
		'groupid':'',
		'hcontent':'',
		'intra':'',
		'showby':'',
		'strbody':'',
		'strmemo':'',
		'topage':g,
		}
	r=requests.get(url,data=param,headers=headers)
# 	print r.encoding
	r.encoding = 'gbk'
	zhu_ye = BeautifulSoup(r.text,'html5lib')
# 	print zhu_ye
	link_list=zhu_ye.find_all(class_='inforow')
	linklen=len(link_list) 
 
	for i in range(linklen):
		link_url=link_list[i].a['href']
		link_text=link_list[i].a['title']
		i_d=re.search(r'\d{3,}',link_url).group()
		nei_rong=link_text.strip().replace('\n','').replace(' ','').replace('  ','')
# 		nei_rong=link_list[i].text.strip().replace('\n','').replace(' ','').replace('  ','')
# 		if u'本院'  in link_text or u'法院'  in link_text:			
# 			i_d=re.search(r'\d{3,}',link_url).group()
# 			print i_d,link_text
		sql = "INSERT INTO fj_sanming VALUES('%s','%s','%s','%s')" %(i_d,nei_rong,updatetime,shi_qu)
		# print g,i,sql.encode('gbk','ignore')
		print g,i,sql
		try:
			cursor.execute(sql)
			conn.commit()
		except:
			print 'aaaaa'
MSSQL.execute_sop('fj_sanming')