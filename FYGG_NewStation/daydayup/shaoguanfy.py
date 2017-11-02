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
import urllib
import urllib2
import httplib2
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf8')
today = datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

for p in range(155,161):
	param = {
	'__ASYNCPOST':'false',
	'__EVENTARGUMENT':p,
	'__EVENTTARGET':'ctl00$ContentPlaceHolder1$AspNetPager1',
	'__EVENTVALIDATION':"""/wEWCQKdwsnTAQLJz8u5CAKg39XvCQKg3+nKAgK0w7i7DQKqw7iOAwLS+4TpCwL3uvOGAgK87PLABtKImaN12sjlNGikhpBeP4MI
	3dio""",
	'__VIEWSTATE':"""/wEPDwUJODI1NTczMjYyD2QWAmYPZBYCAgEPZBYCAgEPZBYCAgMPZBYCZg9kFgQCEQ8WAh4LXyFJdGVtQ291bnQCDxYeAgEPZBYCZg8VCQExFTIwMTYtMDMtMDQgMDk6MDA6MDAuMAQ2MTM0KO
	+8iDIwMTXvvInpn7bkuK3ms5XmsJHkuoznu4jlrZfnrKwxOTHlj7co77yIMjAxNe+8iemftuS4reazleawkeS6jOe7iOWtl+esrDE5MeWPtzfooqvkuIror4nkuro66Z
	+25YWz5biC5Lic5Y2X5bel6LS45YWs5Y+444CB5LqR5rWu5biCLi4uBuWNseaZlhLnrKzkuIPlrqHliKTms5Xluq0J5byg5YCN5peXZAICD2QWAmYPFQkBMhUyMDE2LTAzLTAyIDA5OjAwOjAwLjAENjAzMSfvvIgyMDE177yJ6Z
	+25Lit5rOV5rCR5LqM5Yid5a2X56ysMzDlj7cn77yIMjAxNe+8iemftuS4reazleawkeS6jOWIneWtl+esrDMw5Y+3M+WOn+WRij
	rlpKfov57ms5vljY7lu7rkuJrog73mupDmnInpmZDlhazlj7gsIOiiqy4uLgnlj7bph5HljY4S56ys5LiD5a6h5Yik5rOV5bqtCeW8oOWAjeaXl2QCAw9kFgJmDxUJATMVMjAxNi0wMi0yNiAxNTowMDowMC4wBDY2MDQp77yIMjAxNe
	+8iemftuS4reazleawkeS4gOe7iOWtl+esrDEzNTHlj7cp77yIMjAxNe+8iemftuS4reazleawkeS4gOe7iOWtl+esrDEzNTHlj7cx6KKr5LiK6K
	+J5Lq6OumCk+inguWooywg5LiK6K+J5Lq6OumftuWFs+S6v+WIqS4uLgnmnLHlupTpup8S56ys5YWt5a6h5Yik5rOV5bqtCeWwgeaFp
	+aVj2QCBA9kFgJmDxUJATQVMjAxNi0wMi0yNiAwOTozMDowMC4wBDY5OTYn77yIMjAxNe+8iemftuS4reazleWIkeS4gOWIneWtl
	+esrDU55Y+3J++8iDIwMTXvvInpn7bkuK3ms5XliJHkuIDliJ3lrZfnrKw1OeWPtxPooqvlkYrkuro66LWW6aaZ5b63Ceadjumjnua0shXkubPmupDms5XpmaLlhazliKTluq0G5Y
	+26IyCZAIFD2QWAmYPFQkBNRUyMDE2LTAyLTE1IDEwOjMwOjAwLjAENzQ2MRnvvIgyMDE277yJ57KkMDLmiaflvII15Y+3Ge+8iDIwMTbvvInnsqQwMuaJp
	+W8gjXlj7cx5byC6K6u5Lq6OuWImOWFiee6rywg6KKr5byC6K6u5Lq6OumftuWFs+W4guaWsC4uLgbnjovli4cS56ys5LiD5a6h5Yik5rOV5bqtBum
	+meWon2QCBg9kFgJmDxUJATYVMjAxNi0wMi0xNSAwOTowMDowMC4wBDc0NjIZ77yIMjAxNu+8ieeypDAy5omn5byCNuWPtxnvvIgyMDE277yJ57KkMDLmiaflvII25Y
	+3N+W8guiuruS6ujrmlrDkuLDljr/lsI/msLTnlLXokKXlhazlj7jjgIHmlrDkuLDljr/kuLAuLi4G546L5YuHEuesrOS4g+WuoeWIpOazleW6rQbpvpnlqJ9kAgcPZBYCZg8VCQE3FTIwMTYtMDItMDIgMDk6MDA6MDAuMAQ3NDMxGu
	+8iDIwMTbvvInnsqQwMuihjOe7iDEy5Y+3Gu+8iDIwMTbvvInnsqQwMuihjOe7iDEy5Y+3Meiiq+S4iuivieS6ujrlu5bmjqXlqKMsIOS4iuivieS6ujrpn7blhbPluILmraYuLi4G5LiH6Z2WEuesrOWbm
	+WuoeWIpOazleW6rQnmnY7nvr/nm59kAggPZBYCZg8VCQE4FTIwMTYtMDItMDIgMDk6MDA6MDAuMAQ3NDMyGu+8iDIwMTbvvInnsqQwMuihjOe7iDEz5Y
	+3Gu+8iDIwMTbvvInnsqQwMuihjOe7iDEz5Y+3Meiiq+S4iuivieS6ujrmnLHmlrDlprksIOWOn+Wuoeiiq+WRijrpn7blhbPluIIuLi4G5LiH6Z2WEuesrOWbm
	+WuoeWIpOazleW6rQnmnY7nvr/nm59kAgkPZBYCZg8VCQE5FTIwMTYtMDItMDEgMTU6MDA6MDAuMAQ3NDU5Ge+8iDIwMTbvvInnsqQwMuaJp
	+W8gjPlj7cZ77yIMjAxNu+8ieeypDAy5omn5byCM+WPtzPnlLPor7fkuro65aeL5YW05Y6/576O5pmv5oi/5Zyw5Lqn5pyJ6ZmQ5YWs5Y
	+4LCAuLi4J5Y+26YeR5Y2OEuesrOS4g+WuoeWIpOazleW6rQnlvKDlgI3ml5dkAgoPZBYCZg8VCQIxMBUyMDE2LTAyLTAxIDA5OjAwOjAwLjAENjExMyjvvIgyMDE177yJ6Z
	+25Lit5rOV5rCR5LqM57uI5a2X56ysMTcx5Y+3KO+8iDIwMTXvvInpn7bkuK3ms5XmsJHkuoznu4jlrZfnrKwxNzHlj7c36KKr5LiK6K
	+J5Lq6OuS4reWbveW7uuiuvumTtuihjOiCoeS7veaciemZkOWFrOWPuOmfti4uLgnlj7bph5HljY4S56ys5LiD5a6h5Yik5rOV5bqtCeW8oOWAjeaXl2QCCw9kFgJmDxUJAjExFTIwMTYtMDEtMjkgMDk6MDU6MDAuMAQ3NDI4Ge
	+8iDIwMTbvvInnsqQwMuihjOe7iDnlj7cZ77yIMjAxNu+8ieeypDAy6KGM57uIOeWPtzfkuIror4nkuro65rGf6IuP6ZSL5rOw6ZK755
	+z5bel5YW35Yi26YCg5pyJ6ZmQ5YWs5Y+4Li4uCeeEpuaZk+W3jRLnrKzlhavlrqHliKTms5Xluq0J5p2O576/55ufZAIMD2QWAmYPFQkCMTIVMjAxNi0wMS0yOSAwOTowMDowMC4wBDc0MzAa77yIMjAxNu
	+8ieeypDAy6KGM57uIMTHlj7ca77yIMjAxNu+8ieeypDAy6KGM57uIMTHlj7c35LiK6K+J5Lq6OumftuWFs+W4gumftuS/oeS8geS4muWSqOivouacjeWKoeaciemZkOWFrC4uLgbkuIfpnZYS56ys5Zub5a6h5Yik5rOV5bqtCeadjue
	+v+ebn2QCDQ9kFgJmDxUJAjEzFTIwMTYtMDEtMjggMTY6MDA6MDAuMAQ2NjA1Ke+8iDIwMTXvvInpn7bkuK3ms5XmsJHkuIDnu4jlrZfnrKwxMzUy5Y
	+3Ke+8iDIwMTXvvInpn7bkuK3ms5XmsJHkuIDnu4jlrZfnrKwxMzUy5Y+3Meiiq+S4iuivieS6ujrpu4TojILmuIUsIOS4iuivie
	S6ujrpn7blhbPluILmnKwuLi4J5pyx5bqU6bqfEuesrOWFreWuoeWIpOazleW6rQnlsIHmhafmlY9kAg4PZBYCZg8VCQIxNBUyMDE2LTAxLTI4IDA5OjAwOjAwLjAENzQ2MBnvvIgyMDE277yJ57KkMDLmiaflvII05Y
	+3Ge+8iDIwMTbvvInnsqQwMuaJp+W8gjTlj7c15byC6K6u5Lq6OumftuWFs+W4guWVhui0uOi1hOS6p+e7j+iQpeaciemZkOWFrOWPuCwuLi4J5YiY5L
	+K5rOiEuesrOS4g+WuoeWIpOazleW6rQbpvpnlqJ9kAg8PZBYCZg8VCQIxNRUyMDE2LTAxLTI2IDA5OjAwOjAwLjAENjY1NSnvvIgyMDE177yJ6Z
	+25Lit5rOV5rCR5LiA57uI5a2X56ysMTM5OeWPtynvvIgyMDE177yJ6Z+25Lit5rOV5rCR5LiA57uI5a2X56ysMTM5OeWPtzfooqvkuIror4nkuro66Z
	+25YWz5biC5bu66Z+25bel56iL6YCg5Lu35ZKo6K+i5pyJ6ZmQLi4uCemfqeaWh+mUixLnrKzkuInlrqHliKTms5Xluq0J5oi05paw6IuXZAITDw8WAh4LUmVjb3JkY291bnQCjhNkZGT
	+gFFd4/teOWEzjb7zam57Bb1z/w==""",
	}
	url = 'http://www.sgcourts.gov.cn/notice_kt_List.aspx'
	host = 'http://www.sgcourts.gov.cn/'
	# r = requests.post(url,param)
	# print r.content

	# data = urllib.urlencode(param)
	# adr = urllib2.Request(url)
	# a = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	# b = a.open(adr,data).read()
	# print b

	data = urllib.urlencode(param)
	h = httplib2.Http()
	ca,c = h.request(url,'POST',data,headers={'Content-Type': 'application/x-www-form-urlencoded'})
	# print c
	cbs = BeautifulSoup(c.decode('utf-8'),'html5lib')
	table = cbs.find(id='table')
	# print table
	tr_list = table.find_all('tr')
	# print len(tr_list)
	for i in range(1,len(tr_list)):
		td_list = tr_list[i].find_all('td')
		# print len(td_list)
		kai_ting_shi_jian = td_list[1].text.strip().replace('\n','')
		an_hao = td_list[2].text.strip().replace('\n','')
		surl = td_list[2].a['href']
		link = host+surl
		# dang_shi_ren = td_list[3].text.strip().replace('\n','')
		cheng_ban_fa_guan = td_list[4].text.strip().replace('\n','')
		kai_ting_di_dian = td_list[5].text.strip().replace('\n','')
		shu_ji_yuan = td_list[6].text.strip().replace('\n','')
		ma,m = h.request(link,'GET')
		mbs = BeautifulSoup(m.decode('utf-8'),'html5lib')
		# print i,mbs
		tr_lt = mbs.find(id='table').find_all('tr')
		dang_shi_ren = tr_lt[4].find_all('td')[1].text.strip()
		an_you = tr_lt[5].find_all('td')[1].text.strip()

		sql = "insert into shaoguanfy VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" %(an_hao,an_you,dang_shi_ren,kai_ting_shi_jian,\
			kai_ting_di_dian,cheng_ban_fa_guan,shu_ji_yuan,today)
		print p,i,sql
		try:
			cursor.execute(sql)
			conn.commit()
			print 'NEW'
		except:
			print 'OLD'
conn.close()
