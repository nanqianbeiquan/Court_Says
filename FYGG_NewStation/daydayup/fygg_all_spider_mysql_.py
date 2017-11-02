#!/usr/bin/env python
# -*- coding='utf-8' -*-
import sys
import requests
import selenium
import json
import os
# import pyodbc
import MySQLdb
from bs4 import BeautifulSoup
import threading
import datetime


reload(sys)
sys.setdefaultencoding('utf8')
today = datetime.datetime.now().strftime('%Y-%m-%d')
# target page   http://www.live.chinacourt.org/fygg.shtml
#--server connect ,Database table has established
# cnnt = pyodbc.connect('DRIVER={SQL Server};SERVER=121.42.41.188;DATABASE=CourtNotice;UID=zhangxiaogang;PWD="20p2#NAs}123')
# cursor = cnnt.cursor()

logpath = sys.path[0]+r'\log\fyggo.txt'
# f = open('D:\zhangxig\python_spider\log\\'+datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')+'.txt','w')
f = open(logpath,'a')
req = requests.session()
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"}
def fygg_func(b_n,e_n):
	conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
	cursor=conn.cursor()

	#error count for ValueError:'No JSON object could be decoded'

	err_count = 0

	# start spidering in the range loops
	for n in range(b_n,e_n):
		params={
				"start":n,
				"limit":16,
				"wd":"rmfybulletin",
				"list[0]":"bltntype:"+''
				}
		try:
			r = req.post("http://rmfygg.court.gov.cn/psca/lgnot/solr/searchBulletinInterface.do?callback=?", data=params, headers=headers)
		except Exception as ConnectionError:
			print 'page %s current is not available' %n
			continue


		# ValueError status release try
		try:
			content_dict = json.loads(r.content[2:-1])['objs']
			#print content_dict
			#--break condition!
			if content_dict != []:
				for k in range(len(content_dict)):
				    #print k
					content_fin = json.loads(r.content[2:-1])['objs'][k]#.encode('utf8')
					link_id = content_fin['id']
					crt_name = content_fin['courtcode']
					rel_prn = content_fin['party2']
					pub_date = content_fin['publishdate']
					blt_type = content_fin['bltntypename']
					blt_content = content_fin['content']
					sql = "INSERT INTO bltin188 VALUES ('%s','%s','%s','%s','%s','%s','%s')" %(link_id, crt_name, rel_prn, pub_date, blt_type, blt_content,today)
					# try for if double data
					# print n,k,sql
					try:
						cursor.execute(sql)
						conn.commit()
						f.write('~~'+'NEW'+'~~This is '+str(n)+' page~~'+str(k+1)+' line'+'link'+str(link_id)+"is NEW!"+' Saved '+'~~~~~~~~~~')
						print '~~'+'NEW'+'~~This is '+str(n)+' page~~'+str(k+1)+' line'+'link'+str(link_id)+"is NEW!"+' Saved '+'~~~~~~~~~~'
					except:
						f.write('~~'+'OLD'+'~~This is '+str(n)+' page~~'+str(k+1)+'~~~'+str(link_id)+' already exist'+'~~~~~~')
						print '~~'+'OLD'+'~~This is '+str(n)+' page~~'+str(k+1)+'~~~'+str(link_id)+' already exist'+'~~~~~~~~~'
						continue
					# print k+1,crt_name,rel_prn,pub_date,blt_type,blt_content
					# print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~This is '+ str(n) + ' page~~~~~~~~~~~' +str(k+1)+ '~~~~~~~~~~~~'+str(link_id)+'already exist'+'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
			else:
				f.write('Home Total is '+str(n)+ ' page')
				print 'Home Total is '+str(n)+ ' page'
				continue
		except:
			err_count +=1
			f.write('Error Unexpected times? '+str(err_count))
			print 'Error Unexpected times? '+str(err_count)
			continue
	conn.close()

# tlist = []
# t1 = threading.Thread(target=fygg_func,args=(1,1000))
# tlist.append(t1)
# t2 = threading.Thread(target=fygg_func,args=(1000,2000))
# tlist.append(t2)
# t3 = threading.Thread(target=fygg_func,args=(2000,3000))
# tlist.append(t3)
# t4 = threading.Thread(target=fygg_func,args=(3000,4000))
# tlist.append(t4)
# t5 = threading.Thread(target=fygg_func,args=(4000,5000))
# tlist.append(t5)
# t6 = threading.Thread(target=fygg_func,args=(5000,6000))
# tlist.append(t6)
# t7 = threading.Thread(target=fygg_func,args=(6000,7000))
# tlist.append(t7)
# t8 = threading.Thread(target=fygg_func,args=(7000,8000))
# tlist.append(t8)
# t9 = threading.Thread(target=fygg_func,args=(8000,9000))
# tlist.append(t9)
# t10 = threading.Thread(target=fygg_func,args=(9000,10000))
# tlist.append(t10)
# t11 = threading.Thread(target=fygg_func,args=(10000,11000))
# tlist.append(t11)
# t12 = threading.Thread(target=fygg_func,args=(11000,12000))
# tlist.append(t12)
# t13 = threading.Thread(target=fygg_func,args=(12000,13000))
# tlist.append(t13)
# t14 = threading.Thread(target=fygg_func,args=(13000,14000))
# tlist.append(t14)
# t15 = threading.Thread(target=fygg_func,args=(14000,15000))
# tlist.append(t15)
# t16 = threading.Thread(target=fygg_func,args=(15000,16000))
# tlist.append(t16)
# t17 = threading.Thread(target=fygg_func,args=(16000,17000))
# tlist.append(t17)
# t18 = threading.Thread(target=fygg_func,args=(17000,18000))
# tlist.append(t18)
# t19 = threading.Thread(target=fygg_func,args=(18000,19000))
# tlist.append(t19)
# t20 = threading.Thread(target=fygg_func,args=(19000,20000))
# tlist.append(t20)
# t21 = threading.Thread(target=fygg_func,args=(20000,21000))
# tlist.append(t21)
# t22 = threading.Thread(target=fygg_func,args=(21000,22000))
# tlist.append(t22)
# t23 = threading.Thread(target=fygg_func,args=(22000,23000))
# tlist.append(t23)
# t24 = threading.Thread(target=fygg_func,args=(23000,24000))
# tlist.append(t24)
# t25 = threading.Thread(target=fygg_func,args=(24000,25000))
# tlist.append(t25)
# t26 = threading.Thread(target=fygg_func,args=(25000,26000))
# tlist.append(t26)
# t27 = threading.Thread(target=fygg_func,args=(26000,27000))
# tlist.append(t27)
# t28 = threading.Thread(target=fygg_func,args=(27000,28000))
# tlist.append(t28)
# t29 = threading.Thread(target=fygg_func,args=(28000,29000))
# tlist.append(t29)
# for i in tlist:
# 	i.setDaemon(True)
# 	i.start()
# for i in tlist:
# 	i.join()
fygg_func(1,30)
f.write('Now is %s' %datetime.datetime.now())
print 'Now is %s' %datetime.datetime.now()
f.close()




