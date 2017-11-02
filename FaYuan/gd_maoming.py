#coding=utf-8
import datetime
import sys
import time

import MySQLdb
from selenium import webdriver

from ShuiWu import MSSQL

print datetime.datetime.now().strftime('%Y-%m-%d')
# print str(datetime.datetime.now())[0:10]
reload(sys)
sys.setdefaultencoding('utf8')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')
shi_qu='茂名市'

conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()
MSSQL.execute_start('gd_maoming')
# driver=webdriver.Firefox()
# driver.get('http://sfgk.mmcourts.gov.cn:8000/fm/ktmore.aspx')
url = 'http://sfgk.mmcourts.gov.cn:8000/fm/ktmore.aspx'
browser=webdriver.PhantomJS()
browser.get(url)
source=browser.find_element_by_xpath(".//*[@id='GridView1']")
# html=source.get_attribute('outerHTML')
# Soup = BeautifulSoup(html,'html.parser')
tr_element_list = source.find_elements_by_xpath('tbody/tr')
for tr_element in tr_element_list[1:]:
	td_element_list = tr_element.find_elements_by_xpath('td')
	for td in td_element_list :
		an_hao=td_element_list[0].text.strip()
		an_you=td_element_list[1].text.strip()
		ri_qi=td_element_list[2].text.strip()
		fa_ting=td_element_list[3].text.strip()
		zhu_shen=td_element_list[4].text.strip()
		shu_ji_yuan=td_element_list[5].text.strip()
		cheng_ban_ting=td_element_list[6].text.strip()
# 	print '1',an_hao,an_you,ri_qi,fa_ting,zhu_shen,shu_ji_yuan,cheng_ban_ting
	sql = "INSERT INTO gd_maoming VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(an_hao,an_you,ri_qi,fa_ting,zhu_shen,shu_ji_yuan,cheng_ban_ting,updatetime,shi_qu)
	print 1,sql+";"
	try:
		cursor.execute(sql)
		conn.commit()
	except:
		print 'aaaaa'	
for p in range(1,10):	
	next_botton=browser.find_element_by_id('divepage_Next')
	next_botton.click()
	time.sleep(2)
	source=browser.find_element_by_xpath(".//*[@id='GridView1']")
	tr_element_list = source.find_elements_by_xpath('tbody/tr')
	for tr_element in tr_element_list[1:]:
		td_element_list = tr_element.find_elements_by_xpath('td')
		for td in td_element_list :
			an_hao=td_element_list[0].text.strip()
			an_you=td_element_list[1].text.strip()
			ri_qi=td_element_list[2].text.strip()
			fa_ting=td_element_list[3].text.strip()
			zhu_shen=td_element_list[4].text.strip()
			shu_ji_yuan=td_element_list[5].text.strip()
			cheng_ban_ting=td_element_list[6].text.strip()
# 		print p+1,an_hao,an_you,ri_qi,fa_ting,zhu_shen,shu_ji_yuan,cheng_ban_ting
		sql = "INSERT INTO gd_maoming VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(an_hao,an_you,ri_qi,fa_ting,zhu_shen,shu_ji_yuan,cheng_ban_ting,updatetime,shi_qu)
		print p+1,sql+";"
		try:
			cursor.execute(sql)
			conn.commit()
		except:
			print 'aaaaa'		
MSSQL.execute_sop('gd_maoming')

