# coding=utf-8
import sys
import SpiderMan
from bs4 import BeautifulSoup
import traceback
import re
from mysql_db.UpdateStatus import *
from log_conf.LogConf import *
import logging

reload(sys)
sys.setdefaultencoding('utf8')
pinyin='putianfy'
order_nbr = '5fe6cf97-5592-11e7-be16-f45c89a63279'
requests = SpiderMan.SpiderMan(order_nbr, keep_session=True)
#headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'}

update_start_status(pinyin)
create_logfile(pinyin)
url = 'http://ptzy.chinacourt.org/article/index/id/MzAuNzAwNzAwNCACAAA%3D.shtml'
host = 'http://ptzy.chinacourt.org'


def do_mysql(link_id, gg_detail, sql):
    select_sql = "select * from putianfy where link_id='%s' and gg_detail='%s' " % (link_id, gg_detail)
    has_result = MySQL_court.execute_query(select_sql)
    if not has_result:
        try:
            MySQL_court.execute_update(sql)
        except:
            logging.error(sql )
            logging.error(traceback.format_exc() )
        else:
            logging.info(link_id + gg_detail )


try:
    r = requests.get(url)
    code = r.status_code
    if not code == 200:
        logging.error(url + ' ****http:状态码为：' + str(code))
    rbs = BeautifulSoup(r.text, 'html5lib')
    li_list = rbs.find_all(class_='yui3-g list_br')[1].find_all('li')
    for i in range(len(li_list)):
        at = li_list[i].find_all('span')[0].a
        linp = at['href']
        if str(linp).startswith('/'):
            link = host + linp
            link_id = re.search(r'\d{6,}', linp).group()
            link_text = at.text.strip()
            r1 = requests.get(link)
            code = r1.status_code
            if not code == 200:
                logging.error(link + ' ****http:状态码为：' + str(code) )
            r1bs = BeautifulSoup(r1.text, 'html5lib')
            ta = r1bs.find(class_='detail').find_all('div')[6]
            tap = ta.find_all('p')

            if len(tap) == 0:
                ash = ta.text.split('\n\n')
                for j in range(len(ash)):
                    te = ash[j].strip().replace(' ', '').replace('	', '').replace('\n', '')
                    sql = "insert into putianfy values('%s','%s','%s','%s')" % (link_id, link_text, te, today)

                    do_mysql(link_id, te, sql)
            if len(tap) == 1:
                if i == 39:
                    bsh = ta.text.split('。')
                    for k in range(len(bsh)):
                        if bsh[k].strip() != '':
                            te = bsh[k].strip().replace(' ', '').replace('	', '').replace('\n', '')
                            sql = "insert into putianfy values('%s','%s','%s','%s')" % (link_id, link_text, te, today)

                            do_mysql(link_id, te, sql)
                if i == 40:
                    bsh = ta.text.split(' ')
                    for k in range(len(bsh)):
                        te = bsh[k].strip().replace(' ', '').replace('	', '').replace('\n', '')
                        sql = "insert into putianfy values('%s','%s','%s','%s')" % (link_id, link_text, te, today)

                        do_mysql(link_id, te, sql)
            else:
                for k in range(len(tap)):
                    te = tap[k].text.strip().replace(' ', '').replace('	', '').replace('\n', '')
                    sql = "insert into putianfy values('%s','%s','%s','%s')" % (link_id, link_text, te, today)

                    do_mysql(link_id, te, sql)
        else:
            logging.error(linp + '  wrong!!!!!!!!!!!!!!!!!!' )
            print linp + '  wrong!!!!!!!!!!!!!!!!!!'

except Exception, e:
    logging.error(traceback.format_exc())
else:
    update_end_status(pinyin)
