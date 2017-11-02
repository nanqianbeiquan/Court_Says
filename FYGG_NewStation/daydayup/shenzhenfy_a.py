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

reload(sys)
sys.setdefaultencoding('utf8')
today = datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='210.16.191.150',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

# param = {
# 'cc':0,
# 'page':1,
# 'pageLimit':10,
# 'caseNo':'',
# 'appliers':'',
# 'sessionDateBegin':'',
# 'sessionDateEnd':'',
# }
cp2 = 0
cp3 = 1
headers = {
'Referer':'http://ssfw.szcourt.gov.cn/frontend/anjiangongkai/session?cc=0',
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
}

# cc0=u'中院',cc2=u'福田',cc1=u'罗湖',cc3=u'南山',cc6=u'盐田',cc4=u'宝安',cc5=u'龙岗',cc7=u'前海'
for s in range(8):
	url = 'http://ssfw.szcourt.gov.cn/frontend/anjiangongkai/session?cc='+str(s)

	r = requests.get(url,headers=headers)
	# r = requests.get(url,data=param)
	# r = requests.post(url,data=param,headers=headers)
	print r.encoding
	# r.encoding = 'gbk'
	rbs = BeautifulSoup(r.text,'html5lib')
	print rbs
	table = rbs.find(id='tbData')
	totalpagetext = rbs.find(class_='page').text
	rule = r'\d+'
	totalpage = re.findall(rule,totalpagetext)[2]

	tr_list = table.find_all('tr')
	# print len(tr_list)
	for i in range(len(tr_list)):
		td_list=tr_list[i].find_all('td')
		kai_ting_ri_qi = td_list[0].text.strip()
		kai_ting_shi_jian = td_list[1].text.strip()
		shen_pan_ting = td_list[2].text.strip()
		an_hao = td_list[3].text.strip()
		an_you = td_list[4].text.strip()
		fa_guan_zhu_li = td_list[5].text.strip()
		dang_shi_ren = td_list[6].text.strip().replace('\n',';').replace(';','').replace(' ','').replace('	','')
		kai_ting_date = kai_ting_ri_qi+' '+kai_ting_shi_jian
		sql = "insert into szcourt VALUE('%s','%s','%s','%s','%s','%s','%s')" %(an_hao,an_you,kai_ting_date,\
			shen_pan_ting,fa_guan_zhu_li,dang_shi_ren,today)
		print s,'1',i,sql
		try:
			cursor.execute(sql)
			conn.commit()
			print 'NEW'
		except:
			print 'OLD'

	dos=0
	for p in range(1,70):
		url1 = 'http://ssfw.szcourt.gov.cn/frontend/anjiangongkai/session?cc='+str(s)+'&page='+str(p)+'&pageLimit=10&caseNo=&appliers=&sessionDateBegin=&sessionDateEnd='
		r = requests.get(url1,headers=headers)
		rbs = BeautifulSoup(r.text,'html5lib')
		if p==int(totalpage)+1:
			print '**********last page %s*********' %p
			break

		# print rbs
		table = rbs.find(id='tbData')
		tr_list = table.find_all('tr')

		print len(tr_list)
		# if len(tr_list)<10:
		# 	dos += 1
		if dos==2:
			if p==7:
				print u'数据获取完成，即将关闭'
				break
			print u'已获取最后一页%s数据,切换城市' %p
			break
		# if p%2==0:
		# 	cp2 = tr_list[-1].find_all('td')[3].text.strip()
		# if p%3==0:
		# 	cp3 = tr_list[-1].find_all('td')[3].text.strip()
		# if cp2==cp3:
		# 	dos=2
		# 	print u'网页%s开始重复，准备跳出' %p
		# 	continue
		for i in range(len(tr_list)):
			td_list=tr_list[i].find_all('td')
			kai_ting_ri_qi = td_list[0].text.strip()
			kai_ting_shi_jian = td_list[1].text.strip()
			shen_pan_ting = td_list[2].text.strip()
			an_hao = td_list[3].text.strip()
			if an_hao=='':
				dos=2
				print 'page %s no more data' %p
				break
			an_you = td_list[4].text.strip()
			fa_guan_zhu_li = td_list[5].text.strip()
			dang_shi_ren = td_list[6].text.strip().replace('\n',';').replace(';','').replace(' ','').replace('	','')
			kai_ting_date = kai_ting_ri_qi+' '+kai_ting_shi_jian
			sql = "insert into szcourt VALUE('%s','%s','%s','%s','%s','%s','%s')" %(an_hao,an_you,kai_ting_date,\
				shen_pan_ting,fa_guan_zhu_li,dang_shi_ren,today)
			print s,p+1,i,sql
			try:
				cursor.execute(sql)
				conn.commit()
				print 'NEW'
			except:
				print 'OLD'
conn.close()
		  