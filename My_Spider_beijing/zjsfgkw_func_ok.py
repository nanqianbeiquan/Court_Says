#coding=utf-8
import os
import sys
import requests
import time
from bs4 import BeautifulSoup
import datetime
import MySQLdb
import threading
import json

reload(sys)
sys.setdefaultencoding('utf8')

f = open(r'D://zjsfgkw.txt','a')
print 'starttime:'+time.ctime()
f.write('starttime:'+time.ctime())
today = datetime.datetime.now().strftime('%Y-%m-%d')
# print today,type(today)
# hosts = 'http://www.zjsfgkw.cn'
# url = 'http://www.zjsfgkw.cn/Notice/NoticeKTList'

def zjsfgkw_func(n_start,n_end):
	url = 'http://www.zjsfgkw.cn/Notice/NoticeKTSearch'

	conn = MySQLdb.connect(host='210.16.191.150',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
	cursor=conn.cursor()

	headers = {
			'Host':'www.zjsfgkw.cn',
			'Cookie':'_gscu_274171321=6468497012k3g087; Hm_lvt_c4cb5f597b36c5db42909a369cbaab8e=1464684971,1464745298; _gscbrs_274171321\
	=1; Hm_lpvt_c4cb5f597b36c5db42909a369cbaab8e=1464745670',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}
	for n in range(n_start,n_end):
		param = {
		        'pageno': n,
		        'pagesize': 10,
		        'cbfy': '',
		        'yg': '',
		        'bg': '',
		        'spz':'',
		        'jarq1': '',
		        'jarq2': ''
				}

		r = requests.post(url,data=param,headers=headers)
		# print r.content,type(r.content)
		try:
			r_dict = json.loads(r.content)['list']
			# print r_dict,type(r_dict)
			# print 'aaa'
		except:
			print 'PAGE %s LOADS FAILED' %n
			f.write('PAGE %s LOADS FAILED \n' %n)
			continue
		if len(r_dict)==0:
			print '%s OVER PAGE '%n
			f.write('%s OVER PAGE \n'%n)
			continue
		for i in range(len(r_dict)):
			content = r_dict[i]
			CBBM = content['CBBM'].strip()
			SPZ = content['SPZ'].strip()
			BG = content['BG'].strip()
			FT = content['FT'].strip()
			PQRQ = content['PQRQ'].strip().replace('\n','')
			FY = content['FY'].strip()
			YG = content['YG'].strip()
			KTRQ = content['KTRQ'].strip()
			AH = content['AH'].strip()
			AY = content['AY'].strip()
			# print FY,FT,KTRQ,PQRQ,AH,AY,CBBM,SPZ,YG,BG
			sql = "insert into zjsfgkw VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(FY,FT,KTRQ,PQRQ,AH,AY,CBBM,SPZ,YG,BG,today)
			print i,sql,'\n'
			try:
				cursor.execute(sql)
				conn.commit()
				print 'PAGE %s LINE %s DATA GETS NEW' %(n,i+1)
				f.write('PAGE %s LINE %s DATA GETS NEW \n' %(n,i+1))
			except:
				print 'PAGE %s LINE %s DATA ALREAD EXIST' %(n,i+1)
				f.write('PAGE %s LINE %s DATA ALREAD EXIST \n' %(n,i+1))
	conn.close()

m_list = []
m1 = threading.Thread(target=zjsfgkw_func,args=(1,150))
m_list.append(m1)
m2 = threading.Thread(target=zjsfgkw_func,args=(150,300))
m_list.append(m2)
m3 = threading.Thread(target=zjsfgkw_func,args=(300,450))
m_list.append(m3)
m4 = threading.Thread(target=zjsfgkw_func,args=(450,600))
m_list.append(m4)
m5 = threading.Thread(target=zjsfgkw_func,args=(600,750))
m_list.append(m5)
m6 = threading.Thread(target=zjsfgkw_func,args=(750,900))
m_list.append(m6)
m7 = threading.Thread(target=zjsfgkw_func,args=(900,1050))
m_list.append(m7)
m8 = threading.Thread(target=zjsfgkw_func,args=(1050,1200))
m_list.append(m8)
m9 = threading.Thread(target=zjsfgkw_func,args=(1200,1350))
m_list.append(m9)
m10 = threading.Thread(target=zjsfgkw_func,args=(1350,1500))
m_list.append(m10)
for m in m_list:
	m.setDaemon(True)
	m.start()
m.join()


print 'endtime:'+time.ctime()+'\n'
f.write('endtime:'+time.ctime()+'\n')
f.close()


# if __name__ == '__main__':
# 	zjsfgkw_func(1,8)