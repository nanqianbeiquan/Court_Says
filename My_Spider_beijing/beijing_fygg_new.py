#coding=utf-8
import os
import sys
import requests
import time
import hashlib
from bs4 import BeautifulSoup
import datetime
import MySQLdb
import threading
import re
from selenium import webdriver
import subprocess
from PIL import Image
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
# from selenium import NoSuchElementException

reload(sys)
sys.setdefaultencoding('utf8')
screenshot_offset_x = 0
screenshot_offset_y = 0

today = datetime.datetime.now().strftime('%Y-%m-%d')

# plugin_path = os.path.join(sys.path[0], r'\bjfy\bjfygg.bat')
ocr_path = sys.path[0]+r'\bjfy\bjfygg.bat'
filepath = sys.path[0]+r'\log\bjfy.txt'
imgpath = sys.path[0]+r'\log\bjyzm.jpg'
# print 'ocr:'+ocr_path
yzm_url = 'http://www.bjcourt.gov.cn/yzm.jpg'
check_sure = 'http://www.bjcourt.gov.cn/cpws/checkkaptcha.htm'
host = 'http://www.bjcourt.gov.cn'
go = False
ngo = True
ni = 1
try_times = 10
err_num = 0
dup = 0
print 'pid:', os.getpid()

key1 = {'app_key': '170284467',
        'secret': 'a9162d3d1fbb984f99564a29a469ada8',
        'host': '123.57.11.143',
        'port': '8123',
        'concurrent_num': 100,
        'lock_num': 20
        }
key2 = {'app_key': '151075879',
        'secret': '32ebc7fc46978aeafd5d9c012fa9a037',
        'host': '123.56.242.140',
        'port': '8123',
        'concurrent_num': 10,
        'lock_num': 1
        }
key3 = {'app_key': '137896159',
        'secret': '648a0531abc57e0fd395cefae9961089',
        'host': '123.56.232.139',
        'port': '8123',
        'concurrent_num': 20,
        'lock_num': 0
        }
key4 = {'app_key': '60719893',
        'secret': '23aaf8a59bb7b3188333cc44ee3d53e1',
        'host': '123.56.139.108',
        'port': '8123',
        'concurrent_num': 5,
        'lock_num': 0
        }


class ProxyConf(object):

	def __init__(self, key):
		self.app_key = key['app_key']
		self.secret = key['secret']
		self.host = key['host']
		self.port = key['port']
		self.concurrent_num = key['concurrent_num']
		self.lock_num = key['lock_num']

	def get_proxy(self):
		return {'http': '%s:%s' % (self.host, self.port), 'https': '%s:%s' % (self.host, self.port)}

	def get_auth_header(self, lock_id='0', release_id='0'):
		param_map = {
			"app_key": self.app_key,
			"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),  # 如果你的程序在国外，请进行时区处理
			"retrypost": "true"
			#  ,"with-transaction": '1'
		}
		if lock_id != '0':
			param_map['with-transaction'] = lock_id
		if release_id != '0':
			param_map['release-transaction'] = release_id
		# 排序
		keys = param_map.keys()
		keys.sort()
		codes = "%s%s%s" % (self.secret, str().join('%s%s' % (key, param_map[key]) for key in keys), self.secret)
		# 计算签名
		sign = hashlib.md5(codes).hexdigest().upper()
		param_map["sign"] = sign

		# 拼装请求头Proxy-Authorization的值
		keys = param_map.keys()
		auth_header = "MYH-AUTH-MD5 " + str('&').join('%s=%s' % (key, param_map[key]) for key in keys)
		return auth_header

	# def get_lock_id(self):
	#     return random.randint(1, self.lock_num)

	def get_lock_id(self):
		lock_id = get_lock_id(self.app_key)
		if lock_id != '0':
			return lock_id
		else:
			print u'没有可用lock_id,休眠3秒后重试...'
			time.sleep(3)
			return self.get_lock_id()

	def release_lock_id(self, lock_id):
		release_lock_id(self.app_key, lock_id)

req = requests.session()
headers = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate',
			'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			'Connection':'keep-alive',
			'Host':'www.bjcourt.gov.cn',
			# 'Referer':'http://www.bjcourt.gov.cn/ktgg/index.htm?c=&court=&start=&end=&type=&p=11',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'
			}
