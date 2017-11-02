# coding=utf-8
import sys
import re
import SpiderMan
from lxml import html
import traceback
from mysql_db.UpdateStatus import *
from log_conf.LogConf import *
import logging

reload(sys)
sys.setdefaultencoding('utf8')

order_nbr = '5fe6cf97-5592-11e7-be16-f45c89a63279'
requests = SpiderMan.SpiderMan(order_nbr, keep_session=True)

shi_qu = u'徐州市'
pinyin='xzfy'
#更新状态 开始爬虫
update_start_status(pinyin)
#创建日志
create_logfile(pinyin)


try:
    for p in range(1, 2):
        url = 'http://xzzy.chinacourt.org/article/index/id/MzAqNjAwNTAwNCACAAA%3D/page/' + str(p) + '.shtml'
        host = 'http://xzzy.chinacourt.org'
        r = requests.get(url)
        code = r.status_code
        if not code == 200:
            logging.error(url + ' ****http:状态码为：')
        tree = html.fromstring(r.text)
        li_list = tree.xpath('//div[@id="list"][3]/ul/li')
        for one_li in li_list:
            back_url = one_li.xpath('span[@class="left"]/a/@href')[0]
            gong_gao = one_li.xpath('span[@class="left"]/a/text()')[0]
            link = host + back_url
            link_id = re.search(r'\d{6,}', link).group()

            r2 = requests.get(link)
            code = r2.status_code
            if not code == 200:
                logging.error(link + ' ****http:状态码为：' + str(code))
            tree2 = html.fromstring(r2.text)
            # page_text=tree2.xpath('//div[@class="text"]/text()')[0]
            info = tree2.xpath('//div[contains(@class,"text")]')[0]

            if re.search('\d', gong_gao[0]):
                all_content = info.xpath('p/text()')
                if not all_content:
                    page_text = info.xpath('string(.)').split(u'\n\n')
                    for x in page_text:
                        gg_detail = x.strip()

                        select_sql = "select * from xzfy where gong_gao='%s' and gg_detail='%s' " % (
                        gong_gao, gg_detail)
                        has_result = MySQL_court.execute_query(select_sql)
                        if not has_result:
                            insert_sql = "INSERT INTO xzfy values('%s','%s','%s','%s','%s')" % (
                            link_id, gong_gao, gg_detail, today, shi_qu)
                            try:
                                MySQL_court.execute_update(insert_sql)
                            except:

                                logging.error(insert_sql )
                                logging.error(traceback.format_exc())
                            else:
                                logging.info(gg_detail +'  insert success')
                else:
                    for x in all_content:
                        gg_detail = x.strip()

                        select_sql = "select * from xzfy where gong_gao='%s' and gg_detail='%s' " % (
                        gong_gao, gg_detail)
                        has_result = MySQL_court.execute_query(select_sql)
                        if not has_result:
                            insert_sql = "INSERT INTO xzfy values('%s','%s','%s','%s','%s')" % (
                            link_id, gong_gao, gg_detail, today, shi_qu)
                            try:
                                MySQL_court.execute_update(insert_sql)
                            except:

                                logging.error(insert_sql )
                                logging.error(traceback.format_exc() )
                            else:
                                logging.info(gg_detail + '   insert success')

            else:
                gg_detail = info.xpath('string(.)')
                select_sql = "select * from xzfy where gong_gao='%s' and gg_detail='%s' " % (gong_gao, gg_detail)
                has_result = MySQL_court.execute_query(select_sql)
                if not has_result:
                    insert_sql = "INSERT INTO xzfy values('%s','%s','%s','%s','%s')" % (
                    link_id, gong_gao, gg_detail, today, shi_qu)
                    try:
                        MySQL_court.execute_update(insert_sql)
                    except:
                        logging.error(insert_sql )
                        logging.error(traceback.format_exc() )
                    else:
                        logging.info(gg_detail+' insert success')
except Exception, e:
    logging.error(traceback.format_exc() + '\n')
else:
    update_end_status(pinyin)


