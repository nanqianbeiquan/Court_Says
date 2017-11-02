# coding=utf-8
import os
import sys
import SpiderMan
import traceback
from bs4 import BeautifulSoup
from mysql_db.UpdateStatus import *
from log_conf.LogConf import *
import logging
reload(sys)
sys.setdefaultencoding('utf8')


order_nbr = '5fe6cf97-5592-11e7-be16-f45c89a63279'
requests = SpiderMan.SpiderMan(order_nbr, keep_session=True)
shi_qu=u'苏州市'
pinyin='szfy'
#更新状态 开始爬虫
update_start_status(pinyin)
#创建日志
create_logfile(pinyin)

try:
    main_url='http://www.szzjrmfy.gov.cn/shenwu.php?typeid=110'
    mars = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
    cont = 0
    r = requests.get(main_url)
    r.encoding = 'gb2312'
    code=r.status_code
    if not code==200:
        logging.error(main_url + ' ****http:状态码为：' + str(code) )
    detail = BeautifulSoup(r.text, 'html5lib')
    cc = detail.find_all(class_='newsrightnr')[0].find_all('ul')[1].find_all('li')
    for c in cc:
        text1=c.find('a').text
        if text1.startswith('开庭公告'):
            url= 'http://www.szzjrmfy.gov.cn'+c.a['href']
            logging.info('苏州开庭公告地址：'+url )

    r = requests.get(url)
    r.encoding = 'gb2312'
    code=r.status_code
    if not code==200:
        logging.error(url + ' ****http:状态码为：' + str(code))
    rbs = BeautifulSoup(r.text, 'html5lib')
    ps = rbs.find_all('p')
    for i in range(len(ps)):
        c = ps[i].text.split('\n\n')
        for j in range(len(c)):
            das = []
            mm = c[j].split('\n')
            for l in range(len(mm)):
                # if l==0:
                # print l,mm[l],type(mm[l])
                la = mm[l].split('：')
                # print la[0],len(la),la[1]

                if la[0] == u'案　号':
                    das.append('0')
                    an_hao = la[1]
                    print '****anhao****', an_hao

                elif la[0] == u'案　由':
                    das.append('1')
                    an_you = la[1]
                    print 'anyou', an_you
                elif la[0] == u'当事人':
                    das.append('2')
                    dang_shi_ren = la[1]
                    print '***dangshiren***', dang_shi_ren
                elif la[0] == u'审判长':
                    das.append('3')
                    shen_pan_zhang = la[1]
                    print 'shenpanzhang', shen_pan_zhang
                elif la[0] == u'合议庭':
                    das.append('4')
                    he_yi_ting = la[1]
                    print 'heyiting', he_yi_ting
                elif la[0] == u'地　点':
                    das.append('5')
                    di_dian = la[1]
                    print 'place', di_dian
                elif la[0] == u'日　期':
                    das.append('6')
                    ri_qi = la[1]
                    print 'date', ri_qi
                elif la[0] == u'时　间':
                    das.append('7')
                    shi_jian = la[1]
                    print 'time', shi_jian
                elif la[0] == u'书记员':
                    das.append('8')
                    shu_ji_yuan = la[1]
                    print 'shujiyuan', shu_ji_yuan
                else:
                    print 'boom'
            # print das
            con = [i for i in mars if i not in das]
            for cm in con:
                if cm == '0':
                    an_hao = ''
                elif cm == '1':
                    an_you = ''
                elif cm == '2':
                    dang_shi_ren = ''
                elif cm == '3':
                    shen_pan_zhang = ''
                elif cm == '4':
                    he_yi_ting = ''
                elif cm == '5':
                    di_dian = ''
                elif cm == '6':
                    ri_qi = ''
                elif cm == '7':
                    shi_jian = ''
                elif cm == '8':
                    shu_ji_yuan = ''
                else:
                    print "what's this:", cm
            if an_hao == '':
                continue
            sql = "INSERT INTO szfy VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            an_hao, an_you, dang_shi_ren, \
            shen_pan_zhang, he_yi_ting, di_dian, ri_qi, shi_jian, shu_ji_yuan, today,shi_qu)
            cont = cont + 1
            print i, j, sql, 'miao', cont
            select_sql="select * from szfy where an_hao='%s' and ri_qi='%s' " % (an_hao,ri_qi)
            has_result=MySQL_court.execute_query(select_sql)
            if not has_result:
                try:
                    MySQL_court.execute_update(sql)
                    print '%s GETS NEW' % an_hao
                except:
                    logging.error(sql)
                    logging.error(traceback.format_exc())
                else:
                    logging.info(an_hao+ri_qi)
except:
        logging.error(traceback.format_exc())
else:
    #更新爬虫结束状态
    update_end_status(pinyin)

