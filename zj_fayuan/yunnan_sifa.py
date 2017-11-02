# coding=utf-8
import sys
from lxml import html
import traceback
from mysql_db.UpdateStatus import *
from log_conf.LogConf import *
import logging

import SpiderMan

order_nbr = '5fe6cf97-5592-11e7-be16-f45c89a63279'
requests = SpiderMan.SpiderMan(order_nbr, keep_session=True)
reload(sys)
sys.setdefaultencoding('utf8')
url='http://www.ynfy.gov.cn/ktggPage.jspx?channelId=858&listsize=691&pagego=1'
pinyin='yunnan_sifa'

update_start_status(pinyin)
create_logfile(pinyin)
try:
    page_html=requests.get(url)
    code=page_html.status_code
    if not code==200:
        logging.error(url + ' ****http:状态码为：' + str(code) )
    tree=html.fromstring(page_html.text)
    pageno=int(tree.xpath('//div[@class="turn_page"]/p/a[last()-1]/text()')[0])
    for i in range(1,pageno+1):
            url='http://www.ynfy.gov.cn/ktggPage.jspx?channelId=858&listsize=691&pagego='+str(i)
            page_html=requests.get(url)
            code=page_html.status_code
            if not code==200:
                logging.error(url + ' ****http:状态码为：' + str(code) )
            tree=html.fromstring(page_html.text)
            table_li=tree.xpath('//ul[@class="sswy_news"]/li')
            for one_li in table_li:
                    gg_detail=one_li.xpath('a/@title')[0]
                    select_sql="select * from yunnan_sifa where gg_detail='%s' " % (gg_detail, )
                    has_result=MySQL_court.execute_query(select_sql)
                    if not has_result:
                        sql="insert into yunnan_sifa values('%s','%s')" %(gg_detail,today)
                        try:
                            MySQL_court.execute_update(sql)
                        except:
                            logging.error(sql)
                            logging.error(traceback.format_exc())
                        else:
                            logging.info(gg_detail )

except Exception, e:
    logging.error(traceback.format_exc())
else:
    update_end_status(pinyin)