conf = ProxyConf(key1)
# session = requests.session()
req.proxies = conf.get_proxy()
headers = {'Proxy-Authorization': conf.get_auth_header()}			
def nums_hi(pn):

	global go
	global ni
	global ngo
	global dup
	global err_num
	# url = 'http://www.bjcourt.gov.cn/ktgg/index.htm?c=&court=&start=&end=&type=&p=6179'
	bssample = ''

	conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
	cursor=conn.cursor()	
	while 1:

		try:
			f1 = open(filepath)
			pn = int(f1.read().strip())
			f1.close()

		except:
			pn = pn

		url = 'http://www.bjcourt.gov.cn/ktgg/index.htm?c=&court=&start=&end=&type=&p=%s' %pn

		try:
			# 无验证码情况
			r = req.get(url,headers=headers,timeout=30)
			bs = BeautifulSoup(r.text,'html5lib')
			# print 'bstry:',bs
			court_soup = bs.find(class_='ul_news_long')
			court_soup.text
			print 'no_yzm'

		except Exception as e:
			# 有验证码情况
			# print 'Exception', e
			while 1:
				try:
					r = req.get(yzm_url,headers=headers,timeout=30)
					f = open(imgpath,'wb')
					f.write(r.content)
					f.close()

					cmd = ocr_path+" "+imgpath
					# print 'cmd:'+cmd
					try:
                                                cc = subprocess.Popen(cmd.encode('GBK','ignore'),stdout=subprocess.PIPE)
                                        except:
                                                # req.proxies = conf.get_proxy()
                                                # headers = {'Proxy-Authorization': conf.get_auth_header()}
                                                r = req.get(yzm_url,headers=headers,timeout=30)
                                                f = open(imgpath,'wb')
                                                f.write(r.content)
                                                f.close()

                                                cmd = ocr_path+" "+imgpath
                                                cc = subprocess.Popen(cmd.encode('GBK','ignore'),stdout=subprocess.PIPE)
                                        c_result = cc.stdout.read()
					yzm = c_result.split('\r\n')[-2].strip()
					if u'beijingcourtocr.exe' in yzm:
                                                yzm = 'error'
					# print c_result.split('\r\n')
					# print 'c_result',c_result,type(c_result)
					print 'yzm:',yzm
					# os.remove(route) 	
					params = {'yzm':yzm}
					r = req.post(url=check_sure,params=params,headers=headers)
					# print 'rzm:',r.content

					url = 'http://www.bjcourt.gov.cn/ktgg/index.htm?c=&court=&start=&end=&type=&p=%s' %pn

					r = req.get(url,headers=headers,timeout=30)
					# print r.text
					soup = BeautifulSoup(r.text,'html5lib')
					court_soup = soup.find(class_='ul_news_long')
					court_soup.text
					# print 'court_soup:',court_soup
					err_num == 0
					break
				except Exception as e:
					# print u'验证码继续识别中', e, err_num
					# conf = ProxyConf(key1)
					# # session = requests.session()
					# req.proxies = conf.get_proxy()
					# headers = {'Proxy-Authorization': conf.get_auth_header()}

					if err_num == 20:
						print u'当前网站不可用，程序退出'
						# sys.exit(1)
						raise
					err_num += 1


		# page = court_soup.find(class_='turn_page')
		# print 'pages:',page

		# 结束条件验证，网页重复三次
		# if bssample == soup.text:
		# 	print u'网页重复'
		# 	dup += 1
		# 	if dup == 3:
		# 		print u'最后一页，程序结束，页码回归'
		# 		f = open(filepath,'w')
		# 		f.write(str(1))
		# 		f.close()				
		# 		break
		# bssample = soup.text

		# # ip被封情况，20分钟休息继续尝试
		# if u'访问频繁' in court_soup.text:
		# 	print u'ip暂时被封，休息20分钟'
		# 	# conf = ProxyConf(key1)
		# 	# # session = requests.session()
		# 	# req.proxies = conf.get_proxy()
		# 	# headers = {'Proxy-Authorization': conf.get_auth_header()}			
		# 	time.sleep(1200)
		# 	continue

		li_list = court_soup.find_all('li')
		print u'*************现在加载的页面:**************', pn

		for i in range(len(li_list)):
			# a = li[i]
			# print i,li[i].text,li[i].a.get_attribute('href')
			lim = li_list[i].a
			link = lim.get('href')
			content = lim.get('title')
			# print 'link:', link, 'content', content
			# print '***'+content[0:content.index("，")]
			# print '***'+content[content.index("，")+1:]
			sub_url = host + link
			# print sub_url
			# NID = re.search(r'\d{4,6}',link).group()
			# NAJBH = re.search(r'\d{7,}',link).group()
			NID = re.search(r'(?<=NId=).*(?=&NAj)',link).group()
			NAJBH = re.search(r'(?<=jbh=).*.*',link).group()			
			# date = re.search(r'\w{,content.index(",")}',content).group()
			# print 'nid',NID,'najbh',NAJBH

			try:
				r = req.get(url=sub_url, headers=headers, timeout=15)
				sub_soup = BeautifulSoup(r.text,'html5lib')
				sub_soup.text
				# print u'  详情页面抓取'
			except:
				print u'  详情页面无法获取'
				continue
			time.sleep(0.5)

			try:
				print u'抓取详细信息中。。。。。。'
				sub_content = sub_soup.find(class_='article_con').find_all('p')
				fa_yuan = sub_content[0].text
				gong_gao_nei_rong = sub_content[2].text
				fa_bu_shi_jian = sub_content[4].text
				# print '*****','fy',fa_yuan,'neirong',gong_gao_nei_rong,'fb_time',fa_bu_shi_jian
			except:
				print u'ouch详情页面没加载出来,忽略'
				continue

			# print 'ffeiifjl'+gong_gao_nei_rong
			# date = re.search(r'二\w',sf).group()
			# print 'NID:',NID,'NAJBH:',NAJBH,'\n'
			# print i,link,'\n',content, 'date', date

			sql = "insert into bjcourt VALUES ('%s','%s','%s','%s','%s','%s')" %(NID,NAJBH,\
				fa_yuan,gong_gao_nei_rong,fa_bu_shi_jian,today)

			try:
				print '********',pn,i,sql.encode('gbk')
			except:
				print '*****',pn,i,'illegal chars'

			try:
				cursor.execute(sql)
				conn.commit()
				print '***NEW'
			except Exception as e:
				print '**ALREADY EXISTS',e

		print '第%s页抓取完成' %pn
		pn += 1
		f = open(filepath,'w')
		f.write(str(pn))
		f.close()
		time.sleep(0.5)
			


	conn.close()
	print u'over小宠辛苦了'
	# driver.close()

if __name__ == '__main__':
        while 1:
                try:
                        conf = ProxyConf(key1)
                        # session = requests.session()
                        req.proxies = conf.get_proxy()
                        headers = {'Proxy-Authorization': conf.get_auth_header()}
                        nums_hi(1)
                except Exception as e:
                        print e,time.ctime()
                        time.sleep(1)
