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
mars = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
cont=0
url = 'http://www.szzjrmfy.gov.cn/articles/20140725132949.php'
r = requests.get(url)
print 'aaa',r.encoding
# r.encoding = 'ISO-8859-1'
r.encoding = 'gb2312'
rbs = BeautifulSoup(r.text,'html5lib')
ps = rbs.find_all('p')
for i in range(len(ps)):
	# if i == 97:
		# print 'sts%s' %i,ps[i].text.split(),type(ps[i].text)
		c = ps[i].text.split('\n\n')
		for j in range(len(c)):
			# if j == 4:
			# print j,c[j].split('\n'),type(c[j])
			das = []
			mm = c[j].split('\n')
			for l in range(len(mm)):
				# if l==0:
				# print l,mm[l],type(mm[l])
				la = mm[l].split('：')
				# print la[0],len(la),la[1]
				
				if la[0]==u'案　号':
					das.append('0')
					an_hao=la[1]
					print '****anhao****',an_hao

				elif la[0]==u'案　由':
					das.append('1')
					an_you=la[1]
					print 'anyou',an_you
				elif la[0]==u'当事人':
					das.append('2')
					dang_shi_ren=la[1]
					print '***dangshiren***',dang_shi_ren
				elif la[0]==u'审判长':
					das.append('3')
					shen_pan_zhang = la[1]
					print 'shenpanzhang',shen_pan_zhang
				elif la[0]==u'合议庭':
					das.append('4')
					he_yi_ting = la[1]
					print 'heyiting',he_yi_ting
				elif la[0]==u'地　点':
					das.append('5')
					di_dian = la[1]
					print 'place',di_dian
				elif la[0]==u'日　期':
					das.append('6')
					ri_qi = la[1]
					print 'date',ri_qi
				elif la[0]==u'时　间':
					das.append('7')
					shi_jian=la[1]
					print 'time',shi_jian
				elif la[0]==u'书记员':
					das.append('8')
					shu_ji_yuan=la[1]
					print 'shujiyuan',shu_ji_yuan
				else:
					print 'boom'
			# print das
			con = [i for i in mars if i not in das]
			for cm in con:
				if cm=='0':
					an_hao=''
				elif cm=='1':
					an_you=''
				elif cm=='2':
					dang_shi_ren=''
				elif cm=='3':
					shen_pan_zhang=''
				elif cm=='4':
					he_yi_ting=''
				elif cm=='5':
					di_dian=''
				elif cm=='6':
					ri_qi=''
				elif cm=='7':
					shi_jian=''
				elif cm=='8':
					shu_ji_yuan=''
				else:
					print "what's this:",cm
			if an_hao=='':
				continue
			sql = "INSERT INTO szfy VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(an_hao,an_you,dang_shi_ren,\
				shen_pan_zhang,he_yi_ting,di_dian,ri_qi,shi_jian,shu_ji_yuan,today)
			cont = cont+1
			print i,j,sql,'miao',cont

# 案　号：(2016)苏05民终4630号
# 案　由：劳动争议纠纷
# 当事人：上诉人:昆山晟达峰精密五金有限公司;被上诉人:卜训娥
# 审判长：包刚
# 合议庭：包刚
# 地　点：6238法庭
# 日　期：2016年6月6日
# 时　间：9时30分
# 书记员：韩颖