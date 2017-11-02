# coding=utf-8
import os
import sys
import SpiderMan
from mysql_db.UpdateStatus import *
from log_conf.LogConf import *
import logging
from bs4 import BeautifulSoup
import traceback
import re

reload(sys)
sys.setdefaultencoding('utf-8')
order_nbr = '5fe6cf97-5592-11e7-be16-f45c89a63279'
requests = SpiderMan.SpiderMan(order_nbr, keep_session=True)
pinyin = 'js_zhenjiang'
update_start_status(pinyin)
create_logfile(pinyin)
shi_qu = u'镇江市'

url = 'http://www.zjzy.gov.cn/col79/articlecolumn.php?colid=79'
try:
    for n in range(1, 2):
        param = {
            'colid': 79,
            'currpage': n,
        }
        r = requests.post(url, data=param)
        r.encoding = 'GBK'
        rbs = BeautifulSoup(r.text, 'html5lib')
        bs = rbs.find_all('table')

        tr_list = bs[21].find_all('tr')
        for i in range(1, len(tr_list) - 3):
            # 		if i == 3:
            link = tr_list[i].find_all('td')[2].a['href']
            i_d = re.search(r'\d{3,}', link).group()
            # 		print '***************',i,link,i_d
            # 		if i == 3:
            r2 = requests.get(link)
            r2.encoding = 'GBK'
            r2bs = BeautifulSoup(r2.text, 'html5lib')
            cc = r2bs.find(class_='x_content').text.split('\n')
            klist = []
            for j in range(len(cc)):
                if cc[j].strip().replace('\n', '') != '':
                    sh = cc[j].strip().replace('\n', '')
                    klist.append(sh)
                # 				print sh
                # 				print j,cc[j]
                # 			print len(klist)
            kmist = []
            cnn = 0
            for m in range(len(klist)):
                # print u'第'+str(i)+u'行',m,klist[m]
                # continue
                aa = klist[m]
                # 				print klist[m]
                kmist.append(aa)
                if u'时　间：' in klist[m]:
                    cnn += 1
                    an_hao = kmist[0]
                    an_you = kmist[1]
                    shi_jian = kmist[-1]
                    ri_qi = kmist[-2]
                    fa_ting = kmist[-3]
                    nei_rong = ' '.join(kmist[0:])
                    sql = "insert into js_zhenjiang VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    i_d, an_hao, an_you, nei_rong, fa_ting, ri_qi, shi_jian, today, shi_qu)
                    # print n,i,cnn,sql
                    kmist = []
                    try:
                        MySQL_court.execute_update(sql)
                    # conn.commit()
                    except:
                        print 'aaaaa'
                    else:
                        logging.info(an_hao)

                elif u'开庭地点：' in klist[m]:
                    # print 'miao',m,klist[m]
                    cnn += 1
                    an_hao = ''
                    an_you = ''
                    shi_jian = ''
                    ri_qi = kmist[0]
                    fa_ting = ''
                    nei_rong = kmist[1].replace(' ', '').replace('  ', '')
                    sql = "insert into js_zhenjiang VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    i_d, an_hao, an_you, nei_rong, fa_ting, ri_qi, shi_jian, today, shi_qu)
                    # print n,i,cnn,sql
                    kmist = []
                    try:
                        MySQL_court.execute_update(sql)
                    except:
                        print 'aaaaa'
                    else:
                        logging.info(an_hao)

except:
        logging.error(traceback.format_exc())
else:
    #更新爬虫结束状态
    update_end_status(pinyin)

