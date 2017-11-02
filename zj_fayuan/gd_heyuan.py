#coding=utf-8
import SpiderMan
from lxml import html
import sys
from mysql_db.UpdateStatus import *
from log_conf.LogConf import *
import logging
import traceback

reload(sys)
sys.setdefaultencoding('utf8')
shi_qu=u'河源'
pinyin='gd_heyuan'
order_nbr = '5fe6cf97-5592-11e7-be16-f45c89a63279'
requests = SpiderMan.SpiderMan(order_nbr, keep_session=True)
#headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'}
                    
update_start_status(pinyin)
create_logfile(pinyin)
try:
    url='http://www.hycourts.gov.cn/ssfw/ktggIndex.aspx'
    page_context=requests.get(url)
    tree= html.fromstring(page_context.text)
    def do_tree(tree):
        total_inform=tree.xpath('//table[@class="d_l_table"]/tr')[1:]
        if total_inform:
            for one_inform in total_inform:
                an_hao=one_inform.xpath('td[1]/text()')[0]
                ri_qi=one_inform.xpath('td[2]/text()')[0]
                shi_jian=one_inform.xpath('td[3]/text()')[0]
                di_dian=one_inform.xpath('td[4]/text()')[0]
                cbr=one_inform.xpath('td[5]/text()')[0]
                dsr=one_inform.xpath('td[6]/text()')[0]
                sql="insert into gd_heyuan values('%s','%s','%s','%s','%s','%s','%s','%s')" %(an_hao,\
                                                                    ri_qi,shi_jian,di_dian,cbr,dsr,today,shi_qu)
                try:
                    MySQL_court.execute_update(sql)
                    print an_hao+ri_qi+shi_jian+di_dian+cbr+dsr
                except:
                    print an_hao+ri_qi+'出现重复'
                else:
                    logging.info(an_hao+ri_qi)
            #return an_hao,ri_qi,shi_jian,di_dian,cbr,dsr

    total_page=int(tree.xpath('//select[@id="anpNewsList_input"]/option[last()]/@value')[0])
    if  total_page==1:
        do_tree(tree)
    else:
        __EVENTTARGET='anpNewsList'
        __VIEWSTATE=tree.xpath('//input[@id="__VIEWSTATE"]/@value')[0]
        __VIEWSTATEGENERATOR=tree.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value')[0]
        __EVENTVALIDATION=tree.xpath('//input[@id="__EVENTVALIDATION"]/@value')[0]
        for i in range(1,total_page+1):
            data={
            '__VIEWSTATE':__VIEWSTATE,
            '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
            '__EVENTTARGET':__EVENTTARGET,
            '__EVENTARGUMENT':str(i),
            '__EVENTVALIDATION':__EVENTVALIDATION,
            'anpNewsList_input':'1'
            }
            page_context=requests.post(url,data=data,timeout=200)
            tree= html.fromstring(page_context.text)
            print 'page'+str(i)
            do_tree(tree)
except:
        logging.error(traceback.format_exc())
else:
    #更新爬虫结束状态
    update_end_status(pinyin)
