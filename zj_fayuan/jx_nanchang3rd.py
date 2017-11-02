# coding=utf-8
import sys
import requests
from bs4 import BeautifulSoup
import re
import urllib
import urllib2
import httplib2
from mysql_db.UpdateStatus import *
from log_conf.LogConf import *
import logging
import traceback
reload(sys)
sys.setdefaultencoding('utf8')
shi_qu=u'南昌市'
pinyin='jx_nanchang3rd'



thday = (datetime.date.today() + datetime.timedelta(-45)).strftime('%Y-%m-%d')
req = requests.session()


class court_mighty(object):


    def __init__(self):  # u'初始化参数等等'

        self.url0 = 'http://nczy.chinacourt.org/article/index/id/MzAxMzAwNjAwMiACAAA%3D/page/1.shtml'  # u'南昌中级法院'
        self.host = 'http://nczy.chinacourt.org'

    def param_deal(self, n):  # u'参数修改，n为页数'

        param = {
            'currentPage': n,
            'dsr': '',
            'dz': '',
            'fydm': 510000,
            'ktrq1': '',  # thday,
            'ktrq2': '',  # today,
            'mhpp': 1,
            'nav': 02,
            'nd': 2017,
            'opt': 'qbkt',
            'zh': '',
        }
        return param

    def headers_deal(self):
        headers = {
            # 'Accept-Encoding':'gzip, deflate',
            'Host': 'nczy.chinacourt.org',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
        }
        # print headers
        return headers



    def url_deal(self, n):  # u'url改造工厂'
        # urlo = self.url0

        url = 'http://nczy.chinacourt.org/article/index/id/MzAxMzAwNjAwMiACAAA%3D/page/' + str(n) + '.shtml'
        self.n = n
        # print 'url',url
        return url

    def quest_getout(self, url, headers):  # httplib2

        h = httplib2.Http()
        he, co = h.request(url, 'GET', headers=headers)
        return co

    def quest_getout1(self, url, headers):  # urllib2
        req = urllib2.Request(url, headers=headers)
        requ = urllib2.urlopen(req).read()
        return requ

    def quest_getout2(self, url, headers):  # requests,可接headers
        # print url
        req = requests.session()
        r = req.get(url=url, headers=headers, timeout=60)
        # r = requests.get(url,headers)
        # print r.encoding
        # r.encoding = 'gbk'  #u'乱码情况使用'
        return r.text

    def quest_postout(self, url, param, headers):  # httplib2

        data = urllib.urlencode(param)  # u'带参数的需要对参数进行加工'
        # print 'post_data_dealer',data
        h = httplib2.Http()
        he, co = h.request(url, 'POST', data, headers=headers)
        # he,co = h.request(url,'POST',data)
        return co.decode('utf-8')
    #
    # def quest_postout1(self, url):  # urllib2
    #
    #     data = urllib.urlencode(param)
    #     req = httplib2.Request(url)
    #     opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
    #     con = opener.open(req, data).read()
    #     return con

    def quest_postout2(self, url, data, headers):  # requests

        r = req.post(url, data, headers=headers)
        # r = requests.post(url,data)
        # print r.encoding
        # r.encoding = 'gbk'
        return r.text

    def beaut_souping(self, thn):  # Beautifulsoup处理网页文本,有乱码情况

        mat = thn
        bs = BeautifulSoup(mat, 'lxml')
        return bs

    def re_search(self, rule, strings):  # 正则截取匹配内容
        res = re.search(rule, strings).group()
        return res

    def get_url(self, bs):  # 第一页网站数据抓取
        lin = bs.find(class_='sswy_sub_con_box').div.find_all('a')[0].get('href')
        return lin

    def text_analysis(self, bs):  # 第一页网站数据抓取
        tas = bs.find(id='main').find(id='list')
        ta = tas.ul.find_all('li')
        cnt = 0
        # print 'len(ta)',len(ta)
        for i in range(len(ta)):
            la = ta[i].find_all('span')[0].a
            linka = la.get('href')
            # print 'link', linka
            link_id = re.search(r'\d{5,}', linka).group()
            link = self.host + linka
            title = la.get('title')

            # print i,title,link_id,link
            # print 'cnt',cnt
            # if cnt == 2:
            self.cnt = cnt
            self.title = title
            self.link_id = link_id
            te = self.quest_getout2(link, self.headers_deal())

            self.sub_page(te)
            cnt += 1
        # linka= ta[i].a.get('href')
        # link = self.host+'/'+linka
        # link_id = re.search(r'\d{2,}',link).group()
        # title = ta[i].a.get('title')
        # if u'罪犯' not in title:
        # 	# print i,cnt,link,title
        # 	self.cnt = cnt
        # 	self.title = title
        # 	self.link_id=link_id
        # 	te=self.quest_getout(link,self.headers_deal())
        # 	self.sub_page(te)
        # 	cnt+=1
        # 	tm = ta[i].find_all('td')[1].text.strip()
        # 	link_text = title+' '+tm
        # 	self.link_text=link_text
        # 	self.link_id = link_id
        # 	# print i,cnt,link,link_text,link_id
        # 	# if cnt==1 or cnt==2 or cnt==5:
        # 	self.cnt=cnt
        # te = self.quest_getout2(link,self.headers_deal())
        # self.sub_page(te)
        # cnt+=1

        # 	td_list = ta[i].find_all('td')
        # 	num = td_list[0].text.strip()
        # 	fa_yuan = td_list[1].text.strip()
        # 	kai_ting_shi_jian = td_list[2].text.strip()
        # 	kai_ting_di_dian = td_list[3].text.strip()
        # 	an_hao = td_list[4].text.strip()
        # 	dang_shi_ren = td_list[5].text.strip()
        #
        # 	sql = "insert into sc_gaoyuan2nd VALUES('%s','%s','%s','%s','%s','%s','%s')" %(num,fa_yuan,\
        # 		kai_ting_shi_jian,kai_ting_di_dian,an_hao,dang_shi_ren,today)
        # 	try:
        # 		print i,sql
        # 	except:
        # 		print i,'illegal coding'
        # 	self.data_in(sql)

    #



    def sub_page(self, te):  # 第一页链接过去的内容，第二子页处理
        bs = self.beaut_souping(te)
        # print bs
        try:
            divs = bs.find(class_='text')
        # print 'divs..',divs
        except:
            print 'last page %s reach,go break' % self.n
            exit(0)
        # pn = divs.text.strip().replace('\n','').replace(' ','').replace(' ','')\
        # .replace(u'特此公告。','').replace(u'公告','').replace(u'四川省眉山市中级人民法院','')\
        # .replace(u'本院',u'四川省眉山市中级人民法院')
        # print 'divs',len(divs.text.split('\n'))
        # laos = divs.text.split('\n')
        # li = [x for x in laos if x.strip() != '']
        # print 'li'#,len(li),li[0]
        text = divs.text.strip().replace('\n', '').replace(' ', '')
        # print shi_jian,fa_ting,an_hao,an_you,cheng_ban_ren,dang_shi_ren
        sql = "insert into jx_nanchang3rd VALUES('%s','%s','%s','%s','%s')" % (self.link_id, self.title, \
                                                                          text, today,shi_qu)
        #print self.n, self.cnt, sql
        self.data_in(sql)

    # sql = "insert into sc_meishan2nd VALUES('%s','%s','%s','%s')" %(self.link_id,self.title,pn,today)




    def data_in(self, sql):
        try:
            MySQL_court.execute_update(sql)
        except:
            logging.error(traceback.format_exc())
        else:
            logging.info(sql)


if __name__ == '__main__':
    update_start_status(pinyin)
    create_logfile(pinyin)
    try:
        cla = court_mighty()
        for p in range(1, 2):
            url = cla.url_deal(p)
            # param = cla.param_deal(1)
            headers = cla.headers_deal()
            t = cla.quest_getout(url, headers)
            # print t
            rin = cla.beaut_souping(t)
            # print 'bsdetail',rin
            cla.text_analysis(rin)

    except Exception, e:
        logging.error(traceback.format_exc())
    else:
        update_end_status(pinyin)
