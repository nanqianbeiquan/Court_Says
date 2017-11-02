#coding=utf-8
import os
import requests
from bs4 import BeautifulSoup
import re
import sys
import MySQLdb
import threading
import time

reload(sys)
sys.setdefaultencoding('utf-8')


f = open('D://rmfygg.txt','a')
print 'starttime:'+time.ctime()
f.write('starttime:'+time.ctime())
def rmfygg_func(p_start,p_end):
	cnnt = MySQLdb.connect(host='210.16.191.150',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
	cursor = cnnt.cursor()

	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"}

	for page in range(p_start,p_end):
		urls = 'http://rmfygg.court.gov.cn/psca/lgnot/bulletin/page/0_'+str(page)+'.html'
		hosts = 'http://rmfygg.court.gov.cn'
		content_s = requests.get(urls)
		soup = BeautifulSoup(content_s.text,'html5lib')
		# print soup
		targets = soup.find(class_='contentDiv').find_all('tr')
		# f = open('D:\\fygg2.txt','a')
		# print targets
		if len(targets)==1:
			print time.ctime()+' page '+str(page)+'has no DATA'
			break
		else:
			for i in range(1,len(targets)):
				# print i,targets[i]
				tc = targets[i].find_all('td')
				# print len(tc)
				# print tc
				link = tc[0].a['href']
				link_id = re.search(r"\d{5,}", link).group()
				link_nx = re.search(r".{27}",link).group()
				crt_name = tc[1].a.text.strip()
				blt_type = tc[0].a.text.strip()
				rld_prn  = tc[2].a.text.strip()
				pub_date = tc[3].a.text.strip()
				# print i
				# print 'link_id',link_id,type(link_id)
				# print 'link',link,type(link)
				# print 'crt_name',crt_name,type(crt_name)
				# print 'blt_type',blt_type
				# print 'rld_prn',rld_prn
				# print 'pub_date',pub_date

				content_url = hosts+link_nx+'block'+link_id+'.html'

				blt = requests.get(content_url)
				# print pc.text
				blt_bs = BeautifulSoup(blt.text,'html5lib')
				try:
					blt_content = blt_bs.find(class_="ft1424").text.strip().replace('\n',' ')
				except:
					blt_content = ''
				# print [blt_content]
				# print blt_content
				SQL = "INSERT INTO bltin VALUES('%s', '%s', '%s', '%s', '%s', '%s')" %(link_id,crt_name,rld_prn,pub_date,blt_type,blt_content)
				# print SQL
				try:
					cursor.execute(SQL)
					cnnt.commit()
					print '~~~page '+str(page)+' id '+link_id+' does NEW~~~'+'\n'
					f.write('~~~page '+str(page)+' id '+link_id+' does NEW~~~'+'\n')
				except:
					print '~~~page '+str(page)+' id '+link_id+' does EXIST~~~'+'\n'
					f.write('~~~page '+str(page)+' id '+link_id+' does EXIST~~~'+'\n')
	cnnt.close()			

m_list = []
m1 = threading.Thread(target=rmfygg_func,args=(0,5000))
m_list.append(m1)
m2 = threading.Thread(target=rmfygg_func,args=(5000,10000))
m_list.append(m2)
m3 = threading.Thread(target=rmfygg_func,args=(10000,15000))
m_list.append(m3)
m4 = threading.Thread(target=rmfygg_func,args=(15000,20000))
m_list.append(m4)
# m5 = threading.Thread(target=rmfygg_func,args=(20000,25000))
# m_list.append(m5)
for m in m_list:
	m.setDaemon(True)
	m.start()
m.join()
# cnnt.close()
f.close()
print 'endtime:'+time.ctime()