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
print datetime.datetime.now().strftime('%Y-%m-%d')
# print str(datetime.datetime.now())[0:10]
reload(sys)
sys.setdefaultencoding('utf8')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')

conn = MySQLdb.connect(host='210.16.191.150',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='court_notice',charset='utf8')
cursor=conn.cursor()
href = "http://www.gdjyfy.cn/WebServer/ArticleInfo.aspx?Id=15154"
# r = requests.get(url)
xiang_qing=requests.get(href )
xiang_qing.encoding='utf8'
nei_rong=BeautifulSoup(xiang_qing.text,'html5lib')
# print nei_rong
nr=nei_rong.find(class_="con article-place")
# nr_each=nr.split('br')
anhao_each=nr.text.split("案号:",3)
# nr_td=nr.text.strip().replace('\n','')
print  nr.text.strip()
# print  nr_each[0]
# an_hao1=re.search(u'案号.*号',nr_td).group().strip()
# an_hao2=re.search(u'案号.*号',nr_td).group().strip(u'案号：')
# an_hao=nr_td.split('：',3)[0].strip(u'案由：')
# an_you=nr_td.split('：',3)[1].strip(u'当事人：')
# print an_hao
# print an_you
# zhu_shen=nr_td.split('：',8)[3].strip(u'书记员：')
# shu_ji_yuan=nr_td.split('：',8)[4].strip(u'当事人：')
# dang_shi_ren=nr_td.split('：',8)[5].strip(u'立案时间：')
# li_an=nr_td.split('：',8)[6].strip(u'结案时间：')
# jie_an=nr_td.split('：',8)[7].strip(u'案件状态：')
# zhuang_tai=nr_td.split('：',8)[8].strip(u'通过')
# zhuang_tai=re.search(u'案件状态.*通',nr_td).group().strip(u'案件状态：').strip(u'通')
# print an_hao,an_you,zhu_shen,shu_ji_yuan,dang_shi_ren,li_an,jie_an,zhuang_tai

	





