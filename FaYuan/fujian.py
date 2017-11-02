#coding=utf-8
import datetime
import re
import sys

import MySQLdb
import requests
from bs4 import BeautifulSoup

from ShuiWu import MSSQL

reload(sys)
sys.setdefaultencoding('utf8')
today = datetime.datetime.now().strftime('%Y-%m-%d')

# url = 'http://www.fjcourt.gov.cn/page/Public/CourtReport.aspx'
conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()

MSSQL.execute_start('fjcourt')
headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Connection':'keep-alive',
'Host':'www.fjcourt.gov.cn',
'Referer':'http://www.fjcourt.gov.cn/page/public/courtreport.aspx?yikikata=3af66072-a4f2a484f78c529889f6ed88f24485f6',
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'
}
st = "/wEPDwULLTEyNTQ0ODM0NTYPZBYCZg9kFgICAg9kFgRmDxYCHglpbm5lcmh0bWwFODxhIGhyZWY9Jy9Mb2dpbi5hc3B4JyBzdHlsZT0nZGlzcGxheTpub25lJz7or7fnmbvlvZU8L2E\
+ZAICD2QWBAIBDxYCHgtfIUl0ZW1Db3VudAIUFihmD2QWAmYPFQMPMTYwMDAwMDAwOTc0MzA1VOWOn+WRiuWOpumXqOaZr+W3nuS5kOWbreWPkeWxleaciemZkOWFrOWPuOS4juiiq\
+WRiumZiOWboum4v+ehruiupOWQiOWQjOaViOWKm+e6oOe6twoyMDE3LTAxLTAzZAIBD2QWAmYPFQMPMTYwMDAwMDAwODE5MDgzdeWOn\
+WRiumZiOWboum4v+S4juiiq+WRium7hOaZr+WxseOAgeaZr+W3nuaKlei1hOaciemZkOWFrOWPuOOAgeWOpumXqOaZr+W3nuS5kOWbreWPkeWxleaciemZkOWFrOWPuOiCoeadg\
+i9rOiuqee6oOe6twoyMDE3LTAxLTAzZAICD2QWAmYPFQMPMTYwMDAwMDAyNDk2ODk1Y+eUs+ivt+S6uumDkeS8oOmUg+OAgeiiq\
+eUs+ivt+S6uuazieW3nuW4gumTrem8juaKlei1hOWPkeWxleaciemZkOWFrOWPuOWVhuWTgeaIv+mUgOWUruWQiOWQjOe6oOe6t\
woyMDE2LTEyLTI5ZAIDD2QWAmYPFQMPMTYwMDAwMDAxNzE1OTk3vQHnlLPor7fkurrpu4TlvrfkuJzjgIHooqvnlLPor7fkurrogpbmjK\
/mmKXjgIHooqvnlLPor7fkurrogpbmjK/kuq7jgIHooqvnlLPor7fkurrpk4XlsbHljr/lpKnmn7HlsbHmtYbmupDniZvop5LloZjpk4XplIznn7\
/jgIHooqvnlLPor7fkurrogpbmlrnmuIXjgIHooqvnlLPor7fkurrlkLTmlrnpk63lkIjkvJnljY/orq7nuqDnurcKMjAxNi0xMi0yOGQCBA9kFgJmDxUDDzE2MDAwMDAwMjQ3NjYwMnjnlLPor7fkurrnpo\
/lu7rmrKfmsI/lu7rorr7lj5HlsZXmnInpmZDlhazlj7jjgIHooqvnlLPor7fkurrlkajoibPmooXjgIHooqvnlLPor7fkurrpmYjlm73mganllYblk4HmiL\
/plIDllK7lkIjlkIznuqDnurcKMjAxNi0xMi0yOGQCBQ9kFgJmDxUDDzE2MDAwMDAwMjQ1MTcxNYEB5LiK6K+J5Lq65pmL5rGf5LiH6ZGr6I2j57q657uH5YyW57qk5pyJ6ZmQ5YWs5Y\
+45LiO6KKr5LiK6K+J5Lq65YW05Lia6ZO26KGM6IKh5Lu95pyJ6ZmQ5YWs5Y+45pmL5rGf5pSv6KGM6YeR6J6N5YCf5qy+5ZCI5ZCM57qg57q3CjIwMTYtMTItMjdkAgYPZBYCZg8VAw8xNjAwMDAwMDI0NzY2Njhj55Sz6K\
+35Lq65Y+26YeR5pet44CB6KKr55Sz6K+35Lq656aP5bu655yB6YeR54i15oi/5Zyw5Lqn5byA5Y+R5pyJ6ZmQ5YWs5Y+45oi/5bGL56ef6LWB5ZCI5ZCM57qg57q3CjIwMTYtMTItMjdkAgcPZBYCZg8VAw8xNjAwMDAwMDIxNjA2MjmfAeWOn\
+WRiuWuieW+t+mYv+mVhuaciemZkOWFrOWPuO+8iFVOREVSIEFSTU9VUixJTkMuKeS4juiiq+WRiuemj+W7uuecgeW7t+mjnum+meS9k\
+iCsueUqOWTgeaciemZkOWFrOWPuOOAgeWuieW+t+eOm++8iOS4reWbve+8ieaciemZkOWFrOWPuOS+teWus+WVhuagh+adg+e6o\
Oe6twoyMDE2LTEyLTI3ZAIID2QWAmYPFQMPMTYwMDAwMDAxODA4MjgwsQHnlLPor7fkurrojobnlLDluILlhazlhbHkuqTpgJrmn\
InpmZDlhazlj7jjgIHooqvnlLPor7fkurrkuIrmtbfpmLPmt7PnlLXlrZDorr7lpIfmnInpmZDlhazlj7jjgIHnrKzkuInkurrnpo\
/lu7rpobrmgZLlt6XnqIvpgKDku7flkqjor6LmnInpmZDlhazlj7jmi5vmoIfmipXmoIfkubDljZblkIjlkIznuqDnurcKMjAxNi0xMi0yNmQCCQ9kFgJmDxUDDzE2MDAwMDAwMTcxNjAzNYcB55Sz6K\
+35Lq655+z54uu6bmk6am85pyN6aWw5pyJ6ZmQ5YWs5Y+444CB6KKr55Sz6K+35Lq65rOJ5bee5biC5Lic6L+b5pm65Lia5bm/5ZGK5pyJ6ZmQ5YWs5Y\
+444CB5Y6f5a6h6KKr5ZGK5p6X5bu65paw5bm/5ZGK5ZCI5ZCM57qg57q3CjIwMTYtMTItMjNkAgoPZBYCZg8VAw8xNjAwMDAwMDI0MzQ3NThp55Sz6K\
+35Lq656aP5bu655yB5aiB6K+65pWw5o6n5pyJ6ZmQ5YWs5Y+444CB6KKr55Sz6K+35Lq656aP5bu65aSp5bel6ZO45Lia5pyJ6ZmQ5YWs5Y\
+45om/5o+95ZCI5ZCM57qg57q3CjIwMTYtMTItMjJkAgsPZBYCZg8VAw8xNjAwMDAwMDE5MzM0Nzc86KKr5ZGK5Lq65p6X5Z+55LiB6LWw56eB44CB6LSp5Y2W44CB6L\
+Q6L6T44CB5Yi26YCg5q+S5ZOB572qCjIwMTYtMTItMjJkAgwPZBYCZg8VAw8xNjAwMDAwMDI0NzgyMjV755Sz6K+35Lq66I6G55Sw5biC5Yek5Yew55m\
+6LSn5pyJ6ZmQ5YWs5Y+444CB6KKr55Sz6K+35Lq66I6G55Sw5biC5Lit5pmW5oi/5Zyw5Lqn5byA5Y+R5pyJ6ZmQ5YWs5Y+45oi\
/5bGL56ef6LWB5ZCI5ZCM57qg57q3CjIwMTYtMTItMjJkAg0PZBYCZg8VAw8xNjAwMDAwMDI0NzY2NDCQAeeUs+ivt+S6uuiwouaYn\
+a6kOOAgeiiq+eUs+ivt+S6uuazieW3nuW4guaYjua3h+S9k+iCsueUqOWTgeaciemZkOWFrOWPuOOAgeesrOS4ieS6uuazieW3nuW4gua0m\
+axn+WMuuekvuS8muemj+WIqeS4reW/g+aIv+Wxi+enn+i1geWQiOWQjOe6oOe6twoyMDE2LTEyLTIyZAIOD2QWAmYPFQMPMTYwMDAwMDAxODE5MTI2b\
+eUs+ivt+S6uuazieW3nuaYjOebm+a4lOS4muaciemZkOWFrOWPuOOAgeiiq+eUs+ivt+S6uuazieW3nuW4guWfjuW7uuWbveaciei1hOS6p\
+aKlei1hOaciemZkOWFrOWPuOWQiOWQjOe6oOe6twoyMDE2LTEyLTIxZAIPD2QWAmYPFQMPMTYwMDAwMDAyNDc2NjEzV+eUs+ivt\
+S6uum+mueip+eOieOAgeeUs+ivt+S6uuael+WGrOmbqOOAgeiiq+eUs+ivt+S6uuael+a4heaeneaIv+Wxi+S5sOWNluWQiOWQjOe6oOe6twoyMDE2LTEyLTIxZAIQD2QWAmYPFQMPMTYwMDAwMDAxNjY2MTkzhwHnlLPor7fkurrnpo\
/lt57ph5HljZflj7Dlu7rnrZHlt6XnqIvmnInpmZDlhazlj7jjgIHooqvnlLPor7fkurrpl73kvq/ljr/nlLDlm63miL/lnLDkuq\
flvIDlj5HmnInpmZDlhazlj7jlu7rorr7lt6XnqIvmlr3lt6XlkIjlkIznuqDnurcKMjAxNi0xMi0yMGQCEQ9kFgJmDxUDDzE2MDAwMDAwMjQ3NjYxNZMB55Sz6K\
+35Lq65oOg5a6J5Y6/5Yac5p2R5L+h55So5ZCI5L2c6IGU56S+5bSH5q2m5L+h55So56S+44CB6KKr55Sz6K+35Lq65YiY5bCR5Y2O44CB56ys5LiJ5Lq65byg56eA54\
+N44CB56ys5LiJ5Lq65byg5Lic5ZCT5oi/5bGL5Lmw5Y2W5ZCI5ZCM57qg57q3CjIwMTYtMTItMjBkAhIPZBYCZg8VAw8xNjAwMDAwMDE0NTIxNzZv55Sz6K\
+35Lq656aP5bu655yB5bu66Ziz5biC5bCG6b6Z5rC055S15byA5Y+R5pyJ6ZmQ5YWs5Y+444CB6KKr55Sz6K+35Lq65YiY6ZmF5qW35bu66K6\
+5bel56iL5pa95bel5ZCI5ZCM57qg57q3CjIwMTYtMTItMjBkAhMPZBYCZg8VAw8xNjAwMDAwMDE3NzYzNjR+55Sz6K+35Lq65pmL5rGf6aOO5Y2O6Z6L5p2Q5pyJ6ZmQ5YWs5Y\
+444CB6KKr55Sz6K+35Lq65rOJ5bee5Y2P5Yqb5qih5YW35pyJ6ZmQ5YWs5Y+444CB5Y6f5a6h6KKr5ZGK5p6X5a625L+t5Yqg5b\
el5ZCI5ZCM57qg57q3CjIwMTYtMTItMjBkAgMPDxYGHgtSZWNvcmRjb3VudALUKx4IUGFnZVNpemUCFB4QQ3VycmVudFBhZ2VJbmRleAICZGRkP8L09ZOn\
+5Nqxsj+8N9LBD4aH0D/A1ONLs1jv8/0lgc="
st = st.replace('\n','')
req = requests.session()
for p in range(1,20):
	param = {
		'__EVENTARGUMENT':p,
		'__EVENTTARGET':'ctl00$cplContent$AspNetPager1',
		'__VIEWSTATE':st,
	}
	# url = 'http://www.fjcourt.gov.cn/page/Public/CourtReport.aspx?yikikata=3af66072-b98e0bd5432dc987f00a1de5a7f1083a'
	url = 'http://www.fjcourt.gov.cn/page/public/courtreport.aspx?yikikata=3af66072-a4f2a484f78c529889f6ed88f24485f6'
	host = 'http://www.fjcourt.gov.cn'
	r = req.post(url=url,data=param,headers=headers)
	rbs = BeautifulSoup(r.text,'html5lib')
	# print rbs
	rli = rbs.find(class_='module-case-items')
	# print rli
	li_list = rli.find_all('li')
	for i in range(len(li_list)):
		ech = li_list[i].a
		linp = ech['href']
		link = host + linp
		link_id = re.search(r'\d{8,}',link).group()
		link_text = li_list[i].text.strip()
		# print i,link_id,li_list[i].text,link
		try:
			r1 = requests.get(link)
		except:
			print 'requests.exceptions.ConnectionError'
			continue
		r1bs = BeautifulSoup(r1.text,'html5lib')
		cc = r1bs.find(class_='article-content')
		try:
			ct = cc.find_all('p')[0].text.strip()
		except:
			ct = cc.text.strip()
		try:
			cp = cc.find_all('p')[2].text.strip()
		except:
			cp = ''
		# print i,link_id,ct,cp
		sql = "insert into fjcourt values('%s','%s','%s','%s','%s')" %(link_id,link_text,ct,cp,today)
		print p,i,sql
		try:
			cursor.execute(sql)
			conn.commit()
			print 'NEW'
		except:
			print 'OLD'
MSSQL.execute_sop('fjcourt')
conn.close()
