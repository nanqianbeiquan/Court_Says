#coding=utf-8
import os
import sys
import re
import requests
import time
from bs4 import BeautifulSoup
import datetime
import MySQLdb
import threading
import PyV8

reload(sys)
sys.setdefaultencoding('utf8')
# url = 'http://www.gdcourts.gov.cn/ecdomain/framework/gdcourt/hnohoambadpabboeljehjhkjkkgjbjie.jsp'
filepath = sys.path[0]+r'\log\hshfy.txt'
f = open(filepath,'a')
print 'starttime:'+time.ctime()
f.write('starttime:'+time.ctime())
# a = datetime.datetime.now().strftime('%Y-%m-%d')
a = (datetime.date.today()+datetime.timedelta(-15)).strftime('%Y-%m-%d')
b = (datetime.date.today()+datetime.timedelta(+15)).strftime('%Y-%m-%d')
print a,b
today = datetime.datetime.now().strftime('%Y-%m-%d')
req = requests.session()
class ShangHaiFygg(object):

	def get_yzm(self):
		headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Host':'www.hshfy.sh.cn',
		# 'Referer':'http://www.hshfy.sh.cn/shfy/gweb/ktgg_search.jsp?jdfwkey=4olbd2',
		'Content-Type': 'application/x-www-form-urlencoded',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36'
		} 	
		r = req.get(url='http://www.hshfy.sh.cn/shfy/gweb/ktgg_search.jsp?',headers=headers)
		r.encoding = 'gbk'
		# print r.headers,r.text
		if u'您的浏览器需要支持JavaScript' in r.text:
			print u'手动解析JavaScript'
			soup = BeautifulSoup(r.text, 'lxml')
			script = soup.select('script')[0].text
			# script = script[len('eval(')+1:-1]
			print 'script', script
			# script = script.replace("""eval("cb=eval;cb(bb);");""","""return ea+"search.jsp?jdfwkey=h"+fa;eval("cb=eval;cb(bb);""")
			ctxt = PyV8.JSContext()
			ctxt.enter()
			res = ctxt.eval(script)
			print 'js_after', res
		bs = BeautifulSoup(r.text,'html5lib')
		print bs.text.encode('gbk','ignore')
		rule = r'(?<=yzm=").*(?=")'
		yzm = re.search(rule,bs.text).group()
		# yzm = 'UDRT'
		print 'yzm:', yzm
		return yzm

	def hshfy_func(self,n_start,n_end):
		time.sleep(2)
		cnt = 0
		combo = 0
		# yzm = self.get_yzm()
		while 1:
			try:
				# yzm = self.get_yzm()
				yzm = 'yKHz'
				break
			except:
				print u'验证码获取失败，暂停10秒',time.ctime()
				time.sleep(10)
				combo += 1
				if combo == 10:
					print u'网站暂时失效，更新取消', time.ctime()
					sys.exit()
		conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
		cursor=conn.cursor()

		headers = {
		'Referer':'http://www.hshfy.sh.cn/shfy/gweb/ktgg_search.jsp?jdfwkey=4olb62',
		'Content-Type': 'application/x-www-form-urlencoded',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36'
		} 
		for n in range(n_start,n_end):
			time.sleep(3)
			param = {
				'ah':'',
				'bg':'',
				'ft':'',
				'ktrqjs':b,
				'ktrqks':a,
				'pagesnum':n,
				'spc':'',
				'yg':'',
				'yzm':yzm,
					}
			url = 'http://www.hshfy.sh.cn/shfy/gweb/ktgg_search_content.jsp?jdfwkey=4olb62'
			# url = 'http://www.hshfy.sh.cn/shfy/gweb/count_all.jsp?pa=acGFnZT1HRyZwYXJhbT1LVFhYz?'
			# url = 'http://www.hshfy.sh.cn/shfy/gweb/ktgg_search.jsp?jdfwkey=v7vvo2'
			# url = 'http://www.bjcourt.gov.cn/ktgg/index.htm'
			# url = 'http://www.bjcourt.gov.cn/ktgg/index.htm?c=&court=&start=&end=&type=&p=10000'
			# var url = "yzm="+yzm+"&ft="+h_ft+"&ktrqks="+h_ktrqks+"&ktrqjs="+h_ktrqjs+"&spc="+h_spc+"&yg="+h_yg+"&bg="+h_bg+"&ah="+h_ah+"&pagesnum="+pageNum
			try:
				r = req.post(url,data = param,headers=headers,timeout=20)
			except Exception as ConnectionError:
				print 'page:'+str(n)+'ConnectionError,Go To Next Page'
				continue
			# r = requests.get(url,headers=headers)
			# r.encoding = 'gbk'
			# print r.content,'\n',r.headers,'\n',r.status_code,r.encoding,type(r)

			soup = BeautifulSoup(r.text,'html5lib')
			# print soup
			if n == 500:
				cif = soup.find(class_='meneame')
				page_txt = cif.find('strong').text
				page_out = int(int(page_txt)/15)+2
				# print page_out
				# break
			# print n,page_out
			if n == page_out:
				print u'到达最后一页%s附近' %n
				break
			tr_list = soup.find_all('tr')
			# print tr_list[-2],len(tr_list)
			if len(tr_list)<6:
				cnt += 1
				print 'page %d does not exist' %n
				f.write('page %d does not exist' %n)
				if cnt == 50:
					print 'no more page'
					print soup
					break
				# break
				continue
			# print u'带*为普通案件'
			for i in range(len(tr_list)-4):
				# print i,tr_list[i+4]

				td_list = tr_list[i+4].find_all('td')
			# for j in range(len(td_list)):
				# print j,td_list[j]
				fa_yuan = td_list[0].text.strip()
				fa_ting = td_list[1].text.strip()
				kai_ting_ri_qi = td_list[2].text.strip()
				an_hao = td_list[3].text.strip()
				an_you = td_list[4].text.strip()
				cheng_ban_bu_men = td_list[5].text.strip()
				shen_pan_zhang = td_list[6].text.strip()
				yuan_gao = td_list[7].text.strip()
				bei_gao = td_list[8].text.strip()

				sql = u"insert into hshfy VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')" %(fa_yuan,fa_ting,kai_ting_ri_qi,an_hao,an_you,cheng_ban_bu_men,shen_pan_zhang,yuan_gao,bei_gao,today)
				# print n,i,sql
				try:
					cursor.execute(sql)
					conn.commit()
					print '~~page %d de %d TIS %s NEW FOO ~~\n' %(n,i,an_hao)
					f.write('~~page %d de %d TIS %s NEW FOO ~~\n' %(n,i,an_hao))
				except:
					print '~~page %d de %d ALREADY HAVE data %s ~~\n' %(n,i,an_hao)
					f.write('~~page %d de %d ALREADY HAVE data %s ~~\n' %(n,i,an_hao))

		conn.close()

# get_yzm()
if __name__ == '__main__':
	fy = ShangHaiFygg()
	# fy.get_yzm()
	fy.hshfy_func(500,1500)
#m_list = []
#for s in range(1,(2000/100)+1):
#	if s == 1:
#		m1 = threading.Thread(target=hshfy_func,args=(1,100))
#	else:
#		m1 = threading.Thread(target=hshfy_func,args=((s-1)*100,s*100))
#	m_list.append(m1)
# m1 = threading.Thread(target=hshfy_func,args=(1,2000))
# m_list.append(m1)
# m2 = threading.Thread(target=hshfy_func,args=(260,520))
# m_list.append(m2)
# m3 = threading.Thread(target=hshfy_func,args=(520,780))
# m_list.append(m3)
# m4 = threading.Thread(target=hshfy_func,args=(780,1040))
# m_list.append(m4)
# m5 = threading.Thread(target=hshfy_func,args=(1040,1300))
# m_list.append(m5)
#for m in m_list:
#	m.setDaemon(True)
#	m.start()
#for m in m_list:
#        m.join()
# cnnt.close()
print 'endtime:'+time.ctime()
f.write('endtime:'+time.ctime()+'\n')
f.close()
