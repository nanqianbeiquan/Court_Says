# coding=utf-8
import sys
from lxml import html
import re
import traceback
from mysql_db.UpdateStatus import *
from log_conf.LogConf import *
import logging
import SpiderMan

reload(sys)
sys.setdefaultencoding('utf8')
pinyin='sx_fy'

order_nbr = '5fe6cf97-5592-11e7-be16-f45c89a63279'
crawler = SpiderMan.SpiderMan(order_nbr, keep_session=True)
url = 'http://www.shanxify.gov.cn/ktgg/index.jhtml'
domain = 'http://www.shanxify.gov.cn'

update_start_status(pinyin)
create_logfile(pinyin)


def getA(nei_rong_url):
    page_content = crawler.get(nei_rong_url)
    tree = html.fromstring(page_content.text)
    try:
        nei_rong = tree.xpath('//div[@id="sjym"]/div[@class="center"]/div[@class="text"]/p[2]/text()')[0]
        fa_yuan_words = tree.xpath('//div[@id="sjym"]/div[@class="center"]/div[@class="text"]/h2/text()')[0]
        fa_yuan = re.findall(u'作者：(.*)', fa_yuan_words)[0]
    except:
        logging.error(nei_rong_url + '问题如下：')
        logging.error( traceback.format_exc() )
    else:
        return nei_rong, fa_yuan


try:
    page_content = crawler.get(url)
    tree = html.fromstring(page_content.text)
    last_page_url = tree.xpath('//div[@class="turn_page"]/p/a[last()-1]/@href')[0]
    last_page_no = int(re.findall('pagego=(\d{1,})', last_page_url)[0])
    for i in range(1, last_page_no + 1):
        logging.info(str(i)+ '当前的页数' )
        page_url = domain + re.sub('pagego=(\d{1,})', 'pagego=%s', last_page_url) % (str(i),)
        page_content = crawler.get(page_url)
        tree = html.fromstring(page_content.text)
        all_nei_rong = tree.xpath('//div[@class="right"]/div[@class="text"]/ul/li')
        for oneli in all_nei_rong:
            nei_rong_url = oneli.xpath('a/@href')[0]
            if nei_rong_url.startswith('http'):
                try:
                    nei_rong, fa_yuan = getA(nei_rong_url)
                except:
                    pass
                else:
                    select_sql="select * from sx_fy where nei_rong='%s' " % (nei_rong, )
                    has_result=MySQL_court.execute_query(select_sql)
                    if not has_result:
                        sql = "insert into sx_fy values('%s','%s','%s')" % (nei_rong, today, fa_yuan)
                        try:
                            MySQL_court.execute_update(sql)
                            # print nei_rong
                        except:
                            logging.error(sql)
                            logging.error(traceback.format_exc())
                        else:
                            now_now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            logging.info(str(now_now)+'   '+nei_rong)
            else:
                nei_rong_title = oneli.xpath('a/text()')[0]
                logging.error(nei_rong_title+'  标题超链接错误，无法看到内容，url为：'+nei_rong_url)
except Exception, e:
    logging.error(traceback.format_exc())
else:
    update_end_status(pinyin)
