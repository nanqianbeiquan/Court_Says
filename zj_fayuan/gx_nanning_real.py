# coding=utf-8
import os
import sys
import SpiderMan
from bs4 import BeautifulSoup
from mysql_db.UpdateStatus import *
from log_conf.LogConf import *
import logging
import re
import traceback


reload(sys)
sys.setdefaultencoding('utf-8')
order_nbr = '5fe6cf97-5592-11e7-be16-f45c89a63279'
requests = SpiderMan.SpiderMan(order_nbr, keep_session=True)
pinyin='gx_nanning2nd_real'
update_start_status(pinyin)
create_logfile(pinyin)


shi_qu = u'南宁市'

try:
    for p in range(1, 2):
        url = 'http://nnzy.chinacourt.org/article/index/id/M0g3MzAwNTAwNCACAAA%3D/page/' + str(p) + '.shtml'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')
        detail_list = soup.find_all('ul')[4].find_all('li')
        i = 0
        for detail in detail_list:
            i += 1
            title = detail.find('a').text

            if u'开庭公告' in title:

                href_list = detail.find('span').a['href']
                i_d = re.search(r'\d{5,}', href_list).group()
                href = 'http://nnzy.chinacourt.org' + href_list
                r = requests.get(href)
                detail = BeautifulSoup(r.text, 'html5lib')
                cc = detail.find_all(class_='text')[1].text.split('\n')

                klist = []
                for j in range(len(cc)):

                    if cc[j].strip() != '':
                        sh = cc[j].strip().replace('\n', '')
                        klist.append(sh)

                kmist = []
                cnn = 0
                for m in range(len(klist)):
                    aa = klist[m]
                    kmist.append(aa)

                    if u'成员：' in klist[m]:

                        cnn += 1
                        an_hao = kmist[0]
                        nei_rong = kmist[1]
                        shi_jian = kmist[2]
                        fa_ting = kmist[3]
                        cheng_yuan = kmist[4]
                        sql = "insert into gx_nanning2nd_real VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % \
                              (i_d, an_hao, nei_rong, shi_jian, fa_ting, cheng_yuan, today, shi_qu)

                        kmist = []

                        try:

                            MySQL_court.execute_update(sql)
                        except Exception,e:

                            print 'aaaaa'
                        else:
                            logging.info(an_hao)
except Exception, e:
    logging.error(traceback.format_exc())
else:
    update_end_status(pinyin)
