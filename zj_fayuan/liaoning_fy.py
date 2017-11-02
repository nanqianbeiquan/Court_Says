# coding=utf-8
import sys
from lxml import html
import traceback
import SpiderMan
from mysql_db.UpdateStatus import *
from log_conf.LogConf import *
import logging
reload(sys)
sys.setdefaultencoding('utf8')

pinyin='liaoning_fy'
order_nbr = '5fe6cf97-5592-11e7-be16-f45c89a63279'
requests = SpiderMan.SpiderMan(order_nbr, keep_session=True)
url = 'http://www.lnsfy.gov.cn/ktgg/index.jhtml'

update_start_status(pinyin)
create_logfile(pinyin)

def get_tree(url):
    page_html = requests.get(url)
    code = page_html.status_code
    if not code == 200:
        logging.error(url + ' ****http:状态码为：' + str(code))
        return 0
    else:
        tree = html.fromstring(page_html.text)
        return tree


try:
    tree = get_tree(url)
    pageno = int(tree.xpath('//div[@id="pag"]/p/a[last()-1]/text()')[0])
    for i in range(1, pageno+ 1):
        url = 'http://www.lnsfy.gov.cn/ktggPage.jspx?channelId=235&listsize=' + str(pageno) + '&pagego=' + str(i)
        page_html = requests.get(url)
        tree = html.fromstring(page_html.text)
        table_li = tree.xpath('//div[@class="Sub fr"]/ul/li')
        for one_li in table_li:
            gg_detail = one_li.xpath('a/@title')[0]
            select_sql="select * from liaoning_fy where gg_detail='%s' " % (gg_detail, )
            has_result=MySQL_court.execute_query(select_sql)
            if not has_result:
                sql = "insert into liaoning_fy values('%s','%s')" % (gg_detail, today)
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

