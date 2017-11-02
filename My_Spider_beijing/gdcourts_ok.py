#coding=utf-8
import os
import sys
import requests
import time
from bs4 import BeautifulSoup
import datetime
import MySQLdb
import threading

reload(sys)
sys.setdefaultencoding('utf8')


f = open('D://gdcourts.txt','a')
f.write('starttime:'+time.ctime()+'\n')
print 'starttime:'+time.ctime()
today = datetime.datetime.now().strftime('%Y-%m-%d')
def gdcourts_func(p_start,p_end):
	conn = MySQLdb.connect(host='210.16.191.150',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
	cursor=conn.cursor()

	# url = 'http://www.gdcourts.gov.cn/ecdomain/framework/gdcourt/hnohoambadpabboeljehjhkjkkgjbjie.jsp?gglx=1&ggbt=&countNum=12&endRowNum=12&pageclickednumber=1'
	# urltest = 'http://www.gdcourts.gov.cn/ecdomain/framework/gdcourt/hnohoambadpabboeljehjhkjkkgjbjie.jsp?gglx=1&ggbt=&countNum=12&endRowNum=180120&pageclickednumber=15010'
	# f = open('D://hshfy.txt','a')
	for page in range(p_start,p_end):

		host = 'http://www.gdcourts.gov.cn'
		url = 'http://www.gdcourts.gov.cn/ecdomain/framework/gdcourt/hnohoambadpabboeljehjhkjkkgjbjie.jsp?gglx=1&ggbt=&countNum=12&endRowNum=%s&pageclickednumber=%s'%(page*12,page)
		# url = 'http://www.bjcourt.gov.cn/ktgg/index.htm'
		# url1 = 'http://www.bjcourt.gov.cn/ktgg/index.htm?c=&court=&start=&end=&type=&p=11'
		# url = 'http://www.bjcourt.gov.cn/ktgg/index.htm?c=&court=&start=&end=&type=&p=11'
		r = requests.get(url)
		# r = requests.session()
		# r.get(url1)
		# time.sleep(10)
		# s = r.get(url)
		content = BeautifulSoup(r.text,'html5lib')
		# c_list = content.find('form').table.tbody.tr.td[2].find_all('tr')
		try:
			c_list = content.find('form').find_all('tbody')[6].find_all('tr')
		except:
			print '!!!!!!!!!!!page %s is not temporary loaded!!!!!!!!!!!' %page
			continue
		# print len(c_list)
		if len(c_list)==3:
			print 'OVER PAGE '+time.ctime()+'\n'
			f.write('OVER PAGE '+time.ctime()+'\n')
			continue
		for i in range((len(c_list)-3)/2):
		# print i,c_list[2*i+1]
			td_list = c_list[2*i+1].find_all('td')
			an_ha0 = td_list[0].text.strip()
			# print an_hao
			link_url_proto = td_list[0].find('a').get('href').strip().replace('\n','')
			fa_yuan = td_list[1].text.strip()
			ri_qi = td_list[2].text
			che_xiao = td_list[3].text
			# print 'aaa',link_url
			link_url = ''.join(str(link_url_proto).split())
			content_url = host + link_url
			# print td_list[0]

			# print '2',content_url

			cc = requests.get(content_url)
			# print cc.content
			# time.sleep(0.5)
			ccbs = BeautifulSoup(cc.text,'html5lib')
			cc_table = ccbs.find('table',class_='table_list_B')

			# print 'aaaeg',cc_table
			try:
				cc_tr = cc_table.find_all('tr')
			except:
				print 'detail PAGE is not loaded'
				continue

			an_hao = cc_tr[0].find_all('td')[1].text.strip()
			kai_ting_shi_jian = cc_tr[1].find_all('td')[1].text.strip()
			kai_ting_di_dian = cc_tr[2].find_all('td')[1].text.strip()
			dang_shi_ren = cc_tr[3].find_all('td')[1].text.strip()
			zhu_shen_fa_guan = cc_tr[4].find_all('td')[1].text.strip()
			geng_xin_shi_jian = cc_tr[5].find_all('td')[1].text.strip()
			fa_ting_yong_tu = cc_tr[6].find_all('td')[1].text.strip()
			shi_fou_che_xiao = cc_tr[7].find_all('td')[1].text.strip()
			SQL = u"INSERT INTO gdcourts VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(fa_yuan,an_hao,kai_ting_shi_jian,\
				kai_ting_di_dian,dang_shi_ren,zhu_shen_fa_guan,geng_xin_shi_jian,fa_ting_yong_tu,shi_fou_che_xiao,today)
			# print i+1,SQL
			try:
				cursor.execute(SQL)
				conn.commit()
				print '~~~~PAGE %s the %s anhao %s is NEW \n' %(page,i+1,an_ha0)
				f.write('~~~~PAGE %s the %s anhao %s is NEW \n ' %(page,i+1,an_ha0))
			except:
				print '~~~~PAGE %s the %s anhao %s ALREADY HAVE \n' %(page,i+1,an_ha0)
				f.write('~~~~PAGE %s the %s anhao %s ALREADY HAVE \n' %(page,i+1,an_ha0))
				
	conn.close()

m_list = []
m1 = threading.Thread(target=gdcourts_func,args=(1,1500))
m_list.append(m1)
m2 = threading.Thread(target=gdcourts_func,args=(1500,3000))
m_list.append(m2)
m3 = threading.Thread(target=gdcourts_func,args=(3000,4500))
m_list.append(m3)
m4 = threading.Thread(target=gdcourts_func,args=(4500,6000))
m_list.append(m4)
m5 = threading.Thread(target=gdcourts_func,args=(6000,7500))
m_list.append(m5)
m6 = threading.Thread(target=gdcourts_func,args=(7500,9000))
m_list.append(m6)
m7 = threading.Thread(target=gdcourts_func,args=(9000,10500))
m_list.append(m7)
m8 = threading.Thread(target=gdcourts_func,args=(10500,12000))
m_list.append(m8)
m9 = threading.Thread(target=gdcourts_func,args=(12000,13500))
m_list.append(m9)
m10 = threading.Thread(target=gdcourts_func,args=(13500,15000))
m_list.append(m10)
for m in m_list:
	m.setDaemon(True)
	m.start()
m.join()


print 'endtime:'+time.ctime()+'\n'
f.write('endtime:'+time.ctime()+'\n')
f.close()

# if __name__ == '__main__':
# 	gdcourts_func(2,3)