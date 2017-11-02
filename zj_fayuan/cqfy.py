# coding=utf-8
import sys
import multiprocessing
from lxml import html
import traceback
import re
import SpiderMan
from mysql_db.UpdateStatus import *
from log_conf.LogConf import *
import logging
reload(sys)
sys.setdefaultencoding('utf8')


order_nbr = '5fe6cf97-5592-11e7-be16-f45c89a63279'
requests = SpiderMan.SpiderMan(order_nbr, keep_session=True)
pinyin='chongqing_fy'
main_url='http://www.cqfygzfw.com/court/gg_listgg.shtml'
content_url_ahead='http://www.cqfygzfw.com/court/gg_ggxx.shtml?gg.id='

update_start_status(pinyin)



def get_pageno(d):
    page_content=requests.get(d)
    code=page_content.status_code
    if not code==200:
        logging.error(d + ' ****http:状态码为：' + str(code) )
        return 'bad'
    try:
        tree=html.fromstring(page_content.text)
        fanye=tree.xpath('//div[@class="fanye"]')[0]
        pagenotext=fanye.xpath('string(.)')
        pageno=re.findall('\/(.*?)页',str(pagenotext))[0]
    except:
        logging.error( d+'页数为0或者网页结构变了' )
        return 'nodata'
    else:
        return pageno


def get_content(url,an_hao_list,lock):

    page_content=requests.get(url)
    code=page_content.status_code
    if not code==200:

        logging.error(url + ' ****http:状态码为：' + str(code) )

    tree=html.fromstring(page_content.text)
    table=tree.xpath('//div[@class="r_wenben"]/table[@class="table_ys"]/tbody/tr')
    for inform in table:
        fa_yuan=inform.xpath('td[1]/text()')[0]
        an_hao=inform.xpath('td[2]/a/text()')[0].strip()
        aurl=inform.xpath('td[2]/a/@onclick')[0]
        content_url_back=re.findall("'(.*)'",aurl)[0]
        page_content=requests.get(content_url_ahead+content_url_back)
        code=page_content.status_code
        if not code==200:
            logging.error(url + ' ****http:状态码为：' + str(code) )
        tree=html.fromstring(page_content.text)
        table_info=tree.xpath('//table[@class="table_ys2"]/tbody/tr[2]/td')[0]
        nei_rong=table_info.xpath('text()')[0].replace(' ','')
        cbr=re.findall('承办人：(.*)',str((table_info).xpath('string(.)')),re.S)[0].strip()
        kt_date=inform.xpath('td[3]/text()')[0]

        select_sql="select * from chongqing_fy where an_hao='%s' and kt_date='%s' " % (an_hao,kt_date)
        has_result=MySQL_court.execute_query(select_sql)
        if not has_result:

                sql="insert into chongqing_fy values('%s','%s','%s','%s','%s','%s','%s')" %(content_url_back,\
                                                                    an_hao,fa_yuan,kt_date,nei_rong,today,cbr)
                try:
                    MySQL_court.execute_update(sql)
                except Exception,e:
                    logging.error(sql)
                    logging.error(traceback.format_exc())
                else:
                    logging.info(kt_date+an_hao)
        else:
            if an_hao not in an_hao_list.keys():
                an_hao_list[an_hao]=0
            an_hao_list[an_hao]+=1


def func():
    for i in range(0,15):
        today_now=datetime.date.today()
        yesterday = str(today_now+datetime.timedelta(days=i))
        print yesterday
        c='http://www.cqfygzfw.com/court/gg_listgg.shtml?gg.endDate='+yesterday+'&gg.startDate='+yesterday+'&gg.fydm=&gg.ggnr=&page='
        d='http://www.cqfygzfw.com/court/gg_listgg.shtml?gg.endDate='+yesterday+'&gg.startDate='+yesterday+'&gg.fydm=&gg.ggnr=&page=1'
        try:
            pageno=int(get_pageno(d))
        except:
            if get_pageno(d)=='nodata':
                break
            else:
                logging.error('获取页数失败，如果没有http状态码说明dom属性发生变化')
                logging.error(traceback.format_exc())
        else:
            manager = multiprocessing.Manager()
            lock = manager.Lock()
            an_hao_list = manager.dict()

            p = multiprocessing.Pool(processes = 10)
            print '抓取'+yesterday+' 的数据'+'总页数：'+str(pageno)
            logging.info(yesterday+'页数：'+str(pageno))
            for i in range(1, pageno+1):
                url=c+str(i)
                p.apply_async(get_content,[url,an_hao_list,lock])
            p.close()
            p.join()
            an_hao_list = dict(an_hao_list)
            for an_hao in an_hao_list:
                pass
                #print an_hao+'多出现的次数：'+str(an_hao_list[an_hao])



if __name__ == "__main__":
    create_logfile(pinyin)
    try:
        func()
    except:
        logging.error(traceback.format_exc())
    else:
        update_end_status(pinyin)






